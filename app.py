#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source gốc khôi phục từ pydew.py  (obfuscator: PyDew v2.6.3 / ENC python3.12 High)
Tên file gốc trong marshal: <PyDew>

Tóm tắt: công cụ đăng ký hàng loạt tài khoản mail tạm mail.tm
qua danh sách proxy, lưu kết quả vào mail_tm@Doki.txt
"""

import os
import requests
import random
import string
import time
import threading
from colorama import Fore, Style, init
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel


# ---------------------------------------------------------------- helpers ---

def decode_string(s, k, salt):
    """Bộ giải mã chuỗi của PyDew (a85 + XOR dòng LCG)."""
    import base64 as _b
    raw = _b.a85decode(s)
    out = bytearray(len(raw))
    kk = k
    for i, b in enumerate(raw):
        out[i] = b ^ kk & 255
        kk = kk * 1103515245 + salt + i & 0xFFFFFFFF
    return bytes(out).decode('utf-8')


def hash_mix(x):
    """Hàm mồ côi, được định nghĩa nhưng KHÔNG BAO GIỜ được gọi."""
    return (x * 73244475 ^ x >> 16) & 0xFFFFFFFF


def anti_decompiler():
    """Phát hiện decompiler/debugger đang nạp (uncompyle6, decompyle3, pycdc...)."""
    import sys as _s
    import warnings as _w
    _found = [m for m in ('uncompyle6', 'decompyle3', 'decompyle', 'pycdc', 'pycdas')
              if m in _s.modules]
    if _found:
        _w.warn(f'PyDew: công cụ phân tích được phát hiện: {_found}', RuntimeWarning)
    return 1


def junk_1(cクᚲ鼅):
    return 0


def junk_2(b黺Θ齔):
    return 0


def junk_3(tF龗φ齠μu):
    return 0


anti_decompiler()
junk_1(3302)
junk_2(3106)
junk_3(9315)

init(autoreset=True)

# ------------------------------------------------------------- constants ---

PASSWORD = 'HaiLam@DepTrai102'   # _鼵υ龜齕юG黲ο
PREFIX = 'hailam'                # b齬エ齺齍χη龎
OUT_FILE = 'mail_tm@Doki.txt'    # V鼆ЛШ鼞х齜q

PROXIES = [                      # Rテ齖齒LKσ齤u
    '31.59.20.176:6754:kthquiob:oz9nwpusrztr',
    '23.95.150.145:6114:kthquiob:oz9nwpusrztr',
    '198.23.239.134:6540:kthquiob:oz9nwpusrztr',
    '45.38.107.97:6014:kthquiob:oz9nwpusrztr',
    '107.172.163.27:6543:kthquiob:oz9nwpusrztr',
    '198.105.121.200:6462:kthquiob:oz9nwpusrztr',
    '64.137.96.74:6641:kthquiob:oz9nwpusrztr',
    '216.10.27.159:6837:kthquiob:oz9nwpusrztr',
    '23.26.71.145:5628:kthquiob:oz9nwpusrztr',
    '23.229.19.94:8689:kthquiob:oz9nwpusrztr',
    '31.59.20.176:6754:dokideptrai:39rt9fpl2wnf',
    '23.95.150.145:6114:dokideptrai:39rt9fpl2wnf',
    '198.23.239.134:6540:dokideptrai:39rt9fpl2wnf',
    '107.172.163.27:6543:dokideptrai:39rt9fpl2wnf',
    '198.105.121.200:6462:dokideptrai:39rt9fpl2wnf',
    '64.137.96.74:6641:dokideptrai:39rt9fpl2wnf',
    '216.10.27.159:6837:dokideptrai:39rt9fpl2wnf',
    '23.26.71.145:5628:dokideptrai:39rt9fpl2wnf',
    '23.229.19.94:8689:dokideptrai:39rt9fpl2wnf',
    '2.57.20.2:5994:dokideptrai:39rt9fpl2wnf',
    '31.59.20.176:6754:ptnpdaqs:pvt57v196gir',
    '23.95.150.145:6114:ptnpdaqs:pvt57v196gir',
    '198.23.239.134:6540:ptnpdaqs:pvt57v196gir',
    '45.38.107.97:6014:ptnpdaqs:pvt57v196gir',
    '107.172.163.27:6543:ptnpdaqs:pvt57v196gir',
    '198.105.121.200:6462:ptnpdaqs:pvt57v196gir',
    '64.137.96.74:6641:ptnpdaqs:pvt57v196gir',
    '216.10.27.159:6837:ptnpdaqs:pvt57v196gir',
    '23.26.71.145:5628:ptnpdaqs:pvt57v196gir',
    '23.229.19.94:8689:ptnpdaqs:pvt57v196gir',
    '31.59.20.176:6754:cbuoggup:nd4nwe9q3r0q',
    '23.95.150.145:6114:cbuoggup:nd4nwe9q3r0q',
    '198.23.239.134:6540:cbuoggup:nd4nwe9q3r0q',
    '45.38.107.97:6014:cbuoggup:nd4nwe9q3r0q',
    '107.172.163.27:6543:cbuoggup:nd4nwe9q3r0q',
    '198.105.121.200:6462:cbuoggup:nd4nwe9q3r0q',
    '64.137.96.74:6641:cbuoggup:nd4nwe9q3r0q',
    '216.10.27.159:6837:cbuoggup:nd4nwe9q3r0q',
    '23.26.71.145:5628:cbuoggup:nd4nwe9q3r0q',
    '23.229.19.94:8689:cbuoggup:nd4nwe9q3r0q',
]

HEADERS = {                      # mуД黽齯υυг齫齒Ψb
    'Content-Type': 'application/json',
}


# ----------------------------------------------------------- core helpers ---

def random_name(M鼩ΕΗΛΤФ齇AΑzяJΩК=6):
    """Sinh chuỗi ngẫu nhiên gồm chữ thường + chữ số."""
    x齖ナβаεГ齻Ξ = 0
    x齖ナβаεГ齻Ξ += 1
    try:
        raise MemoryError(x齖ナβаεГ齻Ξ)
    except MemoryError as IΤиΦГн:
        if IΤиΦГн.args[0] == 1:
            try:
                _ = 1 / 0
            except ZeroDivisionError:
                return ''.join(random.choice(string.ascii_lowercase + string.digits)
                               for _ in range(M鼩ΕΗΛΤФ齇AΑzяJΩК))
        if IΤиΦГн.args[0] == 2:
            wοπDЙΚ = 2674
        if IΤиΦГн.args[0] == 3:
            n黮鼔鼦鼙Τ = 599
        if IΤиΦГн.args[0] == 4:
            wbР齺Τ龡鼿 = 6805


def build_proxy(F鼦黰Κ鼶Φ龎pオΤлΡ鼿т):
    """'ip:port:user:pass' -> dict proxy cho requests."""
    fΑLΚJАA = 0
    fΑLΚJАA += 1
    try:
        raise MemoryError(fΑLΚJАA)
    except MemoryError as B鼫ъцπЩ齍ь:
        if B鼫ъцπЩ齍ь.args[0] == 1:
            try:
                _ = 1 / 0
            except ZeroDivisionError:
                I齀齕鼩υщᚠ齅ΝΡυA齖SΣ龖, f齽龎齤ソ鼴л龣龕, uε鼘鼵齂黹vюア, sβВ龐齓齼黳齞鼆λ齍鼏Ф龒鼼Β = F鼦黰Κ鼶Φ龎pオΤлΡ鼿т.split(':')
        if B鼫ъцπЩ齍ь.args[0] == 1:
            try:
                _ = 1 / 0
            except ZeroDivisionError:
                K鼒Ω鼪齦γ齾齘ΗΟJ龏т = f'http://{uε鼘鼵齂黹vюア}:{sβВ龐齓齼黳齞鼆λ齍鼏Ф龒鼼Β}@{I齀齕鼩υщᚠ齅ΝΡυA齖SΣ龖}:{f齽龎齤ソ鼴л龣龕}'
        if B鼫ъцπЩ齍ь.args[0] == 1:
            try:
                _ = 1 / 0
            except ZeroDivisionError:
                return {'http': K鼒Ω鼪齦γ齾齘ΗΟJ龏т, 'https': K鼒Ω鼪齦γ齾齘ΗΟJ龏т}
        if B鼫ъцπЩ齍ь.args[0] == 2:
            TNΦyタΣ鼿В = 5296
        if B鼫ъцπЩ齍ь.args[0] == 3:
            T齞鼱ωΔ龠龢鼝r = 6073
        if B鼫ъцπЩ齍ь.args[0] == 4:
            _齼Μᚱ黹и齥齙 = 9988


# ============================================================ WEB WRAPPER ===
# Chỉ thêm phần web, KHÔNG sửa logic gốc bên dưới

app = FastAPI()
LOG_BUFFER = []
IS_RUNNING = {"value": False}


def log(msg):
    """Ghi log vào buffer để hiển thị lên web."""
    print(msg)
    LOG_BUFFER.append(msg)
    if len(LOG_BUFFER) > 500:
        LOG_BUFFER.pop(0)


def run_registration(count):
    """Chạy y nguyên logic gốc, chỉ thay print -> log và input -> count."""
    IS_RUNNING["value"] = True
    LOG_BUFFER.clear()
    try:
        domain = requests.get('https://api.mail.tm/domains', timeout=10).json()['hydra:member'][0]['domain']
        log(Fore.YELLOW + f'\n[+] Domain: {domain}\n')

        success = 0
        for i in range(count):
            rand = random_name()
            email = f'{PREFIX}{rand}@{domain}'

            proxy_entry = random.choice(PROXIES)
            proxies = build_proxy(proxy_entry)

            try:
                resp = requests.post('https://api.mail.tm/accounts',
                                     json={'address': email, 'password': PASSWORD},
                                     headers=HEADERS, proxies=proxies, timeout=20)

                if resp.status_code == 201:
                    log(Fore.GREEN + f'[✓] SUCCESS | {email}')
                    with open(OUT_FILE, 'a', encoding='utf-8') as f:
                        f.write(f'{email}:{PASSWORD}\n')
                    success += 1
                else:
                    msg = resp.json().get('hydra:description', resp.text)
                    log(Fore.RED + f'[✗] FAIL | {email} | {msg}')
            except Exception as e:
                log(Fore.RED + f'[✗] ERROR | {email} | {e}')

            time.sleep(1.5)

        log(Style.BRIGHT + Fore.CYAN + f'\nHoàn tất! Thành công: {success}/{count}')

    except Exception as e:
        log(Fore.RED + f'❌ Lỗi: {e}')
    finally:
        IS_RUNNING["value"] = False


class RegRequest(BaseModel):
    count: int


@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mail.tm Registrar</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 40px 20px; min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex; align-items: flex-start; justify-content: center;
  }
  .card {
    width: 100%; max-width: 720px; background: #fff;
    border-radius: 20px; padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  }
  h1 { margin: 0 0 8px; font-size: 28px; color: #1a202c; }
  .sub { color: #718096; margin-bottom: 28px; font-size: 14px; }
  label { display: block; font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 8px; }
  input[type=number] {
    width: 100%; padding: 14px 16px; font-size: 16px;
    border: 2px solid #e2e8f0; border-radius: 10px; outline: none;
    transition: border-color .2s;
  }
  input[type=number]:focus { border-color: #667eea; }
  button {
    width: 100%; padding: 15px; font-size: 16px; font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff; border: none; border-radius: 10px; cursor: pointer;
    margin-top: 18px; transition: transform .1s, opacity .2s;
  }
  button:hover:not(:disabled) { transform: translateY(-2px); }
  button:disabled { opacity: .5; cursor: not-allowed; }
  #status {
    margin-top: 20px; padding: 14px 16px; border-radius: 10px;
    font-size: 14px; display: none;
  }
  .info { background: #ebf8ff; color: #2b6cb0; }
  .success { background: #f0fff4; color: #276749; }
  .error { background: #fff5f5; color: #c53030; }
  #logBox {
    margin-top: 20px; background: #1a202c; color: #e2e8f0;
    padding: 18px; border-radius: 12px; font-family: 'Monaco', monospace;
    font-size: 12.5px; line-height: 1.6; max-height: 420px; overflow-y: auto;
    white-space: pre-wrap; word-break: break-all; display: none;
  }
  #logBox::-webkit-scrollbar { width: 8px; }
  #logBox::-webkit-scrollbar-thumb { background: #4a5568; border-radius: 4px; }
  .stat { display: flex; gap: 12px; margin-top: 16px; }
  .stat div {
    flex: 1; padding: 12px; border-radius: 10px; text-align: center;
    background: #f7fafc; font-size: 13px; color: #4a5568;
  }
  .stat span { display: block; font-size: 22px; font-weight: 700; color: #2d3748; margin-top: 4px; }
  a.dl {
    display: inline-block; margin-top: 16px; padding: 12px 20px;
    background: #48bb78; color: #fff; text-decoration: none;
    border-radius: 10px; font-weight: 600; font-size: 14px;
  }
  a.dl:hover { background: #38a169; }
</style>
</head>
<body>
<div class="card">
  <h1>📧 Mail.tm Registrar</h1>
  <p class="sub">Đăng ký hàng loạt tài khoản mail tạm qua proxy</p>

  <label>Số lượng mail cần đăng ký</label>
  <input type="number" id="count" value="5" min="1" max="200">

  <button id="btn" onclick="startReg()">🚀 Bắt đầu đăng ký</button>

  <div id="status"></div>

  <div class="stat" id="stats" style="display:none;">
    <div>Tổng<span id="sTotal">0</span></div>
    <div>Thành công<span id="sOk" style="color:#38a169">0</span></div>
    <div>Thất bại<span id="sFail" style="color:#e53e3e">0</span></div>
  </div>

  <div id="logBox"></div>
  <a class="dl" id="dl" href="/download" style="display:none;">⬇️ Tải file kết quả</a>
</div>

<script>
let polling = null;

async function startReg() {
  const count = parseInt(document.getElementById('count').value);
  if (!count || count < 1) { alert('Nhập số hợp lệ!'); return; }

  const btn = document.getElementById('btn');
  const status = document.getElementById('status');
  const logBox = document.getElementById('logBox');
  const stats = document.getElementById('stats');
  const dl = document.getElementById('dl');

  btn.disabled = true;
  btn.textContent = '⏳ Đang chạy...';
  status.style.display = 'block';
  status.className = 'info';
  status.textContent = 'Đã bắt đầu, vui lòng chờ...';
  logBox.style.display = 'block';
  logBox.textContent = '';
  stats.style.display = 'flex';
  dl.style.display = 'none';
  document.getElementById('sTotal').textContent = count;
  document.getElementById('sOk').textContent = '0';
  document.getElementById('sFail').textContent = '0';

  try {
    await fetch('/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({count: count})
    });
  } catch(e) {
    status.className = 'error';
    status.textContent = '❌ Lỗi gửi yêu cầu: ' + e.message;
    btn.disabled = false;
    btn.textContent = '🚀 Bắt đầu đăng ký';
    return;
  }

  polling = setInterval(pollLog, 800);
}

async function pollLog() {
  const r = await fetch('/logs');
  const data = await r.json();

  const logBox = document.getElementById('logBox');
  logBox.textContent = data.lines.join('\\n');
  logBox.scrollTop = logBox.scrollHeight;

  let ok = 0, fail = 0;
  data.lines.forEach(l => {
    if (l.includes('SUCCESS')) ok++;
    else if (l.includes('FAIL') || l.includes('ERROR')) fail++;
  });
  document.getElementById('sOk').textContent = ok;
  document.getElementById('sFail').textContent = fail;

  if (!data.running && data.lines.length > 0) {
    clearInterval(polling);
    const btn = document.getElementById('btn');
    const status = document.getElementById('status');
    btn.disabled = false;
    btn.textContent = '🚀 Bắt đầu đăng ký';
    status.className = 'success';
    status.textContent = '✅ Hoàn tất!';
    document.getElementById('dl').style.display = 'inline-block';
  }
}
</script>
</body>
</html>
"""


@app.post("/register")
def register(req: RegRequest):
    if IS_RUNNING["value"]:
        return {"status": "busy", "msg": "Đang có tác vụ chạy"}
    t = threading.Thread(target=run_registration, args=(req.count,), daemon=True)
    t.start()
    return {"status": "started", "count": req.count}


@app.get("/logs")
def logs():
    # Loại bỏ mã màu ANSI để log hiển thị sạch
    import re
    clean = [re.sub(r'\x1b\[[0-9;]*m', '', l) for l in LOG_BUFFER]
    return {"running": IS_RUNNING["value"], "lines": clean}


@app.get("/download", response_class=PlainTextResponse)
def download():
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return "Chưa có dữ liệu"


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
