from fastapi import FastAPI, Query, Path, HTTPException
from typing import Any, Dict, List, Optional

app = FastAPI(title="Internal Artifacts Service (Mock)")

MOCK_ARTIFACTS: List[Dict[str, Any]] = [
    {
        "artifactReference": "pedro-g",
        "artifactSchemaCode": "CASE",
        "artifactSchemaCodeConfidence": 100.0,
        "caseId": 193066,
        "createdOn": 1765473199,
        "dataArtifactGUID": "ea743c8b-4da6-4f7e-b3fa-c131d2b3e691",
        "dataArtifactVersionGUID": "fdcf97ec-ec0e-45e4-8b17-f67cf5147a6d",
        "hasManualIntervention": False,
        "keys": [],
        "metadata": {
            "additionalData": {},
            "application": "pedro-g",
            "date": 1765473199,
            "user": "jgmarques",
        },
        "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH",
        "ontologyVersion": 1,
        "qcStatus": {
            "assessedBy": "sph-artifact-quality",
            "assessedOn": 1765473199,
            "messageList": [],
            "status": "PASSED",
        },
        "recycling": {"isRecycled": False},
        "sections": {
            "CLIENT_DATA": [
                {
                    "attributes": {
                        "Region": {
                            "value": "Europe"
                        }
                    },
                    "isRoot": True,
                    "sections": {}
                }
            ],
            "COMPANY_DATA": [
                {
                    "attributes": {
                        "Region": {
                            "value": "Americas"
                        }
                    },
                    "isRoot": True,
                    "sections": {}
                }
            ]

        },
        "source": "pedro-g",
        "status": "VALID",
        "user": "jgmarques",
    },
    {
        "artifactReference": "pedro-g",
        "artifactSchemaCode": "PDP_STATIC_DATA",
        "artifactSchemaCodeConfidence": 100.0,
        "caseId": 193066,
        "createdOn": 1765473199,
        "dataArtifactGUID": "5d404c90-bf2d-4c20-9acd-ff1bd3d260bf",
        "dataArtifactVersionGUID": "fdcf97ec-ec0e-45e4-8b17-f67cf5147a6d",
        "hasManualIntervention": False,
        "keys": [],
        "metadata": {
            "additionalData": {},
            "application": "pedro-g",
            "date": 1765473199,
            "user": "jgmarques",
        },
        "ontologyCode": "FACTORY_CLIENT_MIGRATION_BCCH",
        "ontologyVersion": 1,
        "qcStatus": {
            "assessedBy": "sph-artifact-quality",
            "assessedOn": 1765473199,
            "messageList": [],
            "status": "PASSED",
        },
        "recycling": {"isRecycled": False},
        "sections": {
            "CLIENT_DATA": [
                {
                    "attributes": {
                        "Region": {
                            "value": "Europe"
                        }
                    },
                    "isRoot": True,
                    "sections": {}
                }
            ],
            "COMPANY_DATA": [
                {
                    "attributes": {
                        "Region": {
                            "value": "Americas"
                        }
                    },
                    "isRoot": True,
                    "sections": {}
                }
            ]

        },
        "source": "pedro-g",
        "status": "VALID",
        "user": "jgmarques",
    },
]



@app.get("/artifacts", response_model=List[dict])
def get_artifacts(
    caseId: int = Query(..., alias="case-id"),
    artifactSchemaCode: Optional[str] = None,
):
    """
    Mimics the internal artifacts service.
    Returns FULL artifact JSON.
    """
    return [
        artifact
        for artifact in MOCK_ARTIFACTS
        if artifact.get("caseId") == caseId
        and (
            artifactSchemaCode is None
            or artifact.get("artifactSchemaCode") == artifactSchemaCode
        )
    ]

@app.get("/artifacts/{dataArtifactGUID}", response_model=dict)
def get_artifact_by_guid(
    dataArtifactGUID: str = Path(..., description="Artifact GUID"),
):
    """
    Mimics:
    GET /artifacts/{dataArtifactGUID}

    Returns the FULL artifact JSON for a single artifact.
    """
    for artifact in MOCK_ARTIFACTS:
        if artifact.get("dataArtifactGUID") == dataArtifactGUID:
            return artifact

    raise HTTPException(
        status_code=404,
        detail=f"Artifact with GUID {dataArtifactGUID} not found",
    )