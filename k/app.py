import json
import pandas as pd
import gradio as gr

from k.main1 import (
    build_semantic_change_plan,
    get_artifact_by_guid,
    apply_json_pointer,
    transform_artifact_to_target_structure
)


async def process_excel(message, history):

    # message format:
    # { "text": "...", "files": ["path1", "path2"] }

    if isinstance(message, dict) and "files" in message and len(message["files"]) > 0:
        file_path = message["files"][0]
    else:
        return "Please upload an Excel file (.xlsx)."

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return f"Could not read Excel file: {e}"

    required = {"caseId", "whatToChange", "newValue"}
    missing = required - set(df.columns)

    if missing:
        return f"Missing required columns in Excel: {missing}"

    results = []

    for _, row in df.iterrows():
        case_id = int(row["caseId"])
        field_concept = str(row["whatToChange"])
        new_value = row["newValue"]
        description = row.get("description", "")

        plan = build_semantic_change_plan(
            case_id=case_id,
            field_concept=field_concept,
            new_value=new_value,
            schema_codes=None,
        )

        for change in plan["plannedChanges"]:
            original = get_artifact_by_guid.invoke(change["dataArtifactGUID"])
            modified = apply_json_pointer(
                original, change["jsonPointer"], change["newValue"]
            )

            transformed = transform_artifact_to_target_structure(modified)

            if description:
                transformed["changeDescription"] = description

            results.append(transformed)

    return (
        "Finished processing your file.\n\n"
        "Here is the resulting JSON:\n\n"
        f"```json\n{json.dumps(results, indent=2)}\n```"
    )



chatbot = gr.ChatInterface(
    fn=process_excel,
    title="🧠 Data Fix Agent — Chat Mode",
    description=(
        "Upload an Excel file with columns: "
        "`caseId`, `whatToChange`, `newValue`, `description (optional)`.\n\n"
        "I will analyze it, plan the changes, and return normalized artifacts."
    ),
    multimodal=True   # still allows file uploads in the chat
)

if __name__ == "__main__":
    chatbot.launch()
