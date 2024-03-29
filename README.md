# nr-vault-patterns

This repository contains Vault patterns intended for use within the NR Data Analytics Platform (DAP). Contents of the repository:
* Docker container to automate interaction with the NR Broker and NR Vault API
* Custom GitHub Action to access Vault secrets (using the aforementioned Docker container)

## Environment Variables
- `BROKER_JWT` - _Required_ - Token to open intention with the NR Broker
- `VAULT_ENV` - _Required_ - One of: dev/test/prod
- `SECRET_NAME` - _Required_ Name of the secret to be extracted as output

## Usage Example
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

1. NR Broker - Open Intention

2. NR Broker - Provision Token

3. NR Vault - Unwrap Token

4. NR Vault - Get secret
