from http import HTTPStatus

import httpx
from fastapi import APIRouter, Depends, HTTPException
from lnbits.decorators import require_invoice_key

from .models import Example

# views_api.py is for you API endpoints that could be hit by another service

ai-proxy_ext_api = APIRouter(
    prefix="/api/v1",
    tags=["ai-proxy"],
)


@ai-proxy_ext_api.get("/test/{ai-proxy_data}", description="Example API endpoint")
async def api_ai-proxy(ai-proxy_data: str) -> Example:
    if ai-proxy_data != "00000000":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid ai-proxy data",
        )
    # Do some python things and return the data
    return Example(id="2", wallet=ai-proxy_data)


@ai-proxy_ext_api.get(
    "/vetted",
    description="Get the vetted extension readme",
    dependencies=[Depends(require_invoice_key)],
)
async def api_get_vetted():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://raw.githubusercontent.com/lnbits/lnbits-extensions/main/README.md"
        )
        return resp.text
