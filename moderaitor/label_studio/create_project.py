from datetime import datetime, timedelta
import os
import time

from label_studio_sdk import Client

# SECRETS_PATH = os.getenv("SECRETS_PATH", "/run/secrets/")

# def _get_id():
#     with open(f"{SECRETS_PATH}AWS_ACCESS_KEY_ID", "r") as f_hdl:
#         return f_hdl.read().strip()

# def _get_secret():
#     with open(f"{SECRETS_PATH}AWS_SECRET_ACCESS_KEY", "r") as f_hdl:
#         return f_hdl.read().strip()

# os.environ['AWS_ACCESS_KEY_ID'] = _get_id()
# os.environ['AWS_SECRET_ACCESS_KEY'] = _get_secret()

API_KEY = os.getenv('LABEL_STUDIO_USER_TOKEN')

LABEL_STUDIO_URL = 'http://label-studio:8080'

MAX_RETRY_DURATION = timedelta(seconds=60)
RETRY_INTERVAL = 2

def start_client(timeout: timedelta):
    start_time = datetime.now()
    end_time = start_time + timeout

    while datetime.now() < end_time:
        try:
            ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
            response = ls.check_connection()
            print(response)
            return ls
        except Exception as e:
            print(f"Failed to start client: {str(e)}")
            time.sleep(RETRY_INTERVAL)

    raise TimeoutError("Timeout reached while starting client")

def main():
    client = start_client(timeout=MAX_RETRY_DURATION)

    with open(
        "./moderaitor/label_studio/project_config/label_interface.txt",
        "r"
    ) as f_hdl:
        label_config = f_hdl.read()

    project = client.start_project(
        title='Comment moderation project',
        label_config=label_config,
    )

    response = project.connect_s3_import_storage(
        bucket="quarantined-comments",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        use_blob_urls=False
    )
    import_storage_id = response['id']

    response = project.connect_s3_export_storage(
        bucket="annotated-comments",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )

    project.sync_storage('s3', import_storage_id)

if __name__ == "__main__":
    main()
