import os
import requests
import json

def main(broker_url, broker_jwt, vault_url, vault_env, secret_name):
    try:
        # Load intention JSON from file
        with open('/usr/bin/intention.json', 'r') as file:
            intention = json.load(file)
        
        # Post intention JSON
        intention_json = requests.post(
            f"{broker_url}/v1/intention/open",
            headers={"Authorization": f'Bearer {broker_jwt}'}, 
            json=intention
        ).json()

        # Extract action token
        action_token = intention_json.get("actions", {}).get("dap-data-sync", {}).get("token")

        # Get wrapped token
        wrapped_vault_token_json = requests.post(
            f"{broker_url}/v1/provision/token/self",
            headers={"X-Broker-Token": action_token}
        ).json()

        # Extract wrapped token
        wrapped_vault_token = wrapped_vault_token_json.get("wrap_info", {}).get("token")

        # Unwrap vault token
        vault_token_json = requests.post(
            f"{vault_url}/v1/sys/wrapping/unwrap",
            headers={"X-Vault-Token": wrapped_vault_token}
        ).json()

        # Extract action token
        vault_token = vault_token_json.get("auth", {}).get("client_token")

        # Get JSON secret 
        secret_json = requests.get(
            f"{vault_url}/v1/apps/data/{vault_env}/nr-data-solutions/nr-data-analytics-platform/{secret_name}",
            headers={"X-Vault-Token": vault_token}
        ).json()
        
        return secret_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Fetch environment variables
    broker_url = os.environ.get("BROKER_URL")
    broker_jwt = os.environ.get("BROKER_JWT")
    vault_url = os.environ.get("VAULT_URL")
    vault_env = os.environ.get("VAULT_ENV")
    secret_name = os.environ.get("SECRET_NAME")

    secret_json = main(broker_url, broker_jwt, vault_url, vault_env, secret_name)

    if secret_json:
        print(secret_json)
    else:
        print("Failed to retrieve secret")
