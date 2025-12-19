import asyncio
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from config import ADMINS
from filters.admin import IsAdminFilter
from keyboards.admin import admin_menu, admin_back_keyboard, hisobotlar_keyboard
from aiogram.fsm.context import FSMContext
from states.admin import AddContentStates, SendMsgState
from models.contents import Contents, Scans, QRCodes
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from models.users import User
from aiogram.utils.deep_linking import create_start_link
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import uuid

router = Router()


async def save_content_to_db(content_message: Message, title: str):
    if content_message.text:
        await Contents.create(content_type="text", content=content_message.text, title=title)
    elif content_message.photo:
        file_id = content_message.photo[-1].file_id
        await Contents.create(content_type="photo", content=file_id, title=title)
    elif content_message.video:
        file_id = content_message.video.file_id
        await Contents.create(content_type="video", content=file_id, title=title)
    elif content_message.document:
        file_id = content_message.document.file_id
        await Contents.create(content_type="document", content=file_id, title=title)


@router.message(Command("start"), IsAdminFilter())
async def admin_start(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Salom, Admin! Botga xush kelibsiz.", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "⬅️ Orqaga", IsAdminFilter())
async def admin_back(message: Message, state: FSMContext):
    await message.answer("Asosiy menyu:", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "📊 Hisobotlar", IsAdminFilter())
async def admin_reports(message: Message, state: FSMContext):
    await message.answer("Hisobotlar menyusi:", reply_markup=hisobotlar_keyboard)
    await state.clear()

@router.message(F.text == "➕ Kontent qo'shish", IsAdminFilter())
async def admin_add_content(message: Message, state: FSMContext):
    await message.answer("Kontentni yuboring.", reply_markup=admin_back_keyboard)
    await state.set_state(AddContentStates.waiting_for_content)

@router.message(AddContentStates.waiting_for_content, IsAdminFilter())
async def process_content(message: Message, state: FSMContext):
    await state.update_data(content=message)
    if not message.text or not message.caption:
        await message.answer("Endi kontent uchun sarlavha yuboring.")
        await state.set_state(AddContentStates.waiting_for_title)
    else:
        await save_content_to_db(message, "" if message.text else message.caption)

@router.message(AddContentStates.waiting_for_title, IsAdminFilter())
async def process_title(message: Message, state: FSMContext):
    data = await state.get_data()
    content_message: Message = data.get("content")
    
    title = ""
    if message.text:
        title = message.text
    elif message.caption:
        title = message.caption

    await save_content_to_db(content_message, title)
    await message.answer("Kontent muvaffaqiyatli qo'shildi!", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "➕ QR yaratish", IsAdminFilter())
async def admin_create_qr(message: Message, state: FSMContext, bot: Bot):
    scan_id = str(uuid.uuid4())
    
    await QRCodes.create(scan_id=scan_id)
    
    link = await create_start_link(bot, scan_id, encode=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    
    c.drawInlineImage(qr_img, 
                      width / 2 - 150, 
                      height / 2 - 150, 
                      width=300, 
                      height=300)
    
    c.save()
    pdf_buffer.seek(0)
    
    pdf_filename = f"qr_code_{scan_id[:8]}.pdf"
    with open(pdf_filename, 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    pdf_file = FSInputFile(pdf_filename)
    await message.answer_document(
        pdf_file,
        caption=f"✅ QR kod muvaffaqiyatli yaratildi!"
    )
    
    import os
    os.remove(pdf_filename)
    
    await state.clear()
    
@router.message(F.text == "📋 Xabar yuborish", IsAdminFilter()) 
async def admin_send_message(message: Message, state: FSMContext):
    await message.answer("Yuboriladigan xabarni yuboring.", reply_markup=admin_back_keyboard)
    await state.set_state(SendMsgState.waiting_for_message)

@router.message(SendMsgState.waiting_for_message, IsAdminFilter())
async def process_send_message(message: Message, state: FSMContext, bot: Bot):
    users = await User.all()
    sent_count = 0
    failed_count = 0
    
    for user in users:
        try:
            await bot.copy_message(chat_id=user.telegram_id, from_chat_id=message.chat.id, message_id=message.message_id)
            sent_count += 1
            await asyncio.sleep(0.03)
        except TelegramForbiddenError:
            await user.delete()
            failed_count += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as e:
            failed_count += 1
    
    await message.answer(f"Xabar yuborildi!\nMuvaffaqiyatli: {sent_count}\nMuvaffaqiyatsiz: {failed_count}", reply_markup=admin_menu)
    await state.clear()