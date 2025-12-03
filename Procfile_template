# Aetheron Template Backend — Process Definitions
# -----------------------------------------------
# This Procfile is used for local and platform deployment.
# It reflects only the template backend structure. The full
# production environment may use additional processes.

web: uvicorn Aetheron_template:app --host 0.0.0.0 --port $PORT
worker: celery -A celery_worker_template.celery worker --loglevel=info
