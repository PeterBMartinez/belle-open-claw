#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

LIST_ID = os.environ.get("CLICKUP_LIST_ID", "901708426264")
TOKEN = os.environ.get("CLICKUP_TOKEN")
TZ_NAME = os.environ.get("CLICKUP_TZ", "America/New_York")
STATE_PATH = Path(os.environ.get("CLICKUP_STATE_PATH", "/home/peter/.openclaw/state/clickup_new_tasks_today.json"))
MAX_PAGES = int(os.environ.get("CLICKUP_MAX_PAGES", "10"))
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6482200799:AAERIkgTNlhpuePDYWgzywMCydV2uFTP5cE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "849538467")


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def clickup_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": TOKEN})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def send_telegram(message: str) -> dict:
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_tasks_created_today(list_id: str, start_ms: int, end_ms: int):
    tasks = []
    seen_ids = set()
    for page in range(MAX_PAGES):
        params = urllib.parse.urlencode({
            "archived": "false",
            "page": page,
            "order_by": "created",
            "reverse": "true",
            "subtasks": "true",
        })
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task?{params}"
        data = clickup_get(url)
        page_tasks = data.get("tasks", [])
        if not page_tasks:
            break
        stop = False
        for task in page_tasks:
            task_id = task.get("id")
            created_raw = task.get("date_created")
            if not task_id or not created_raw:
                continue
            created_ms = int(created_raw)
            if created_ms < start_ms:
                stop = True
                continue
            if created_ms >= end_ms:
                continue
            if task_id not in seen_ids:
                seen_ids.add(task_id)
                tasks.append(task)
        if stop:
            break
    tasks.sort(key=lambda t: int(t.get("date_created", 0)))
    return tasks


def main():
    if not TOKEN:
        fail("CLICKUP_TOKEN is not set")

    tz = ZoneInfo(TZ_NAME)
    now = datetime.now(tz)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    start_ms = ms(start)
    end_ms = ms(end)
    day_key = start.date().isoformat()

    state = load_state()
    reported_today = set(state.get("reported_ids", [])) if state.get("day") == day_key else set()

    tasks = fetch_tasks_created_today(LIST_ID, start_ms, end_ms)
    new_tasks = [t for t in tasks if t.get("id") not in reported_today]

    payload = {
        "day": day_key,
        "list_id": LIST_ID,
        "timezone": TZ_NAME,
        "checked_at": now.isoformat(),
        "created_today_count": len(tasks),
        "new_since_last_check_count": len(new_tasks),
        "new_tasks": [
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "url": t.get("url"),
                "status": (t.get("status") or {}).get("status"),
                "creator": ((t.get("creator") or {}).get("username") or (t.get("creator") or {}).get("email")),
                "date_created": t.get("date_created"),
            }
            for t in new_tasks
        ],
    }

    print(json.dumps(payload, indent=2))

    if new_tasks:
        lines = [
            "<b>ClickUp Sprint Watcher</b>",
            f"<i>{day_key}</i>",
            "",
            f"<b>{len(new_tasks)}</b> new task(s) created today in list <code>{LIST_ID}</code>",
            "",
        ]
        for task in new_tasks[:15]:
            creator = ((task.get("creator") or {}).get("username") or (task.get("creator") or {}).get("email") or "unknown")
            status = ((task.get("status") or {}).get("status") or "unknown")
            name = (task.get("name") or "Untitled").replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f"• <b>{name}</b>")
            lines.append(f"  status: {status} | creator: {creator}")
            if task.get("url"):
                lines.append(task.get("url"))
            lines.append("")
        if len(new_tasks) > 15:
            lines.append(f"…and {len(new_tasks) - 15} more")
        try:
            tg_result = send_telegram("\n".join(lines))
            if tg_result.get("ok"):
                print(f"Telegram notification sent for {len(new_tasks)} new task(s)")
            else:
                print("Telegram notification failed", file=sys.stderr)
        except Exception as exc:
            print(f"Telegram notification failed: {exc}", file=sys.stderr)

    state = {
        "day": day_key,
        "reported_ids": sorted({*reported_today, *(t.get("id") for t in tasks if t.get("id"))}),
        "last_checked_at": now.isoformat(),
        "last_created_today_count": len(tasks),
    }
    save_state(state)


if __name__ == "__main__":
    main()
