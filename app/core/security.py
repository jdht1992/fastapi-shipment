from http.client import HTTPException
from typing import Annotated
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.utils import decode_access_token

from fastapi import Depends, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")


class AccessTokenBearer(HTTPBearer):
    async def __caller__(self, request):
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials

        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
            )

        return token_data


access_token_bearer = AccessTokenBearer()
Annotated[dict, Depends(access_token_bearer)]
