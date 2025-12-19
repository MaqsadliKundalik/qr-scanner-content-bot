# QR Scanner Content Bot

QR kod orqali kontent tarqatuvchi Telegram bot. Foydalanuvchilar QR kodni skanerlaydi va kontent oladi, admin esa kontentlarni boshqaradi va statistikani ko'radi.

## Bot nima qiladi?

### 👨‍💼 Admin uchun

#### Kontent qo'shish
- Turli xil kontentlar yuklash mumkin: matn, rasm, video, fayl
- Har bir kontentga sarlavha qo'yiladi
- Barcha kontentlar ro'yxatini ko'rish

#### QR kod yaratish
- Noyob QR kodlar yaratish
- QR kod PDF formatda saqlanadi (chop etish uchun qulay)
- Har bir QR kodning o'ziga xos IDsi bor

#### Hisobotlar
- Barcha kontentlar sonini ko'rish
- Excel formatda hisobot yuklab olish:
  - Har bir foydalanuvchi necha marta skanerlagani
  - Foydalanuvchilar ro'yxati
  - Jami skanerlashlar soni

### 👥 Foydalanuvchi uchun

#### QR kod skanerlash
- QR kodni skanerlang → darhol kontent oling
- Har safar yangi (ko'rilmagan) kontent keladi
- Bir QR kodni faqat 1 marta ishlatish mumkin
- Matn, rasm, video yoki fayl olishingiz mumkin

#### Kontent olish
- Siz ko'rmagan kontentdan tasodifiy biri yuboriladi
- Bot qaysi kontentni ko'rganingizni eslab qoladi
- Hamma foydalanuvchilarga turli xil kontentlar taqsimlanadi

## Qanday ishlaydi?

1. **Admin kontent yuklaydi** → Ma'lumotlar bazaga saqlanadi
2. **Admin QR kod yaratadi** → Noyob QR kod PDF qilib yuklab olinadi
3. **Foydalanuvchi QR kodni skanerlaydi** → Bot tekshiradi va ruxsat beradi
4. **Bot kontent yuboradi** → Ko'rilmagan kontentdan biri yuboriladi
5. **Skanerlash saqlanadi** → Statistika yangilanadi
6. **Admin hisobotni ko'radi** → Excel faylda to'liq ma'lumotlar

## Xavfsizlik

- QR kod haqiqiyligi tekshiriladi
- Bir QR kodni qayta-qayta ishlatib bo'lmaydi
- Faqat ruxsat berilgan adminlar boshqaradi
- Barcha skanerlashlar bazada saqlanadi

---

*Python, aiogram va Tortoise ORM asosida yaratilgan* 🚀
