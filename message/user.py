from aiogram import Router, F, Bot
from aiogram.types import Message
from config import ADMINS
from models.users import User
from aiogram.filters import CommandStart
from models.contents import Scans, Contents, QRCodes
from aiogram.utils.deep_linking import decode_payload
import random

router = Router()

@router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    user, created = await User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={'name': message.from_user.full_name}
    )
    
    args = message.text.split()
    if len(args) > 1:
        try:
            encoded_scan_id = args[1]
            scan_id = decode_payload(encoded_scan_id)
            
            qr_code = await QRCodes.get_or_none(scan_id=scan_id)
            if not qr_code:
                await message.answer("❌ Bu QR kod topilmadi yoki yaroqsiz.")
                return
            
            already_used = await Scans.filter(user=user, qrcode=qr_code).exists()
            if already_used:
                await message.answer("❌ Siz bu QR kodni allaqachon ishlatgansiz!")
                return
            
            seen_content_ids = await Scans.filter(user=user).values_list('content_id', flat=True)
            
            if seen_content_ids:
                unseen_contents = await Contents.exclude(id__in=seen_content_ids).all()
            else:
                unseen_contents = await Contents.all()
            
            if not unseen_contents:
                await message.answer("❌ Hozircha yangi kontent yo'q. Barcha kontentlarni ko'rib bo'lgansiz!")
                return
            
            selected_content = random.choice(unseen_contents)
            
            await Scans.create(user=user, content=selected_content, qrcode=qr_code)
            
            caption = selected_content.title if selected_content.title else ""
            
            if selected_content.content_type == "text":
                await message.answer(selected_content.content)
            elif selected_content.content_type == "photo":
                await message.answer_photo(selected_content.content, caption=caption)
            elif selected_content.content_type == "video":
                await message.answer_video(selected_content.content, caption=caption)
            elif selected_content.content_type == "document":
                await message.answer_document(selected_content.content, caption=caption)
            
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    else:
        await message.answer(
            f"Salom, {message.from_user.full_name}! 👋\n\n"
            "Iltimos, botga QR kod orqali kiring."
        )
