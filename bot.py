"""
شوب ستور — WhatsApp Automation Bot (Webhook-only mode)
لا يحتاج SALLA_ACCESS_TOKEN — يعتمد على بيانات الـ Webhook مباشرة
"""
import os, hmac, hashlib, logging, requests
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sho9bot")
app = Flask(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
SALLA_SECRET  = os.getenv("SALLA_APP_SECRET", "")
META_TOKEN    = os.getenv("META_ACCESS_TOKEN", "")
WA_TOKEN      = os.getenv("WA_ACCESS_TOKEN", "")
WA_PHONE_ID   = os.getenv("WA_PHONE_NUMBER_ID", "152632267938763")
REPORT_PHONE  = os.getenv("REPORT_PHONE", "966558619232")
PIXEL_ID      = "992972159819465"
CAMPAIGN_ID   = "120248463358590034"
KSA           = timezone(timedelta(hours=3))

# ── Signature check ────────────────────────────────────────────────────────────
def valid_sig(body: bytes, header: str) -> bool:
    if not SALLA_SECRET: return True
    mac = hmac.new(SALLA_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, header.replace("sha256=", ""))

# ── Meta Pixel (آخر ساعة) ─────────────────────────────────────────────────────
def pixel_stats() -> dict:
    if not META_TOKEN: return {}
    try:
        now = int(datetime.now(timezone.utc).timestamp())
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{PIXEL_ID}/stats",
            params={"access_token": META_TOKEN, "aggregation": "event",
                    "start_time": str(now - 3600), "end_time": str(now)},
            timeout=8)
        if not r.ok: return {}
        counts = {}
        for bucket in r.json().get("data", []):
            for item in bucket.get("data", []):
                ev = item.get("value", "")
                counts[ev] = counts.get(ev, 0) + item.get("count", 0)
        return counts
    except: return {}

# ── Campaign status ────────────────────────────────────────────────────────────
def campaign_info() -> dict:
    if not META_TOKEN: return {"status": "—", "budget": "—"}
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{CAMPAIGN_ID}",
            params={"access_token": META_TOKEN,
                    "fields": "effective_status,daily_budget"},
            timeout=8)
        if not r.ok: return {"status": "—", "budget": "—"}
        d = r.json()
        return {
            "status": d.get("effective_status", "—"),
            "budget": f"{round(int(d.get('daily_budget', 0)) / 100)} ر.س"
        }
    except: return {"status": "—", "budget": "—"}

# ── Is from campaign? ──────────────────────────────────────────────────────────
def from_campaign(order: dict) -> bool:
    src = (order.get("source") or "").lower()
    ref = str(order.get("reference_id", ""))
    return src in {"instagram", "facebook", "meta", "fb"} or "12024846" in src

# ── Extract order data from webhook ───────────────────────────────────────────
def parse_order(data: dict) -> dict:
    """يستخرج بيانات الطلب من webhook payload مباشرة"""
    # سلة ترسل البيانات في data.data أو data مباشرة
    order = data.get("data", data)
    
    # بيانات العميل
    cust = order.get("customer", {})
    if isinstance(cust, str): cust = {}
    
    # بيانات الطلب
    total = order.get("total", {})
    if isinstance(total, (int, float, str)):
        total = {"amount": total, "currency": "SAR"}
    
    # المنتجات
    items = order.get("items", [])
    if not items:
        # بعض الـ webhooks ترسل المنتجات بشكل مختلف
        items = order.get("products", [])
    
    products = "\n".join(
        f"  • {i.get('name', i.get('product_name', '—'))} × {i.get('quantity', 1)}"
        for i in (items if isinstance(items, list) else [])
    ) or "  • —"

    return {
        "ref":      order.get("reference_id", order.get("id", "—")),
        "source":   order.get("source", "—"),
        "status":   (order.get("status", {}) or {}).get("name", "—"),
        "amount":   f"{total.get('amount', '—')} {total.get('currency', 'SAR')}",
        "payment":  order.get("payment_method", "—"),
        "products": products,
        "name":     cust.get("full_name", cust.get("name", "—")),
        "city":     cust.get("city") or cust.get("country") or "—",
        "mobile":   f"{cust.get('mobile_code','')} {cust.get('mobile','')}".strip(),
        "url":      (order.get("urls", {}) or {}).get("admin", "—"),
        "raw":      order,
    }

# ── Build WhatsApp message ─────────────────────────────────────────────────────
def build_msg(order: dict, px: dict, cam: dict, is_cam: bool) -> str:
    now  = datetime.now(KSA).strftime("%d/%m/%Y %H:%M")
    icon = "✅" if cam["status"] == "ACTIVE" else "⏸"
    
    header = ""
    if is_cam:
        header = "🎯 *هذا الطلب من الحملة الإعلانية!*\n\n"
    
    return f"""{header}🛍️ *طلب جديد — شوب ستور*
📅 {now}
━━━━━━━━━━━━━━━━━━━
🔖 *الطلب:* #{order['ref']}
👤 *العميل:* {order['name']}
📍 *الموقع:* {order['city']}
📞 *الجوال:* {order['mobile']}
💳 *الدفع:* {order['payment']}
📦 *المنتجات:*
{order['products']}
💰 *القيمة:* {order['amount']}
🟢 *الحالة:* {order['status']}
📣 *المصدر:* {order['source']}

━━━━━━━━━━━━━━━━━━━
🎯 *حملة ميتا:*
• {icon} {cam['status']} | {cam['budget']}/يوم

📡 *بكسل (آخر ساعة):*
• Purchase: {px.get('Purchase',0)} | Checkout: {px.get('InitiateCheckout',0)}
• AddToCart: {px.get('AddToCart',0)} | PageView: {px.get('PageView',0)}

🔗 {order['url']}"""

# ── Send WhatsApp ──────────────────────────────────────────────────────────────
def send_wa(phone: str, msg: str) -> bool:
    try:
        r = requests.post(
            f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}/messages",
            headers={"Authorization": f"Bearer {WA_TOKEN}",
                     "Content-Type": "application/json"},
            json={"messaging_product": "whatsapp",
                  "recipient_type": "individual",
                  "to": phone,
                  "type": "text",
                  "text": {"preview_url": False, "body": msg}},
            timeout=15)
        ok = r.ok
        log.info(f"{'✅' if ok else '❌'} WA → {phone} | {r.status_code}")
        if not ok: log.error(r.text[:300])
        return ok
    except Exception as e:
        log.error(f"WA error: {e}")
        return False

# ── Webhook ────────────────────────────────────────────────────────────────────
@app.route("/webhook/salla", methods=["POST"])
def webhook():
    body = request.get_data()
    sig  = request.headers.get("X-Salla-Signature", "")
    
    if not valid_sig(body, sig):
        log.warning("Bad signature")
        return jsonify({"error": "unauthorized"}), 401

    data  = request.get_json(force=True, silent=True) or {}
    event = data.get("event", "")
    log.info(f"📨 Event: {event}")

    # الأحداث المهمة فقط
    if event not in ("order.created", "order.updated", "order.status.updated"):
        return jsonify({"ok": True, "skip": event}), 200

    # استخراج بيانات الطلب من الـ webhook مباشرة
    order  = parse_order(data)
    is_cam = from_campaign(order["raw"])

    # جمع بيانات ميتا
    px  = pixel_stats()
    cam = campaign_info()

    # بناء وإرسال الرسالة
    msg = build_msg(order, px, cam, is_cam)
    send_wa(REPORT_PHONE, msg)

    return jsonify({"ok": True, "ref": order["ref"], "campaign": is_cam}), 200

# ── Salla webhook verification (GET) ──────────────────────────────────────────
@app.route("/webhook/salla", methods=["GET"])
def webhook_verify():
    # سلة تتحقق من الـ endpoint بـ GET أحياناً
    return jsonify({"ok": True}), 200

# ── Health ─────────────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({
        "ok": True,
        "time_ksa": datetime.now(KSA).strftime("%Y-%m-%d %H:%M"),
        "wa_phone_id": WA_PHONE_ID,
        "report_to": REPORT_PHONE,
        "pixel": PIXEL_ID,
        "campaign": CAMPAIGN_ID,
        "tokens": {
            "wa": "✅" if WA_TOKEN else "❌",
            "meta": "✅" if META_TOKEN else "❌",
            "salla_secret": "✅" if SALLA_SECRET else "⚠️ optional"
        }
    })

# ── Test ───────────────────────────────────────────────────────────────────────
@app.route("/test")
def test():
    dummy_data = {
        "event": "order.created",
        "data": {
            "id": 1573970250,
            "reference_id": "266110959",
            "source": "instagram",
            "status": {"name": "تم التنفيذ", "slug": "completed"},
            "total": {"amount": "27.99", "currency": "SAR"},
            "payment_method": "مدى",
            "customer": {
                "full_name": "عمر",
                "mobile": "534755901",
                "mobile_code": "+966",
                "city": "ينبع"
            },
            "items": [{"name": "بلس ايفون — الباقة الذهبية", "quantity": 1}],
            "urls": {"admin": "https://s.salla.sa/orders/test"}
        }
    }
    order  = parse_order(dummy_data)
    px     = pixel_stats()
    cam    = campaign_info()
    msg    = build_msg(order, px, cam, True)
    ok     = send_wa(REPORT_PHONE, msg)
    return jsonify({"sent": ok, "to": REPORT_PHONE, "preview": msg[:200]})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    log.info(f"🚀 Bot starting on port {port}")
    app.run(host="0.0.0.0", port=port)
