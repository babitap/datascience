import jwt, requests, base64

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__('Invalid authorization token: ' + details)

def get_headers(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken('missing headers')
    return headers

def get_kid(token):
    headers = get_headers(token)
    try:
        return headers['kid']
    except KeyError:
        raise InvalidAuthorizationToken('missing kid')

def get_jwks(tenant_name,policy_name):
    #Get uri
    #------------
    url='https://'+tenant_name+'.b2clogin.com/'+tenant_name+'.onmicrosoft.com/'+policy_name
    url+='/v2.0/.well-known/openid-configuration'
    #------------
    #url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration'
    #------------
    res = requests.get(url)
    jwk_uri = res.json()['jwks_uri']
    #Get jwks
    res = requests.get(jwk_uri)
    return res.json()    

def match_jwk(kid,jwks):
    #Search jwks
    for jwk in jwks.get('keys'):
        if jwk.get('kid') == kid:
            return jwk
    raise InvalidAuthorizationToken('kid not recognized')

def rsa_pem_from_jwk(jwk):
    #Helper functions
    def ensure_bytes(key):
        if isinstance(key, str): key = key.encode('utf-8')
        return key
    def decode_value(val):
        decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b'==')
        return int.from_bytes(decoded, 'big')
    
    #Return public key
    return RSAPublicNumbers(
        n=decode_value(jwk['n']),
        e=decode_value(jwk['e'])
    ).public_key(default_backend()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def get_public_key(token,tenant_name,policy_name):
    #Get kid for token
    kid=get_kid(token)
    #print('From token header >>>>',kid)
    
    #Get jwks for tenant/polict
    jwks=get_jwks(tenant_name,policy_name)
    
    #Get matching kid to token
    jwk=match_jwk(kid,jwks)
    #print('From jwk >>>>',jwk)
    
    #Return public key cert
    return rsa_pem_from_jwk(jwk)

def validate_jwt(token,tenant_name,policy_name,valid_audiences):

    #Get public key
    public_key = get_public_key(token,tenant_name,policy_name)
    #print(public_key)
    
    #Decode token
    decoded_token = jwt.decode(token,
                         public_key,
                         verify=True,
                         algorithms=['RS256'],
                         audience=valid_audiences
                        )

        
        
    return decoded_token
