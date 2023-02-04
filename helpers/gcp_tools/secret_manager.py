from google.cloud.secretmanager import SecretManagerServiceClient
import logging
import json
from pathlib import Path
from helpers.gcp_tools import GCLOUD_CREDENTIALS, GCP_PROJECT_ID

logger = logging.getLogger(__name__)


def generate_secret_manager_client():
    return SecretManagerServiceClient(credentials=GCLOUD_CREDENTIALS)


def access_secret_version(secret_name: str,
                          gcp_project_id: str = GCP_PROJECT_ID,
                          version_id: str = 'latest',
                          client: SecretManagerServiceClient = None,
                          download_path: Path = None) -> str:
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    if not client:
        # Create the Secret Manager client.
        client = SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{gcp_project_id}/secrets/{secret_name}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")

    if download_path:
        with open(download_path, 'w+') as f:
            f.write(payload)
        logger.info(f"{download_path} downloaded successfully")

    try:
        return json.loads(payload)
    except json.decoder.JSONDecodeError:
        return payload
