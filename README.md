<div align="center">

# 🤖 WhatsApp Automation Bot
### بوت واتساب ذكي للمتاجر الإلكترونية (سلة)

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp_API-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://developers.facebook.com/docs/whatsapp)
[![Salla](https://img.shields.io/badge/Salla-Partner-7B2FBE?style=for-the-badge)](https://salla.dev/)

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Deploy](https://img.shields.io/badge/Deploy-Railway-blueviolet?style=flat-square&logo=railway)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📌 نظرة عامة

**WhatsApp Automation Bot** هو بوت ذكي يربط متجرك على منصة **سلة** بـ **WhatsApp Business API** تلقائياً. يعمل في وضع Webhook-only بدون الحاجة لـ Access Token يدوي، ويوفر تقارير فورية عن الطلبات والمبيعات والإحصائيات مباشرة على واتساب.

```
╔═══════════════════════════════════════════════════════════════╗
║              🤖 WHATSAPP AUTOMATION BOT                       ║
║                                                               ║
║   سلة Store  ──Webhook──►  Flask Bot  ──►  WhatsApp API       ║
║       │                       │                  │            ║
║       ▼                       ▼                  ▼            ║
║   طلب جديد            معالجة الحدث         رسالة تلقائية      ║
║   دفع ناجح            تحليل البيانات        إشعار فوري        ║
║   إلغاء طلب           إنشاء التقرير         تقرير يومي        ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ✨ المميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 📦 **إشعارات الطلبات** | إشعار فوري على واتساب عند كل طلب جديد |
| 💰 **تتبع المبيعات** | تقارير مبيعات يومية وأسبوعية تلقائية |
| 📊 **إحصائيات Meta Pixel** | تتبع أحداث الإعلانات في آخر ساعة |
| 📢 **حالة الحملات** | مراقبة حالة حملات الإعلانية على Meta |
| 🔐 **التحقق الأمني** | التحقق من توقيع الـ Webhook بـ HMAC-SHA256 |
| ☁️ **نشر سحابي** | جاهز للنشر على Railway و Heroku |
| 🇸🇦 **دعم عربي كامل** | رسائل باللغة العربية مع توقيت السعودية |

---

## 🛠️ التقنيات المستخدمة

```
┌────────────────────────────────────────────────┐
│                 TECH STACK                      │
├──────────────────┬─────────────────────────────┤
│  Backend         │  Python 3.9 + Flask          │
│  WhatsApp API    │  Meta Cloud API (v19.0)       │
│  Store Platform  │  Salla Webhook Integration   │
│  Meta Analytics  │  Meta Pixel + Campaign API   │
│  Security        │  HMAC-SHA256 Signature Check │
│  Deployment      │  Railway (Procfile config)   │
│  Config          │  python-dotenv (.env)        │
└──────────────────┴─────────────────────────────┘
```

---

## 📁 هيكل المشروع

```
wats/
├── 🐍 bot.py              ← الكود الرئيسي للبوت
├── 📄 requirements.txt    ← المكتبات المطلوبة
├── 📄 Procfile            ← إعداد Railway/Heroku
├── 📄 railway.json        ← إعدادات Railway
├── 📄 deploy.sh           ← سكريبت النشر
└── 📄 .env                ← المتغيرات البيئية (لا يُرفع)
```

---

## ⚙️ إعداد وتشغيل المشروع

### 1️⃣ تثبيت المتطلبات
```bash
git clone https://github.com/Eissaali11/wats.git
cd wats
pip install -r requirements.txt
```

### 2️⃣ إعداد ملف .env
```env
# سلة
SALLA_APP_SECRET=your_salla_app_secret

# WhatsApp Business API
WA_ACCESS_TOKEN=your_whatsapp_token
WA_PHONE_NUMBER_ID=your_phone_number_id

# Meta (Pixel + Campaigns)
META_ACCESS_TOKEN=your_meta_token

# رقم الهاتف لإرسال التقارير
REPORT_PHONE=966xxxxxxxxx
```

### 3️⃣ تشغيل البوت
```bash
python bot.py
# يعمل على: http://localhost:5000
```

### 4️⃣ إعداد Webhook على سلة
```
URL: https://your-domain.com/webhook
Events: order.created, order.payment.updated, order.canceled
```

---

## ☁️ النشر على Railway

```bash
# 1. تسجيل الدخول إلى Railway
railway login

# 2. نشر المشروع
railway up

# 3. إضافة المتغيرات البيئية من لوحة Railway
# Settings → Variables → Add All from .env
```

---

## 🔌 API Endpoints

| Method | Endpoint | الوصف |
|--------|----------|-------|
| `POST` | `/webhook` | استقبال أحداث سلة |
| `GET` | `/webhook` | التحقق من الـ Webhook |
| `GET` | `/health` | فحص حالة الخادم |
| `GET` | `/report` | إرسال تقرير يدوي |

---

## 📊 أنواع الإشعارات

```
📦 طلب جديد      → إشعار فوري مع التفاصيل
💳 تأكيد الدفع   → إشعار دفع ناجح
❌ إلغاء طلب     → إشعار إلغاء
📈 تقرير يومي    → إحصائيات المبيعات
🎯 Pixel Stats   → أحداث الإعلانات
📢 حالة الحملة   → ميزانية وحالة الحملة
```

---

## 📜 الترخيص

MIT License — مرخص للاستخدام الحر التجاري والشخصي

---

<div align="center">

**صُنع بـ 🐍 Python لأتمتة متاجر سلة 🛒**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Eissaali11)

</div>
