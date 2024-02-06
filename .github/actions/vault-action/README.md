# GitHub Action to Access NR Vault Secrets

# Environment Variables
- `BROKER_JWT` - _Required_ - Token to open intention with the NR Broker
- `VAULT_ENV` - _Required_ - One of: dev/test/prod
- `SECRET_NAME` - _Required_ Name of the secret to be extracted as output

# Example
```sh
name: vault-workflow

on: [push]

jobs:    
  pull:
    name: Import Vault Secrets
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
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

