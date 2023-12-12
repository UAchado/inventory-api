import os
import requests

from jose import jwt, JWTError
from fastapi import HTTPException, Request, status

def verify_access(request: Request):
    
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "ERROR: Authorization header missing")
    try:
        token = authorization.split(" ")[1]
        issuer = os.getenv('COGNITO_ISSUER')
        audience = os.getenv('COGNITO_AUDIENCE')
        response = requests.get(f"{issuer}/.well-known/jwks.json")
        jwks = response.json()["keys"]
        decoded_token = jwt.decode(token, jwks, algorithms=["RS256"],
                                   audience = audience, issuer = issuer)
        return decoded_token
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "ERROR: Invalid Access token")
    except Exception:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "ERROR: Error authenticating")