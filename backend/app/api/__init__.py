from fastapi import APIRouter
from .routers import router as main_router

router = APIRouter()
router.include_router(main_router, prefix="", tags=["Main"])
