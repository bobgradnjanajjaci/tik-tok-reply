from flask import Flask, render_template_string, request
import requests
import re

app = Flask(__name__)

# 🔧 KONFIGURACIJA
PANEL_URL = "https://dnoxsmm.com/api/v2"
API_KEY = "78e1e447b6a8ba2189d0afcd04487c5b"
SERVICE_ID = 4575 

# 🔁 LISTE REPLYEVA
REPLIES_SET_1 = [
    "For me its scary how much power this book has. I felt like someone had reached into my head and exposed everything about how money acutally works... ",
    "Actually I cant believe how is easy to find this book. Just search full name of the book and the first site is their official site. Cant believe how easy it is to find this",
    "The fact is, this book is real and it truly teaches you how to be successful. It's up to each of us to take the chance and read it. Goated book",
    "IS IT REAL that people actually know about this book??? I’m so happy to see others who’ve read it too. Chapter 4 is literally a gold mine, it changed an entire area of my life",
    "This book will become top 1 for money strategies and mindset, I can guarantee that. I highly recommend it to everyone..",
    "Ok so i started seeing this book everywhere lately and btw I did a little research… it actually seems like the real deal. I’m only on chapter 2 but it already has some crazy good info.",
    "this book is literally a must-read when it comes to money and success. I’m shocked it’s still not a best seller after so many legit stories",
    "claimm"
]

REPLIES_SET_2 = [
    "this book changed my life too a few years ago. It’s not the usual BS like other LOA books, i genuinely recommend everyone to read it. Logan is a genius",
    "IS IT REAL that people actually know about this book??? I’m so happy to see others who’ve read it too. Chapter 4 is literally a gold mine, it changed an entire area of my life",
    "why are so many people praising this book? i wanna hear your detailed stories plsss",
    "claimm",
    "Amen",
    "where do i find this book yall???",
    "I just ordered it so i’ll read it soon, i can’t keep running from reality. I really hope this helps me",
    "hmm i’m skeptical but i’ll give it a chance, the book is insanely cheap anyway"
]

def convert_to_mobile_format(pc_link):
    """
    Ekstraktuje Video ID i Comment ID (cid) i pravi mobilnu verziju linka.
    Ovo simulira mobilni request koji paneli zahtevaju.
    """
    try:
        # Čišćenje razmaka
        link = pc_link.strip()
        
        # 1. Tražimo Video ID (niz od ~19 cifara)
        video_id_match = re.search(r'video/(\d+)', link)
        
        # 2. Tražimo Comment ID (cid). Može biti u b64 formatu ili ciframa
        # SMM paneli obično traže cid parametar
        cid_match = re.search(r'cid=([^& \n]+)', link)
        
        if video_id_match and cid_match:
            v_id = video_id_match.group(1)
            c_id = cid_match.group(1)
            
            # Formiramo link koji simulira mobilni browser/app endpoint
            # Većina panela prihvata ovaj m.tiktok.com format kao 'mobile link'
            mobile_url = f"https://m.tiktok.com/v/{v_id}.html?cid={c_id}"
            return mobile_url
            
        return link # Ako ne uspe ekstrakcija, vraća original
    except Exception:
        return pc_link

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>TikTok Link Converter & Sender</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { margin: 0; background: #050816; color: #f9fafb; display: flex; justify-content: center; min-height: 100vh; }
    .container { max-width: 800px; width: 100%; padding: 40px 20px; }
    .card { background: rgba(15, 23, 42, 0.95); border-radius: 18px; padding: 30px; box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6); border: 1px solid rgba(148, 163, 184, 0.2); }
    h1 { font-size: 22px; text-align: center; color: #8b5cf6; margin-bottom: 20px; }
    textarea { width: 100%; min-height: 180px; background: #000; border: 1px solid #334155; border-radius: 10px; color: #6366f1; padding: 15px; font-size: 13px; outline: none; }
    .btn-primary { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none; padding: 12px 30px; border-radius: 50px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 15px; transition: 0.3s; }
    .btn-primary:hover { opacity: 0.9; transform: scale(1.01); }
    .log { margin-top: 20px; background: #000; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 11px; max-height: 300px; overflow-y: auto; border-left: 3px solid #8b5cf6; }
    .radio-group { display: flex; gap: 20px; margin: 15px 0; justify-content: center; }
    .status-msg { text-align: center; margin-top: 10px; font-size: 14px; color: #10b981; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>TikTok Link Auto-Converter</h1>
      <form method="post">
        <label style="font-size: 13px; color: #94a3b8;">Nalepi dugačke PC linkove komentara:</label>
        <textarea name="input_links" placeholder="https://www.tiktok.com/@user/video/123...?cid=456...">{{ input_links }}</textarea>
        
        <div class="radio-group">
          <label><input type="radio" name="reply_set" value="set1" checked> Reply Set #1</label>
          <label><input type="radio" name="reply_set" value="set2"> Reply Set #2</label>
        </div>

        <button type="submit" class="btn-primary">🚀 KONVERTUJ I POŠALJI NA PANEL</button>
      </form>
      
      {% if status %}
        <div class="status-msg">{{ status }}</div>
      {% endif %}

      {% if log %}
        <div class="log"><strong>LOG OPERACIJA:</strong>\n{{ log }}</div>
      {% endif %}
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
            return True, f"Order ID: {data['order']}"
        return False, f"Greška panela: {data}"
    except Exception as e:
        return False, f"Sistemska greška: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    input_links = ""
    status = ""
    log_lines = []

    if request.method == "POST":
        input_links = request.form.get("input_links", "")
        reply_set = request.form.get("reply_set", "set1")
        comments = REPLIES_SET_2 if reply_set == "set2" else REPLIES_SET_1
        
        lines = [l.strip() for l in input_links.splitlines() if l.strip()]
        
        success_count = 0
        for raw_link in lines:
            # KONVERZIJA U MOBILE FORMAT (m.tiktok.com)
            mobile_link = convert_to_mobile_format(raw_link)
            
            # SLANJE NA PANEL
            ok, msg = send_reply_order(mobile_link, comments)
            
            if ok:
                success_count += 1
                log_lines.append(f"[OK] Poslato kao: {mobile_link} | {msg}")
            else:
                log_lines.append(f"[FAIL] Link: {mobile_link} | {msg}")
        
        status = f"Obrađeno {len(lines)} linkova. Uspešno: {success_count}."

    return render_template_string(
        HTML_TEMPLATE, 
        input_links=input_links, 
        status=status, 
        log="\n".join(log_lines)
    )

if __name__ == "__main__":
    app.run(debug=True)
