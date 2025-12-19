from aiogram import Router
from message import admin, reports, user

router = Router()
router.include_router(admin.router)
router.include_router(reports.router)   
router.include_router(user.router)