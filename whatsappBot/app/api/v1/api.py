from fastapi import APIRouter

from .endpoints import whatsapp, menu, orders

api_router = APIRouter()

api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])