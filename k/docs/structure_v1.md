# Semantic data fix agent

Processes Excel files to update artifacts. Uses an LLM (Qwen 2.5) to semantically understand field concepts rather than requiring exact JSON paths, making it more user-friendly.

1. api.py - Mock FastAPI service simulating an internal artifacts API
2. main.py - Core agent logic with LangChain tools
3. app.py - Gradio chat interface for user interaction

### Mock API (api.py)

- Provides endpoints to retrieve artifacts by case ID
- Contains sample artifacts with nested sections structure (CLIENT_DATA, COMPANY_DATA)
- Each artifact has metadata like schema codes, regions, and QC status

### Core Agent Logic (main.py)

**Key Tools:**
- ´get_artifact_guid´ - Fetches artifacts GUIDs for a case
- ´get_artifact_by_guid´ - Retrieves full artifact JSON
- ´extract_change_intent´ - Uses LLM to parse natural language requests
- ´locate_change_targets´ - Uses LLM to find JSON paths matching field concepts

**Main Workflow:**
1. Get artifact GUIDs for the case
2. For each artifact, locate fields matching the concept (e.g., "company data region")
3. Generate a change plan with ingestion artifact

**Helper Functions:**
- ´apply_json_pointer´ - Applies changes to JSON using RFC 6901 pointers
- ´normalize_sections´ - Flattens nested attribute structures
- ´transform_artifact_to_target_structure´ - Converts artifacts to ingestion artifact

### Gradio Interface (app.py)

**Process:**
1. User uploads Excel with columns: caseId, whatToChange, newValue, description
2. For each row, builds a semantic change plan
3. Applies changes using JSON pointers
4. Returns ingestion artifact JSON

**Example Excel row:**

- caseId: 193066
- whatToChange: "company data region"
- newValue: "Asia"

The agent would find all "Region" fields in COMPANY_DATA sections and update them to "Asia".