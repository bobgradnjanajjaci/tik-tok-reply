from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# 🔧 KONFIGURACIJA
PANEL_URL = "https://dnoxsmm.com/api/v2"
API_KEY = "78e1e447b6a8ba2189d0afcd04487c5b"
SERVICE_ID = 4575 

REPLIES_SET_1 = [
    "For me its scary how much power this book has...",
    "Actually I cant believe how is easy to find this book...",
    "The fact is, this book is real..."
]

REPLIES_SET_2 = [
    "this book changed my life too a few years ago...",
    "IS IT REAL that people actually know about this book???",
]

# --- NOVA FUNKCIJA ZA KONVERZIJU ---
def get_mobile_link(pc_link):
    """
    Uzima PC link i pretvara ga u kratki mobilni link 
    imitirajući mobilni uređaj.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/04.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    try:
        # Čistimo link od nepotrebnih stvari pre slanja
        clean_pc_link = pc_link.strip()
        if not clean_pc_link.startswith("http"):
            clean_pc_link = "https://" + clean_pc_link

        # Šaljemo zahtev TikToku i pratimo redirekcije
        # allow_redirects=True nam omogućava da dođemo do finalnog skraćenog linka
        response = requests.get(clean_pc_link, headers=headers, allow_redirects=True, timeout=10)
        
        # Vraćamo finalni URL (obično će biti u formatu vt.tiktok.com ili slično)
        return response.url
    except Exception as e:
        print(f"Greška pri konverziji linka: {e}")
        return pc_link # Ako ne uspe, šalje original

# --- HTML TEMPLATE (Samo mala izmena u tekstu) ---
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>TikTok Auto-Converter & Sender</title>
  <meta charset="utf-8">
  <style>
    /* ... (Zadrži sav tvoj CSS koji si poslao) ... */
    body { background: #050816; color: #f9fafb; font-family: system-ui; }
    .container { max-width: 900px; margin: auto; padding: 20px; }
    .card { background: rgba(15, 23, 42, 0.95); padding: 20px; border-radius: 18px; border: 1px solid rgba(148, 163, 184, 0.3); }
    textarea { width: 100%; min-height: 200px; background: #000; color: #fff; padding: 10px; }
    button { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 10px 20px; border-radius: 999px; cursor: pointer; border: none; }
    .log { background: #000; padding: 10px; font-size: 11px; margin-top: 10px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>TikTok PC -> Mobile Converter</h1>
      <p style="font-size:12px; color:#9ca3af; text-align:center;">
        Zalepi <b>PC linkove</b>. Skripta će ih automatski pretvoriti u <b>mobile format</b> pre slanja na panel.
      </p>
      <form method="post">
        <textarea name="input_links" placeholder="https://www.tiktok.com/@user/video/762960...">{{ input_links }}</textarea>
        <div style="margin: 15px 0;">
           <input type="radio" name="reply_set" value="set1" checked> Set 1
           <input type="radio" name="reply_set" value="set2"> Set 2
        </div>
        <button type="submit">🚀 Convert & Send to Panel</button>
      </form>
      <div class="log">{{ log }}</div>
    </div>
  </div>
</body>
</html>
"""

def send_reply_order(comment_link: str, comments_list: list[str]):
    comments_text = "\n".join(comments_list)
    payload = {
        "key": API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": comment_link,
        "comments": comments_text,
    }
    try:
        r = requests.post(PANEL_URL, data=payload, timeout=20)
        data = r.json()
        if "order" in data:
            return True, f"order={data['order']}"
        return False, f"resp={data}"
    except Exception as e:
        return False, f"exception={e}"

@app.route("/", methods=["GET", "POST"])
def index():
    input_links = ""
    log_lines = []
    if request.method == "POST":
        input_links = request.form.get("input_links", "")
        reply_set = request.form.get("reply_set", "set1")
        comments = REPLIES_SET_2 if reply_set == "set2" else REPLIES_SET_1
        
        lines = [l.strip() for l in input_links.splitlines() if l.strip()]
        
        for raw_link in lines:
            # 1. KONVERZIJA: PC -> MOBILE
            mobile_link = get_mobile_link(raw_link)
            log_lines.append(f"[CONVERT] {raw_link[:30]}... -> {mobile_link}")
            
            # 2. SLANJE NA PANEL
            ok, msg = send_reply_order(mobile_link, comments)
            if ok:
                log_lines.append(f"[SUCCESS] {msg}")
            else:
                log_lines.append(f"[FAILED] {msg}")
                
    return render_template_string(HTML_TEMPLATE, input_links=input_links, log="\n".join(log_lines))

if __name__ == "__main__":
    app.run(debug=True)
