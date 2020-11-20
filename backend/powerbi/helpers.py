import msal
import json,os,urllib,itertools
import requests
from django.conf import settings


def getaccesstoken():
    '''Returns AAD token using MSAL'''

    response = None
    try:
        authMode = settings.PBI_AUTHENTICATION_MODE.lower()
        clientId = settings.PBI_CLIENT_ID
        authorityUrl = settings.PBI_AUTHORITY_URL
        scope = settings.PBI_SCOPE

        if authMode == 'masteruser':

            masterUserName = settings.PBI_MASTER_USER
            masterUserPass = settings.PBI_MASTER_PASS
            
            # Create a public client to authorize the app with the AAD app
            clientapp = msal.PublicClientApplication(clientId, authority=authorityUrl)
            accounts = clientapp.get_accounts(username=masterUserName)
            if accounts:
                
                # Retrieve Access token from cache if available
                response = clientapp.acquire_token_silent(scope, account=accounts[0])
            if not response:
                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_by_username_password(masterUserName, masterUserPass, scopes=scope)     
        elif authMode == 'serviceprincipal':

            clientSecret = settings.PBI_CLIENT_SECRET

            clientapp = msal.ConfidentialClientApplication(clientId, client_credential=clientSecret, authority=authorityUrl)
            
            # Retrieve Access token from cache if available
            response = clientapp.acquire_token_silent(scopes=scope, account=None)
            if not response:
                
                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=scope)
        try:
            return response['access_token']
        except KeyError:
            raise Exception(response['error_description'])

    except Exception as ex:
        raise Exception('Error retrieving Access token\n' + str(ex))

def getembedparam(accesstoken, workspaceId, reportId):
    '''Returns Embed token and Embed URL'''

    try:
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + accesstoken}

        reporturl = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspaceId + '/reports/' + reportId
        
        apiresponse = None

        try:
            apiresponse = requests.get(reporturl, headers=headers)
            #if app.debug:
                #print('Embed URL Request ID: ', apiresponse.headers.get('RequestId'))
        except Exception as ex:
            raise Exception('Error while retrieving report Embed URL\n')

        if not apiresponse:
            raise Exception('Error while retrieving report Embed URL\n' + apiresponse.reason + '\nRequestId: ' + apiresponse.headers.get('RequestId'))

        try:
            apiresponse = json.loads(apiresponse.text)
            embedurl = apiresponse['embedUrl']
            datasetId = apiresponse['datasetId']
        except Exception as ex:
            raise Exception('Error while extracting Embed URL from API response\n' + apiresponse.text)
            
        # Get embed token
        embedtokenurl = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        body = {'datasets': []}
        if datasetId != '':
            body['datasets'].append({'id': datasetId})

        if reportId != '':
            body['reports'] = []
            body['reports'].append({'id': reportId})

        if workspaceId != '':
            body['targetWorkspaces'] = []
            body['targetWorkspaces'].append({'id': workspaceId})

        apiresponse = None
        
        try:
            
            # Generate Embed token for multiple workspaces, datasets, and reports. Refer https://aka.ms/MultiResourceEmbedToken
            apiresponse = requests.post(embedtokenurl, data=json.dumps(body), headers=headers)
            # if app.debug:
            #     print('Embed token Request ID: ', apiresponse.headers.get('RequestId'))
        except:
            raise Exception('Error while invoking Embed token REST API endpoint\n')
        
        if not apiresponse:
            raise Exception('Error while retrieving report Embed URL\n' + apiresponse.reason + '\nRequestId: ' + apiresponse.headers.get('RequestId'))

        try:
            apiresponse = json.loads(apiresponse.text)
            embedtoken = apiresponse['token']
            embedtokenid = apiresponse['tokenId']
            tokenexpiry = apiresponse['expiration']
            # if app.debug:
            #     print('Embed token Expires on: ', tokenexpiry)
            #     print('Embed Token ID: ', embedtokenid)
        except Exception as ex:
            raise Exception('Error while extracting Embed token from API response\n' + apiresponse.reason)

        response = {'accessToken': embedtoken, 'embedUrl': embedurl, 'tokenExpiry': tokenexpiry}
        return response
    except Exception as ex:
        return {'errorMsg': str(ex)}