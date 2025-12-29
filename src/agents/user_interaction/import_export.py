import os
import requests
from google.adk.agents import Agent
from google.adk.artifacts import GcsArtifactService
from google.adk.tools import google_search

# 1. Initialize Production Artifact Service for "Any Size" files
# Set this via environment variable: export ARTIFACT_SERVICE_URI="gs://your-bucket-name"
artifact_service = GcsArtifactService(bucket_name=os.getenv("ARTIFACT_SERVICE_URI"))

# 2. Tool to IMPORT from any location (URL or local path)
def import_any_file(source_location: str, alias: str) -> str:
    """Imports a file of any size from a link or local path into the agent's cloud storage."""
    try:
        if source_location.startswith(("http://", "https://")):
            # Stream large files directly to avoid RAM issues
            with requests.get(source_location, stream=True) as r:
                r.raise_for_status()
                # ADK 2025 save_artifact handles the stream to GCS
                artifact_service.save_artifact(r.raw, alias)
        else:
            # Import from local machine path
            artifact_service.save_artifact(source_location, alias)
        
        return f"Successfully imported '{alias}' to secure cloud artifacts."
    except Exception as e:
        return f"Import failed: {str(e)}"

# 3. Tool to EXPORT to any location (Link/Cloud or Local)
def export_any_file(alias: str, destination_path: str) -> str:
    """Exports an artifact to a local folder or a cloud destination."""
    try:
        artifact_service.load_artifact(alias, destination_path)
        return f"Exported '{alias}' to {os.path.abspath(destination_path)}"
    except Exception as e:
        return f"Export failed: {str(e)}"

# 4. Agent Definition
file_manager_agent = Agent(
    name="Universal_Data_Agent",
    model="gemini-2.5-flash-lite", # Best 2025 model for fast multimodal routing
    instruction=(
        "You are a file logistics expert. You can handle files of ANY size. "
        "When a user provides a link or path to 'import', use 'import_any_file'. "
        "When they ask to 'save', 'download', or 'export' to a location, use 'export_any_file'. "
        "You have access to Google Search to find external links if the user doesn't provide one."
    ),
    tools=[import_any_file, export_any_file, google_search],
    artifact_service=artifact_service
)

# Example interaction:
# Prompt: "Import the 10GB dataset from https://example.com/big_data.csv as 'main_data'"
# Follow-up: "Now export 'main_data' to C:/Users/Admin/Desktop/report.csv"
