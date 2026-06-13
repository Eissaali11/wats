#!/bin/bash
# ════════════════════════════════════════════════
# شوب ستور Bot — Railway Deploy Script
# شغّل هذا الملف من جهازك بعد فك الضغط
# ════════════════════════════════════════════════

echo "🚀 بدء النشر على Railway..."

# 1. تثبيت Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 تثبيت Railway CLI..."
    npm install -g @railway/cli
fi

# 2. تسجيل الدخول
echo "🔐 تسجيل الدخول..."
railway login

# 3. إنشاء المشروع
echo "📁 إنشاء مشروع جديد..."
railway init --name sho9-whatsapp-bot

# 4. رفع المتغيرات
echo "⚙️ رفع المتغيرات..."
railway variables set \
  WA_ACCESS_TOKEN="EAAjwAMAyOg4BRtZCKgZBy779wy9DIrhjGchLmYK1wJt9fgm7MVCYr0bfRHEOR2F6pQPMdRd1UZBgnmnsWXrF9HZAuwvnysfuvDllHEbGahSso4Ec8dnBhHlyZAUZBPEJZCDT3RUF1iRhqZCh348mZBrGZCnrlnAduTC4SPlOr13lnlKtry4kZAgCiRZC2LowS3VHq0Yz7EYz" \
  WA_PHONE_NUMBER_ID="152632267938763" \
  REPORT_PHONE="966558619232" \
  META_ACCESS_TOKEN="REPLACE_WITH_YOUR_META_TOKEN" \
  SALLA_APP_SECRET="" \
  PORT="5000"

# 5. النشر
echo "🚢 نشر الكود..."
railway up --detach

# 6. جلب الرابط
echo "🌐 جلب رابط التطبيق..."
sleep 5
railway domain

echo ""
echo "✅ تم النشر!"
echo "اختبر البوت على: https://YOUR_URL/test"
echo "ثم اربط الـ Webhook في سلة على: https://YOUR_URL/webhook/salla"
