import json
from jose import jwt
from fastapi import HTTPException
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = '<YOUR AUTH0 DOMAIN>'
API_AUDIENCE = '<YOUR AUTH0 API IDENTIFIER>'
ALGORITHMS = ['RS256']

class Auth():
    def verify_jwt_token(self, token: str):
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
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
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token is expired")
            except jwt.JWTClaimsError:
                raise HTTPException(status_code=401, detail="incorrect claims,"
                                    "please check the audience and issuer")
            except Exception:
                raise HTTPException(status_code=401, detail="Unable to parse"
                                    " authentication token.")
        return payload

    def requires_scope(self, required_scope, token):
        """Determines if the required scope is present in the Access Token
        Args:
            required_scope (str): The scope required to access the resource
        """
        unverified_claims = jwt.get_unverified_claims(token)
        if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
        return False
