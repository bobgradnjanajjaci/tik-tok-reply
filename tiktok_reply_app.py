from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# 🔧 KONFIGURACIJA – OVO POPUNI
PANEL_URL = "https://dnoxsmm.com/api/v2"
API_KEY = "09e6e0fdfba11b73696a0a04965d2fe5"          # npr. 6b4b33ef856ee4ef973fcaa450e62786
SERVICE_ID = 4575                           # STAVI TAČAN service ID za TikTok custom comment reply

# 🔁 LISTE REPLYEVA – TVOJE LISTE

REPLIES_SET_1 = [
    "For me its scary how much power this book has. I felt like someone had reached into my head and exposed everything about how money acutally works... ",
    "The fact is, this book is real and it truly teaches you how to be successful. It's up to each of us to take the chance and read it. Goated book"
    "IS IT REAL that people actually know about this book??? I’m so happy to see others who’ve read it too. Chapter 4 is literally a gold mine, it changed an entire area of my life",
    "This book will become top 1 for money strategies and mindset, I can guarantee that. I highly recommend it to everyone..",
    "Ok so i started seeing this book everywhere lately and btw I did a little research… it actually seems like the real deal. I’m only on chapter 2 but it already has some crazy good info. I also looked deeper and heard that Ethan had some connections with secret societies and pulled a lot of knowledge from there that’s usually hidden from the average person, so no wonder the book is kinda hidden and so good",
    "this book is literally a must-read when it comes to money and success. I’m shocked it’s still not a best seller after so many legit stories",
    "claimm",
    
   
    

]

REPLIES_SET_2 = [
    "this book changed my life too a few years ago. It’s not the usual BS like other LOA books, i genuinely recommend everyone to read it. Logan is a genius",
    "IS IT REAL that people actually know about this book??? I’m so happy to see others who’ve read it too. Chapter 4 is literally a gold mine, it changed an entire area of my life",
    "why are so many people praising this book? i wanna hear your detailed stories plsss",
    "claimm",
    "Amen",
    "where do i find this book yall???",
    "I just ordered it so i’ll read it soon, i can’t keep running from reality. I really hope this helps me",
    "hmm i’m skeptical but i’ll give it a chance, the book is insanely cheap anyway",
    "Ok so i started seeing this book everywhere lately and btw I did a little research… it actually seems like the real deal. I’m only on chapter 2 but it already has some crazy good info. I also looked deeper and heard that Logan had some connections with secret societies and pulled a lot of knowledge from there that’s usually hidden from the average person, so no wonder the book is kinda hidden and so good",
    "this book is literally a must-read when it comes to manifestation. I’m shocked it’s still not a best seller after so many legit stories",
]

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>TikTok Comment Reply Sender</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {
      box-sizing: border-box;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body {
      margin: 0;
      padding: 0;
      background: #050816;
      color: #f9fafb;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
    }

    .container {
      max-width: 900px;
      width: 100%;
      padding: 24px 16px 48px;
    }

    .card {
      background: rgba(15, 23, 42, 0.95);
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.3);
    }

    h1 {
      font-size: 24px;
      margin-bottom: 4px;
      text-align: center;
    }

    .subtitle {
      text-align: center;
      font-size: 13px;
      color: #9ca3af;
      margin-bottom: 18px;
    }

    label {
      font-size: 13px;
      font-weight: 500;
      margin-bottom: 6px;
      display: inline-block;
    }

    textarea {
      width: 100%;
      min-height: 200px;
      background: rgba(15, 23, 42, 0.9);
      border-radius: 12px;
      border: 1px solid rgba(55, 65, 81, 0.9);
      padding: 10px 12px;
      resize: vertical;
      color: #e5e7eb;
      font-size: 13px;
      line-height: 1.4;
      outline: none;
    }

    textarea:focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.6);
    }

    .hint {
      font-size: 11px;
      color: #9ca3af;
      margin-top: 4px;
    }

    .btn-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin: 16px 0;
    }

    button {
      border: none;
      border-radius: 999px;
      padding: 10px 20px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.15s ease;
    }

    .btn-primary {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: white;
      box-shadow: 0 10px 25px rgba(79, 70, 229, 0.6);
    }

    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 12px 30px rgba(79, 70, 229, 0.8);
    }

    .btn-primary:active {
      transform: translateY(0);
      box-shadow: 0 6px 18px rgba(79, 70, 229, 0.6);
    }

    .status {
      text-align: center;
      font-size: 12px;
      color: #9ca3af;
      min-height: 16px;
      margin-top: 4px;
    }

    .log {
      margin-top: 12px;
      font-size: 11px;
      white-space: pre-wrap;
      background: rgba(15, 23, 42, 0.85);
      border-radius: 10px;
      padding: 10px;
      border: 1px solid rgba(55,65,81,0.9);
      max-height: 260px;
      overflow: auto;
    }

    .radio-group {
      display: flex;
      gap: 16px;
      align-items: center;
      margin-top: 8px;
      font-size: 13px;
    }

    .radio-group label {
      font-weight: 400;
      margin: 0;
    }

  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>TikTok Comment Reply Sender</h1>
      <div class="subtitle">
        Nalepi TikTok <b>comment linkove</b> (jedan po liniji), izaberi listu replyeva i pusti da app pošalje sve ordere na panel (service {{ service_id }}).<br>
        Link se šalje PANELU TAČNO onakav kakav ga ovde nalepiš (bez ikakve konverzije).
      </div>

      <form method="post">
        <label for="input_links">Comment linkovi</label>
        <textarea id="input_links" name="input_links" placeholder="Primer:
https://vm.tiktok.com/ZMHTTNkcWmPVu-YrDtq/
https://vm.tiktok.com/ZMHTTNStjBu8S-bAkas/
https://vm.tiktok.com/ZMHTTNAsVghg4-9kpCE/">{{ input_links or '' }}</textarea>
        <div class="hint">Svaki red = jedan TikTok comment link (ostaje isti, ne pretvara se u PC link).</div>

        <div style="margin-top:14px;">
          <span style="font-size:13px;font-weight:500;">Izaberi set replyeva:</span>
          <div class="radio-group">
            <label>
              <input type="radio" name="reply_set" value="set1" {% if reply_set == 'set1' %}checked{% endif %}>
              Replyevi #1 ({{ replies1_count }} kom)
            </label>
            <label>
              <input type="radio" name="reply_set" value="set2" {% if reply_set == 'set2' %}checked{% endif %}>
              Replyevi #2 ({{ replies2_count }} kom)
            </label>
          </div>
          <div class="hint">
            Replyevi se šalju kao Custom Comments list (po jedan u svakom redu).
          </div>
        </div>

        <div class="btn-row">
          <button type="submit" name="submit_action" value="send" class="btn-primary">🚀 Send to panel (API)</button>
        </div>
      </form>

      <div class="status">{{ status or '' }}</div>
      {% if log %}
      <div class="log">{{ log }}</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

def send_reply_order(comment_link: str, comments_list: list[str]):
    """
    Šalje JEDAN order na DNOXSMM za custom comments (reply).
    comment_link -> koristi se TAČNO onakav kakav si ga nalepio (bez konverzije).
    comments_list -> lista stringova, svaki reply u posebnom redu.
    """
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
        try:
            data = r.json()
        except Exception:
            return False, f"HTTP {r.status_code}, body={r.text[:200]}"

        if "order" in data:
            return True, f"order={data['order']}"
        else:
            return False, f"resp={data}"
    except Exception as e:
        return False, f"exception={e}"

@app.route("/", methods=["GET", "POST"])
def index():
    input_links = ""
    status = ""
    log_lines = []
    reply_set = "set1"

    if request.method == "POST":
        reply_set = request.form.get("reply_set", "set1")
        input_links = request.form.get("input_links", "")
        lines = [l.strip() for l in input_links.splitlines() if l.strip()]

        if reply_set == "set2":
            comments = REPLIES_SET_2
            set_name = "Replyevi #2"
        else:
            comments = REPLIES_SET_1
            set_name = "Replyevi #1"

        if not comments:
            status = "⚠ Odabrani set replyeva je PRAZAN – popuni REPLIES_SET_1 / 2 u kodu."
        else:
            sent_ok = 0
            sent_fail = 0
            log_lines.append(f"Korišćen set: {set_name} ({len(comments)} komentara)")
            log_lines.append(f"Slanje na {PANEL_URL}, service={SERVICE_ID}")
            log_lines.append("")

            for raw_link in lines:
                link_to_send = raw_link.strip()
                if not link_to_send:
                    sent_fail += 1
                    log_lines.append(f"[SKIP] Prazan link u liniji.")
                    continue

                ok, msg = send_reply_order(link_to_send, comments)
                if ok:
                    sent_ok += 1
                    log_lines.append(f"[OK] {link_to_send} -> {msg}")
                else:
                    sent_fail += 1
                    log_lines.append(f"[FAIL] {link_to_send} -> {msg}")

            status = f"Gotovo. Linija: {len(lines)}, uspešnih ordera: {sent_ok}, fail: {sent_fail}."

    log = "\n".join(log_lines) if log_lines else ""

    return render_template_string(
        HTML_TEMPLATE,
        input_links=input_links,
        status=status,
        log=log,
        reply_set=reply_set,
        replies1_count=len(REPLIES_SET_1),
        replies2_count=len(REPLIES_SET_2),
        service_id=SERVICE_ID,
    )

if __name__ == "__main__":
    app.run(debug=True)


