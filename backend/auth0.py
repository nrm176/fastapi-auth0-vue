import requests
from jose import jwt
from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request
import enum
import os

auth_config = {
    'domain': os.environ.get('DOMAIN'),
    'audience': os.environ.get('AUDIENCE'),
    'algorithms': ["RS256"]
}


class Permission(enum.Enum):
    READ_API = 'read:api'
    ME = 'me'
    ALL = 'read:api,me'


class JWTBearer():
    def __init__(self, auth_config, permission: Permission, verify_exp=True):
        self.auth_config = auth_config
        self.permission = permission
        self.verify_exp = verify_exp

    def get_jwk_from_auth0API(self):
        """
        Fetch JWK(public key) from Auth0 API
        :return:
            String: jwks
        """
        json_url = f"https://{self.auth_config['domain']}/.well-known/jwks.json"
        jwks = requests.get(json_url).json()
        return jwks

    def get_token_from_client(self, request: Request):
        """
        Get authorization from a request from the frontend
        :param request:
        :return:
            String: token
        """
        auth = request.headers.get("authorization", None)
        _, token = auth.split()
        return token

    def check_permissions(self, token):
        """
        Confirm permission
        :param token:
        :return:
            Boolean: True if a permission exists
        """
        permissions = jwt.get_unverified_claims(token)['permissions']
        if self.permission.value in permissions:
            return True
        else:
            return False

    async def __call__(self, request: Request):
        jwks = self.get_jwk_from_auth0API()
        token = self.get_token_from_client(request)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.auth_config['algorithms'],
                    audience=self.auth_config['audience'],
                    issuer="https://" + self.auth_config['domain'] + "/",
                    options={'verify_exp': self.verify_exp}
                )
                if self.permission:
                    if self.check_permissions(token) is False:
                        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")
            except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")
            return payload
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK invalid")