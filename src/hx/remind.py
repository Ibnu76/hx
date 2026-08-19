"""Reminder system."""

import json
import click
from pathlib import Path
from datetime import datetime, timedelta

REMINDERS_FILE = Path.home() / ".hx" / "reminders.json"


def _load_reminders() -> list[dict]:
    if REMINDERS_FILE.exists():
        return json.loads(REMINDERS_FILE.read_text())
    return []


def _save_reminders(reminders: list[dict]) -> None:
    REMINDERS_FILE.parent.mkdir(exist_ok=True)
    REMINDERS_FILE.write_text(json.dumps(reminders, indent=2))


def list_active() -> list[dict]:
    return [r for r in _load_reminders() if not r.get("done")]


@click.group("remind", invoke_without_command=True)
@click.argument("text", nargs=-1, required=False)
@click.option("--in", "in_time", default=None, help="Remind in (e.g., 2h, 30m, 1d)")
@click.option("--at", "at_time", default=None, help="Remind at (e.g., 09:00)")
@click.option("--daily", is_flag=True, help="Repeat daily")
@click.pass_context
def remind_group(ctx, text, in_time, at_time, daily):
    """Set or list reminders."""
    if not text:
        # List mode
        active = list_active()
        if not active:
            click.echo("No active reminders.")
            return
        click.echo(f"\n📌 Active Reminders ({len(active)})\n")
        for r in active:
            click.echo(f"  {r['id']:>3}. {r['text']}")
        return

    content = " ".join(text)
    due = None
    if in_time:
        due = _parse_duration(in_time)
    elif at_time:
        due = _parse_time(at_time)

    reminders = _load_reminders()
    entry = {
        "id": len(reminders) + 1,
        "text": content,
        "due": due.isoformat() if due else None,
        "daily": daily,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    reminders.append(entry)
    _save_reminders(reminders)
    click.echo(f"✅ Reminder set: {content}")


@remind_group.command("done")
@click.argument("reminder_id", type=int)
def remind_done(reminder_id):
    """Mark reminder as done."""
    reminders = _load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r["done"] = True
            _save_reminders(reminders)
            click.echo(f"✅ Done: {r['text']}")
            return
    click.echo("Reminder not found", err=True)


def _parse_duration(s: str) -> datetime:
    """Parse '2h', '30m', '1d' into datetime."""
    now = datetime.now()
    num = int(s[:-1])
    unit = s[-1]
    if unit == "h":
        return now + timedelta(hours=num)
    elif unit == "m":
        return now + timedelta(minutes=num)
    elif unit == "d":
        return now + timedelta(days=num)
    return now + timedelta(hours=1)


def _parse_time(s: str) -> datetime:
    """Parse 'HH:MM' into today's datetime."""
    h, m = map(int, s.split(":"))
    now = datetime.now()
    target = now.replace(hour=h, minute=m, second=0)
    if target < now:
        target += timedelta(days=1)
    return target
