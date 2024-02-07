# nr-vault-patterns

This repository contains Vault patterns intended for use within the NR Data Analytics Platform (DAP). Contents of the repository: 
* Docker container to automate interaction with the NR Broker and NR Vault API
* Custom GitHub Action to access Vault secrets (using the aforementioned Docker container)

## Environment Variables
- `BROKER_JWT` - _Required_ - Token to open intention with the NR Broker
- `VAULT_ENV` - _Required_ - One of: dev/test/prod
- `SECRET_NAME` - _Required_ Name of the secret to be extracted as output

## Usage Examples

1. Use Vault secrets in an Airflow DAG. Example: 
```sh
from airflow import DAG
from pendulum import datetime
from kubernetes import client
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.secret import Secret

vault_jwt = Secret("env", None, "nr-vault-jwt")

with DAG(
    start_date=datetime(2023, 11, 23),
    catchup=False,
    schedule=None,
    dag_id="vault_example",
) as dag:
    vault_action = KubernetesPodOperator(
        task_id="get_ods_host",
        image="ghcr.io/bcgov/nr-vault-patterns:main",
        in_cluster=True,
        namespace="a1b9b0-dev",
        name="get_ods_host",
        random_name_suffix=True,
        labels={"DataClass": "High", "Release": "test-release-af"},  # network policies
        reattach_on_restart=True,
        is_delete_operator_pod=True,
        get_logs=True,
        log_events_on_failure=True,
        secrets=[vault_jwt],
        container_resources= client.V1ResourceRequirements(
        requests={"cpu": "10m", "memory": "256Mi"},
        limits={"cpu": "50m", "memory": "500Mi"})
    )
```

2. Use Vault secrets in a GitHub Actions workflow. Example: 
```sh
name: vault-workflow

on: [push]

jobs:    
  pull:
    name: Import Vault Secrets
    runs-on: ubuntu-22.04
    steps:
      - name: NR Vault Pattern 
        id: nr-vault-patterns
        uses: bcgov/nr-vault-patterns@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          BROKER_JWT: ${{ secrets.BROKER_JWT }}
          VAULT_ENV = 'dev'
          SECRET_NAME = 'ods-dev'
```

##  Use of GHCR
The container image is built and pushed to the GHCR any time there is a push or PR to the **main** branch. Images are named according to the file path and tagged with the branch name.
```sh
docker pull ghcr.io/bcgov/nr-vault-patterns:main
```

## API Workflow 

This Vault pattern is based on the following API steps: 

1. NR Broker - POST /v1/intention/open 

2. NR Broker - POST /v1/provision/token/self

3. NR Vault - POST /v1/sys/wrapping/unwrap

4. NR Vault - GET /v1/apps/data/dev/nr-data-solutions/nr-data-analytics-platform/
