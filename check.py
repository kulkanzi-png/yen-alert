import json
import os
import time
import urllib.parse
import urllib.request

API = "https://open.er-api.com/v6/latest/JPY"
STATE_FILE = "state.json"

# 환경변수로 조정 가능 (기본값 사용 가능)
THRESHOLD = float(os.environ.get("THRESHOLD", "900"))        # 100엔당 원화, 이 금액 이하이면 알림
CHANGE_ALERT = float(os.environ.get("CHANGE_ALERT", "3"))    # 직전 확인 대비 이 금액 이상 변동 시 알림(원)
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def get_rate():
    """100엔당 원화 환율"""
    with urllib.request.urlopen(API, timeout=15) as r:
        data = json.load(r)
    return data["rates"]["KRW"] * 100


def send_telegram(text):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("텔레그램 설정이 없어 출력만 합니다:", text)
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    body = urllib.parse.urlencode({"chat_id": TG_CHAT_ID, "text": text}).encode()
    with urllib.request.urlopen(url, data=body, timeout=15) as r:
        r.read()


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"last_rate": None, "alerted": False}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    state = load_state()
    rate = get_rate()
    now = time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() + 9 * 3600))  # KST
    prev = state["last_rate"]
    messages = []

    if prev is not None:
        change = rate - prev
        if abs(change) >= CHANGE_ALERT:
            arrow = "📈" if change > 0 else "📉"
            messages.append(f"{arrow} 엔화 변동 {change:+.2f}원\n현재 100엔 = {rate:.2f}원")

    if rate <= THRESHOLD and not state["alerted"]:
        messages.append(f"🔔 기준 금액 이하입니다\n현재 100엔 = {rate:.2f}원 (기준 {THRESHOLD:.0f}원)")
        state["alerted"] = True
    elif rate > THRESHOLD and state["alerted"]:
        state["alerted"] = False  # 다시 올라오면 다음 하락 때 재알림

    print(f"[{now} KST] 100엔 = {rate:.2f}원 / 직전: {prev if prev is None else round(prev, 2)}")

    for m in messages:
        send_telegram(f"[엔화 알림 {now}]\n{m}")

    state["last_rate"] = rate
    save_state(state)


if __name__ == "__main__":
    main()
