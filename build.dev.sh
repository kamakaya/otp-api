export GCP_PROJECT=one-time-password-via-api

gcloud config set project $GCP_PROJECT
gcloud builds submit --config cloudbuild.dev.yaml