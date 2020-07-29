import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# define and assign API_AUDIENCE and AUTH0_DOMAIN and ALGORITHMS
AUTH0_DOMAIN = 'tonycookey.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeapp'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    # get authorization header from request
    auth_header = request.headers.get('Authorization', None)
    # check if authoroization header exists
    if not auth_header:
        # raise auth error sice the authorization header is not present
        raise AuthError({
            'description': 'The Authorization header is not present.',
            'code': 'authorization_header_missing'
        }, 401)
    # split auth header into the bearer and token
    split_auth_header = auth_header.split()
    # check if the header sent is a bearer token
    if split_auth_header[0].lower() != 'bearer':
        # raise auth error since the authorization header is not a bearer token
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The Authorization header must start with "Bearer".'
        }, 401)
    # Check if the split_auth_header array contains two items (bearer string
    # and token)
    elif len(split_auth_header) == 1:
        # if split_auth_header contain only 1 item ,raise auth error
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    # raise error if the split_auth_header contains more than two items, which
    # is invald and incorrect
    elif len(split_auth_header) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The Authorization header must be a bearer token.'
        }, 401)

    # pass the second item in the split_auth_header array/dict whih is the
    # access token fron Auth0
    token = split_auth_header[1]
    return token


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string
    is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    # check if any permissions exist on the payload
    if 'permissions' not in payload:
        # raise error since no permissions exist on the payload
        raise AuthError({
            'code': 'invalid per',
            'description': 'There are no Permssion not inlcuded in this payload'
        }, 401)
    # check if the permission sent is in the payload
    if permission not in payload['permissions']:
        # raise error since there are no permissions in the permissions
        # array/dict
        raise AuthError({
            'code': 'unauthorized',
            'description': "You currently do not have permission to access this"
        }, 401)


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
     https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # verify token using the jwt library
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # check if key id exists in auth token
    if 'kid' not in unverified_header:
        # raise error if key id is not in header
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # iterate through keys to get particular keys
    for key in jwks['keys']:
        # check if the kid exists and is valid
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kid': key['kid'],
                'kty': key['kty'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # check if RSA Key exists
    if rsa_key:
        # decode the jwt token and extract needed fields
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload
        # raise errors if expired token
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)
        # raise error if claims is invalid
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        # raise error if error occured or functio could not parse
        # authentication token
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    # raise auth error if rsa_key does not exist or is null
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get  token from token header
            token = get_token_auth_header()
            # verify ad ecode jwt token
            payload = verify_decode_jwt(token)
            # check for permissions on the payload
            check_permissions(permission, payload)
            # return payload and decorator arguments
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
