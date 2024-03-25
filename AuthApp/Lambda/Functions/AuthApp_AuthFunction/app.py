import boto3
import json
import os

# Replace these values with your actual Cognito pool ID, client ID, and region
user_pool_id = os.environ['UserpoolID']
client_id = os.environ['ClientsID']


# Initialize the Cognito Identity Provider client
client = None

def initiate_auth(email, password):
    try:
        # Authenticate the user and get the authentication token
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
            ClientMetadata={
                'username': email,
                'password': password
            }
        )
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return response, None

def refresh_auth(email, refresh_token):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            },
            ClientMetadata={
            })
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None

def lambda_handler(event, context):
    global client
    if client is None:
        client = boto3.client('cognito-idp')
    email = event['email']
    resp = None  # Initialize resp outside the conditional blocks
    if 'password' in event:
        resp, msg = initiate_auth(email, event['password'])

    if 'refresh_token' in event:
        resp, msg = refresh_auth(email, event['refresh_token'])
    if msg is not None:
        return {
            'status': 'fail',
            'msg': msg
        }

    response = {
        'status': 'success',
        'id_token': resp['AuthenticationResult']['IdToken']
        # 'access_token': resp['AuthenticationResult']['AccessToken']
    }

    if 'password' in event:
        response['refresh_token'] = resp['AuthenticationResult']['RefreshToken']

    return response
