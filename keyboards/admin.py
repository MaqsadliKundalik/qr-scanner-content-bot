from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

admin_menu = ReplyKeyboardBuilder()
admin_menu.button(text="➕ Kontent qo'shish")
admin_menu.button(text="➕ QR yaratish")
admin_menu.button(text="📊 Hisobotlar")
admin_menu.button(text="📋 Xabar yuborish")
admin_menu.adjust(2, 1)
admin_menu = admin_menu.as_markup(resize_keyboard=True)

admin_back_keyboard = ReplyKeyboardBuilder()
admin_back_keyboard.button(text="⬅️ Orqaga") 
admin_back_keyboard = admin_back_keyboard.as_markup(resize_keyboard=True)

hisobotlar_keyboard = ReplyKeyboardBuilder()
hisobotlar_keyboard.button(text="Kontentlar", callback_data="contents_report")
hisobotlar_keyboard.button(text="Skanerlashlar", callback_data="scans_report")
hisobotlar_keyboard.button(text="Foydalanuvchilar", callback_data="users_report")
hisobotlar_keyboard.button(text="⬅️ Orqaga")
hisobotlar_keyboard.adjust(1)
hisobotlar_keyboard = hisobotlar_keyboard.as_markup(resize_keyboard=True)

def del_content_keyboard(content_id: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🗑️ O'chirish", callback_data=f"delete_content:{content_id}")
    return keyboard.as_markup()