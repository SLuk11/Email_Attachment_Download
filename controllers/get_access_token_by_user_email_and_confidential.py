import msal
import logger as log

def generate_access_token(tenant_id, client_id, client_secret, scope):
    try:
        authority = 'https://login.microsoftonline.com/' + tenant_id
        app = msal.ConfidentialClientApplication(client_id, authority=authority
                                                 , client_credential=client_secret)
        token_response = app.acquire_token_for_client(scopes=scope)
        acc_tk = token_response['access_token']

        return acc_tk
    except Exception as e:
        log.write_log('Generate_access_token: {}'.format(e.args[0]))
        return None

def get_access_token(tenant_id, client_id, client_secret, scope):
    access_token = generate_access_token(tenant_id, client_id, client_secret, scope)
    # Create headers for request stmt
    headers = {
        "Authorization": f"Bearer {access_token}",
        "ContentType": "application/json"
    }
    return access_token, headers
