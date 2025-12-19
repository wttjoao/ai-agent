from __future__ import annotations

import copy
import json
import re
from typing import Any, Dict, List, Optional

import requests
from langchain_ollama import ChatOllama
from langchain.tools import tool


INTERNAL_API_URL = "http://localhost:8001/artifacts"

model = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0.0,
)

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


def _coerce_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item.get("text", json.dumps(item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def _extract_first_json(text: str) -> str:
    text = text.strip()
    match = _JSON_FENCE_RE.search(text)
    if match:
        text = match.group(1).strip()

    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    start = min(i for i in (text.find("{"), text.find("[")) if i != -1)
    for end in range(len(text), start, -1):
        candidate = text[start:end].strip()
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            continue

    raise ValueError("No valid JSON found in model output")


def _model_json_call(prompt: str, retries: int = 1) -> Any:
    last_error = None
    for _ in range(retries + 1):
        resp = model.invoke(prompt)
        text = _coerce_content_to_text(resp.content)
        try:
            return json.loads(_extract_first_json(text))
        except Exception as e:
            last_error = e
            prompt += "\n\nCRITICAL: Return ONLY valid JSON. No explanations."
    raise RuntimeError(f"Model JSON failure: {last_error}")


@tool
def get_artifact_guid(
    case_id: int,
    artifact_schema_code: Optional[str] = None,
) -> List[str]:
    """Returns dataArtifactGUID(s) for a case."""
    params = {"case-id": case_id}
    if artifact_schema_code:
        params["artifactSchemaCode"] = artifact_schema_code

    resp = requests.get(INTERNAL_API_URL, params=params, timeout=10)
    resp.raise_for_status()

    return [
        a["dataArtifactGUID"]
        for a in resp.json()
        if isinstance(a, dict) and "dataArtifactGUID" in a
    ]


@tool
def get_artifact_by_guid(data_artifact_guid: str) -> Dict[str, Any]:
    """Returns FULL artifact JSON by GUID."""
    resp = requests.get(f"{INTERNAL_API_URL}/{data_artifact_guid}", timeout=10)
    resp.raise_for_status()
    return resp.json()


@tool
def extract_change_intent(user_request: str) -> Dict[str, Any]:
    """Extracts structured intent from a natural language request."""
    prompt = f"""
Extract structured intent from the request.

Request:
{user_request}

Return JSON ONLY:
{{
  "caseId": 193066,
  "fieldConcept": "company data region",
  "newValue": "Asia",
  "schemas": ["PDP_STATIC_DATA"]  // or null
}}
"""
    return _model_json_call(prompt, retries=1)


@tool
def locate_change_targets(
    artifact_json: Dict[str, Any],
    requested_field_concept: str,
) -> List[Dict[str, Any]]:
    """Finds existing JSON Pointer paths matching the requested field concept."""
    prompt = f"""
Artifact JSON:
{json.dumps(artifact_json, indent=2)}

Requested field concept:
{requested_field_concept}

Return JSON ONLY:
[
  {{
    "jsonPointer": "/path/to/value",
    "currentValue": "..."
  }}
]
"""
    result = _model_json_call(prompt, retries=1)
    return result if isinstance(result, list) else []


def build_semantic_change_plan(
    case_id: int,
    field_concept: str,
    new_value: str,
    schema_codes: Optional[List[str]],
) -> Dict[str, Any]:
    schema_filters = schema_codes or [None]
    planned_changes = []

    guids = []
    for schema in schema_filters:
        guids.extend(get_artifact_guid.invoke(
            {"case_id": case_id, "artifact_schema_code": schema}
        ))

    for guid in dict.fromkeys(guids):
        artifact = get_artifact_by_guid.invoke(guid)
        targets = locate_change_targets.invoke(
            {"artifact_json": artifact, "requested_field_concept": field_concept}
        )

        for t in targets:
            planned_changes.append(
                {
                    "dataArtifactGUID": guid,
                    "artifactSchemaCode": artifact.get("artifactSchemaCode"),
                    "caseId": artifact.get("caseId"),
                    "jsonPointer": t["jsonPointer"],
                    "oldValue": t["currentValue"],
                    "newValue": new_value,
                }
            )

    return {
        "caseId": case_id,
        "requestedChange": {
            "fieldConcept": field_concept,
            "newValue": new_value,
            "schemasRequested": schema_codes or "ALL",
        },
        "plannedChanges": planned_changes,
        "status": "PLANNED" if planned_changes else "NO_MATCHING_FIELDS_FOUND",
    }

def apply_json_pointer(doc: dict, pointer: str, value: Any) -> dict:
    doc = copy.deepcopy(doc)
    parts = pointer.lstrip("/").split("/")
    current = doc

    for p in parts[:-1]:
        p = p.replace("~1", "/").replace("~0", "~")
        current = current[int(p)] if p.isdigit() else current[p]

    last = parts[-1].replace("~1", "/").replace("~0", "~")
    current[int(last)] if last.isdigit() else current.__setitem__(last, value)
    return doc

def normalize_attributes(attrs: dict) -> dict:
    return {
        k: (v["value"] if isinstance(v, dict) and "value" in v else v)
        for k, v in attrs.items()
    }


def normalize_sections(sections: dict) -> dict:
    normalized = {}
    for section_name, nodes in sections.items():
        normalized[section_name] = [
            {
                "attributes": normalize_attributes(node.get("attributes", {})),
                "isRoot": bool(node.get("isRoot", False)),
                "sections": node.get("sections", {}),
            }
            for node in nodes
        ]
    return normalized


def transform_artifact_to_target_structure(artifact: dict) -> dict:
    return {
        "artifactSchemaCode": artifact.get("artifactSchemaCode"),
        "artifactSchemaCodeConfidence": artifact.get("artifactSchemaCodeConfidence", 100),
        "caseId": artifact.get("caseId"),
        "createdOn": artifact.get("createdOn"),
        "dataArtifactGUID": artifact.get("dataArtifactGUID"),
        "dataArtifactVersionGUID": artifact.get("dataArtifactVersionGUID"),
        "hasManualIntervention": artifact.get("hasManualIntervention", False),
        "keys": artifact.get("keys", []),
        "metadata": artifact.get("metadata", {}),
        "ontologyCode": artifact.get("ontologyCode"),
        "ontologyVersion": artifact.get("ontologyVersion", 1),
        "qcStatus": artifact.get("qcStatus", {}),
        "recycling": artifact.get("recycling", {"isRecycled": False}),
        "sections": normalize_sections(artifact.get("sections", {})),
        "source": artifact.get("source"),
        "status": artifact.get("status"),
        "user": artifact.get("user"),
    }

if __name__ == "__main__":
    user_prompt = (
        "Change the company data region to 'Asia' for caseId 193067 related to CASE schema code."
    )

    intent = extract_change_intent.invoke({"user_request": user_prompt})

    plan = build_semantic_change_plan(
        case_id=intent["caseId"],
        field_concept=intent["fieldConcept"],
        new_value=intent["newValue"],
        schema_codes=intent.get("schemas"),
    )

    results = []

    for change in plan["plannedChanges"]:
        original = get_artifact_by_guid.invoke(change["dataArtifactGUID"])
        modified = apply_json_pointer(
            original, change["jsonPointer"], change["newValue"]
        )
        results.append(transform_artifact_to_target_structure(modified))

    print(json.dumps(results, indent=2))
