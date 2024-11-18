import asyncio

from fastapi import APIRouter
from lnbits.db import Database
from loguru import logger

from .tasks import wait_for_paid_invoices
from .views import ai-proxy_ext_generic
from .views_api import ai-proxy_ext_api

db = Database("ext_ai-proxy")

scheduled_tasks: list[asyncio.Task] = []

ai-proxy_ext: APIRouter = APIRouter(prefix="/ai-proxy", tags=["ai-proxy"])
ai-proxy_ext.include_router(ai-proxy_ext_generic)
ai-proxy_ext.include_router(ai-proxy_ext_api)

ai-proxy_static_files = [
    {
        "path": "/ai-proxy/static",
        "name": "ai-proxy_static",
    }
]


def ai-proxy_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def ai-proxy_start():
    from lnbits.tasks import create_permanent_unique_task

    task = create_permanent_unique_task("ext_testing", wait_for_paid_invoices)
    scheduled_tasks.append(task)
