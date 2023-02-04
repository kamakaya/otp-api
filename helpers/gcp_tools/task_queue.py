from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from logging import getLogger
from uuid import uuid4
from typing import Union
import datetime
import json

from helpers.gcp_tools import GCLOUD_PROJECT, GCLOUD_CREDENTIALS, APP_URL, GCLOUD_REGION, GCLOUD_SA_EMAIL
from helpers.general import is_json

logger = getLogger(__name__)


def generate_task_id() -> str:
    return f"TaskID_{uuid4()}"


def generate_tasks_client() -> tasks_v2.CloudTasksClient:
    return tasks_v2.CloudTasksClient(credentials=GCLOUD_CREDENTIALS)


def enqueue_task(payload: Union[str, dict, list], *,
                 queue_name: str,
                 target_url: str,
                 oidc_audience: str = APP_URL,
                 task_id: str = None,
                 client: tasks_v2.CloudTasksClient = None,
                 in_seconds: int = None,
                 project: str = GCLOUD_PROJECT,
                 location: str = GCLOUD_REGION,
                 service_account_email: str = GCLOUD_SA_EMAIL) -> tasks_v2.Task:

    if not task_id:
        task_id = generate_task_id()

    if not client:
        # Create a client.
        client = generate_tasks_client()

    # Construct the incoming_request body.
    task = {
        "http_request": {  # Specify the type of incoming_request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": target_url,  # The full target_url path that the task will be sent to.
            "oidc_token": {
                "service_account_email": service_account_email,
                "audience": oidc_audience
            }
        }
    }
    if payload is not None:
        if isinstance(payload, (dict, list)):
            # Convert dict to JSON string
            payload = json.dumps(payload)

        if is_json(payload):
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json"}

        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the incoming_request.
        task["http_request"]["body"] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp

    parent = client.queue_path(project, location, queue_name)
    if task_id is not None:
        task_name = f"{parent}/tasks/{task_id}"
        
        # Add the name to tasks.
        task["name"] = task_name

    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    return response





