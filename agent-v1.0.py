import json
from typing import Any, Dict, List

from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from sqlalchemy import false, true


MOCK_ARTIFACTS: List[Dict[str, Any]] = [ { "artifactReference": "pedro-g", "artifactSchemaCode": "CASE", "artifactSchemaCodeConfidence": 100.0, "caseId": 193067, "createdOn": 1765473199, "dataArtifactGUID": "ea743c8b-4da6-4f7e-b3fa-c131d2b3e691", "dataArtifactVersionGUID": "fdcf97ec-ec0e-45e4-8b17-f67cf5147a6d", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": {}, "application": "pedro-g", "date": 1765473199, "user": "jgmarques" }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473199, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "CASE": [ { "attributes": { "externalReference": { "confidence": 100.0, "value": "pedro-g" }, "caseStatus": { "confidence": 100.0, "value": "OPEN" } }, "isRoot": true, "sections": {} } ] }, "source": "pedro-g", "status": "VALID", "user": "jgmarques" }, { "artifactSchemaCode": "PDP_STATIC_DATA", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473622, "dataArtifactGUID": "5d404c90-bf2d-4c20-9acd-ff1bd3d260bf", "dataArtifactVersionGUID": "c6fa6eaa-7786-4ded-a7ae-25eb4a22633e", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": {}, "application": "pedro-g", "date": 1765473622, "user": "jgmarques" }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473622, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "PARTNER_DATA": [ { "attributes": { "PartnerType": { "value": "Individual" }, "Role": { "value": "AH" }, "SourcePartnerRef": { "value": "109812-partner" }, "FirstName": { "value": "Anya" }, "PhoneNumber": { "value": "12345678|12345670|12345671|12345672|12345673|12345674|12345675|12345676|12345677|12345620|12345621|12345622|12345623|12345624|12345625|12345626|12345627|12345628" }, "PrimaryEmail": { "value": "email@kpmg.com" }, "SecondaryEmail": { "value": "email@kpmg.com" }, "LastName": { "value": "Sharma" } }, "isRoot": false, "sections": {} } ], "DOCUMENT": [ { "attributes": { "F2BCaseBusinessID": { "value": "123132" }, "DocumentProducedDate": { "value": "07/02/25" }, "DeltaStatus": { "value": "123" }, "DocumentType": { "value": "Kick-off Letter" }, "OMSDocumentID": { "value": "123" } }, "isRoot": false, "sections": {} } ], "CLIENT_DATA": [ { "attributes": { "OrgUnitCode": { "value": "OTest" }, "MigrationStatusReason": { "value": "Test- Migration" }, "WaveRef": { "value": "WAVE999" }, "RmStaffID": { "value": "10022" }, "RetDispatch": { "value": "Retained Mail" }, "ConstellationRef": { "value": "321313" }, "ClientGrouping": { "value": "Non-Profit Organizations" }, "MigrationStatus": { "value": "Not Scheduled" }, "BR": { "value": "Digital" }, "BookingCenterName": { "value": "CH" }, "LetterCodePrefix": { "value": "CD29" }, "SegmentSubgroup": { "value": "Sub-1" }, "SubWaveFinancialRef": { "value": "coc1234" }, "APID": { "value": "ATest" }, "TargetSegment": { "value": "PB" }, "InopCIF": { "value": "123" }, "SubWaveCSDRef": { "value": "coc123" }, "Status": { "value": "23242432234" }, "Validation": { "value": "Required" }, "CIF": { "value": "CX-183238" }, "DeemedConsentDeadline": { "value": "07/02/25" }, "JourneyType": { "value": "Assisted" }, "RmFirstName": { "value": "Victor" }, "IPDocType": { "value": "IP_IRRELEVANT" }, "DeltaStatus": { "value": "ADD" }, "Sector": { "value": "GWM" }, "CSCustomerOffice": { "value": "Geneva" }, "FIM": { "value": "Management Capital Partners" }, "CIFType": { "value": "IND" }, "MarketTeam": { "value": "Singapore" }, "FreeAssetRatio": { "value": "68" }, "CMJPhase": { "value": "Pipeline and Initiation" }, "HashPID": { "value": "PTest" }, "OutreachStatus": { "value": "Kick-off Letter Sent" }, "DataEntitlementSegment": { "value": "PB" }, "RmLastName": { "value": "Vogel" }, "HasPFA": { "value": "1" }, "Region": { "value": "Europe" }, "RmEmailAddress": { "value": "email@test.com" }, "BookingCenterRef": { "value": "CH" }, "RmGPN": { "value": "20" } }, "isRoot": true, "sections": {} } ], "PORTFOLIO_DATA": [ { "attributes": { "InvestmentHorizon": { "value": "3" }, "VolatilityScore": { "value": "12 %" }, "ServiceType": { "value": "1" }, "RiskTolerance": { "value": "1" }, "PortfolioID": { "value": "108482-300" }, "IhMismatch": { "value": "Y" }, "FarMismatch": { "value": "Y" }, "ReferenceCurrency": { "value": "USD" } }, "isRoot": false, "sections": {} } ] }, "source": "pedro-g", "status": "VALID", "user": "jgmarques" }, { "artifactReference": "pedro-g", "artifactSchemaCode": "CASE", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473631, "dataArtifactGUID": "97c59a68-8d9d-405d-aa0d-35336827f62f", "dataArtifactVersionGUID": "a552454a-0149-471c-9570-64d333df1d9d", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": {}, "application": "kpmg-system", "date": 1765473631 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473631, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "CASE": [ { "attributes": { "externalReference": { "confidence": 100.0, "value": "pedro-g" }, "milestone": { "confidence": 100.0, "value": "ORIGINATION" }, "caseStatus": { "confidence": 100.0, "value": "OPEN" } }, "isRoot": true, "sections": {} } ] }, "source": "kpmg-system", "status": "VALID" }, { "artifactReference": "664104", "artifactSchemaCode": "APPIAN_PROCESS_UPDATE_ACKNOWLEDGEMENT", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473633, "dataArtifactGUID": "aae7ab37-88da-47ea-a617-49e27b22b5cc", "dataArtifactVersionGUID": "767c747b-589a-41a6-8d17-f9bbd832eb0f", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": { "dispatcherIdentifier": "95eecf94-89b3-46db-8bad-3f83609c2365" }, "application": "kyc-task-data-manager", "date": 1765473633 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473633, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "PROCESS_DATA": [ { "attributes": { "CIF": { "value": "CX-183238" }, "ContractingStatus": { "value": "Pending" }, "PreviousRmGPN": { "value": "20" }, "ProcessID": { "value": "78775" }, "ContractingSubStatus": { "value": "Dispatched" } }, "isRoot": false, "sections": {} } ] }, "source": "kyc-task-data-manager", "status": "VALID" }, { "artifactReference": "pedro-g", "artifactSchemaCode": "CASE", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473641, "dataArtifactGUID": "98a2357b-5b9b-4e68-bb11-ea50543e549c", "dataArtifactVersionGUID": "9dbf7272-4616-47b8-9953-d66aa69a2de3", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": {}, "application": "kpmg-system", "date": 1765473641 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473641, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "CASE": [ { "attributes": { "externalReference": { "confidence": 100.0, "value": "pedro-g" }, "milestone": { "confidence": 100.0, "value": "ID_AND_V" }, "caseStatus": { "confidence": 100.0, "value": "OPEN" } }, "isRoot": true, "sections": {} } ] }, "source": "kpmg-system", "status": "VALID" }, { "artifactReference": "193066", "artifactSchemaCode": "WAVE_FINANCIAL_INFORMATION", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473642, "dataArtifactGUID": "c5409c77-6f8a-4db3-b336-33efb5f0cb2e", "dataArtifactVersionGUID": "7ff4f9a5-470f-4820-9cd1-fe69d8bf6f69", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": { "dispatcherIdentifier": "a737fbf3-b047-4027-857b-81e2eddec354" }, "application": "cif-list", "date": 1765473642 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473642, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "WAVE_FINANCIAL_INFORMATION": [ { "attributes": { "SubWaveFinancialRef": { "value": "coc1234" }, "FinancialMigrationDate": { "value": "24/06/25" }, "ReasonCode": { "value": "SWC-001" } }, "isRoot": false, "sections": {} } ] }, "source": "cif-list", "status": "VALID" }, { "artifactReference": "193066", "artifactSchemaCode": "WAVE_STATIC_INFORMATION", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473642, "dataArtifactGUID": "a0bca11f-dab3-4353-9282-0343af330474", "dataArtifactVersionGUID": "6389da80-599d-4390-ab35-fe5fb89270db", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": { "dispatcherIdentifier": "fd50de4a-6eea-46ca-b80e-7c3048fe76f3" }, "application": "cif-list", "date": 1765473642 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473642, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "WAVE_STATIC_INFORMATION": [ { "attributes": { "StaticMigrationDate": { "value": "04/06/25" }, "SubWaveCSDRef": { "value": "coc123" }, "ReasonCode": { "value": "SWC-001" } }, "isRoot": false, "sections": {} } ] }, "source": "cif-list", "status": "VALID" }, { "artifactReference": "664105", "artifactSchemaCode": "CREATE_DOCUMENT_RESPONSE", "artifactSchemaCodeConfidence": 100.0, "caseId": 193066, "createdOn": 1765473642, "dataArtifactGUID": "1f388df0-3d2f-4be2-8a7d-3cc9b064eecd", "dataArtifactVersionGUID": "f08ba25e-101d-4d60-bbd9-b7baca53c66a", "hasManualIntervention": false, "keys": [], "metadata": { "additionalData": { "dispatcherIdentifier": "db8b3820-ec61-49b3-9506-236e94bfa7f5" }, "application": "kyc-task-data-manager", "date": 1765473642 }, "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH", "ontologyVersion": 1, "qcStatus": { "assessedBy": "sph-artifact-quality", "assessedOn": 1765473642, "messageList": [], "status": "PASSED" }, "recycling": { "isRecycled": false }, "sections": { "DATA": [ { "attributes": { "DocumentID": { "value": "123" }, "AppianDocumentID": { "value": "192911" } }, "isRoot": false, "sections": {} } ] }, "source": "kyc-task-data-manager", "status": "VALID" } ] # ← paste your JSON here as a Python list


def resolve_guids_by_schema(case_id: int, artifact_schema_code: str) -> List[str]:
    return [
        a["dataArtifactGUID"]
        for a in MOCK_ARTIFACTS
        if a.get("caseId") == case_id and a.get("artifactSchemaCode") == artifact_schema_code
    ]

def build_artifact_catalog(case_id: int, max_sections_per_artifact: int = 6) -> Dict[str, Any]:
    """
    Returns a compact 'catalog' for the LLM to reason over:
    - which schema codes exist for this case
    - what section names exist inside each schema
    - a tiny preview of attribute keys (optional)
    """
    artifacts = [a for a in MOCK_ARTIFACTS if a.get("caseId") == case_id]

    catalog = []
    for a in artifacts:
        sections = a.get("sections") or {}
        section_names = list(sections.keys())[:max_sections_per_artifact]

        preview_attrs = []
        try:
            if section_names:
                first_section = section_names[0]
                entries = sections.get(first_section) or []
                if entries and isinstance(entries, list):
                    attrs = (entries[0].get("attributes") or {})
                    preview_attrs = list(attrs.keys())[:10]
        except Exception:
            preview_attrs = []

        catalog.append({
            "artifactSchemaCode": a.get("artifactSchemaCode"),
            "source": a.get("source"),
            "sectionNames": section_names,
            "attributeKeyPreview": preview_attrs,
        })

    return {
        "caseId": case_id,
        "artifactsCatalog": catalog
    }

@tool("get_artifact_catalog", description="Get a compact catalog of artifacts for a caseId (schema codes + section names + key preview).")
def get_artifact_catalog(case_id: int) -> Dict[str, Any]:
    return build_artifact_catalog(case_id)

@tool("get_guids_for_schema", description="Get dataArtifactGUID(s) for a caseId and artifactSchemaCode.")
def get_guids_for_schema(case_id: int, artifact_schema_code: str) -> List[str]:
    return resolve_guids_by_schema(case_id, artifact_schema_code)

llm = ChatOllama(model="qwen2.5:7b-instruct", temperature=0.0)
llm_with_tools = llm.bind_tools([get_artifact_catalog, get_guids_for_schema])

system = SystemMessage(content="""
You are a data-fix assistant.

Goal:
- The user will describe an artifact in natural language (e.g., "static data").
- You MUST identify the best matching artifactSchemaCode for the given case by inspecting the live artifact catalog.

Rules:
- Never invent schema codes.
- Only choose artifactSchemaCode values that appear in the catalog returned by get_artifact_catalog.
- If multiple candidates exist, return the best one with a confidence score and brief rationale.
- After selecting the schema code, call get_guids_for_schema to retrieve GUID(s).
- Final output MUST be JSON only.

Final JSON schema:
{
  "caseId": number,
  "userIntent": string,
  "selectedArtifactSchemaCode": string,
  "confidence": number,   // 0.0 to 1.0
  "rationale": string,
  "dataArtifactGUIDs": [string]
}
""")

def run_query(user_text: str) -> str:
    """
    Runs a single user request end-to-end:
    - LLM calls get_artifact_catalog(caseId)
    - LLM selects schema code based on natural language
    - LLM calls get_guids_for_schema
    - returns final JSON
    """
    messages = [
        system,
        HumanMessage(content=user_text),
    ]

    first = llm_with_tools.invoke(messages)

    if not first.tool_calls:
        raise RuntimeError(f"Model did not call tools. Output: {first.content}")

    messages.append(first)

    while True:
        for tc in messages[-1].tool_calls:
            name = tc["name"]
            args = tc["args"]

            if name == "get_artifact_catalog":
                out = get_artifact_catalog.invoke(args)
            elif name == "get_guids_for_schema":
                out = get_guids_for_schema.invoke(args)
            else:
                raise RuntimeError(f"Unexpected tool: {name}")

            messages.append(
                ToolMessage(
                    tool_call_id=tc["id"],
                    content=json.dumps(out)
                )
            )

        nxt = llm_with_tools.invoke(messages)

        if not nxt.tool_calls:
            return nxt.content

        messages.append(nxt)


if __name__ == "__main__":
    print(run_query("Get the artifact GUID for caseId 193066 where the schema code is related to pdp static data."))