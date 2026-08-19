"""Notes management."""

import json
import click
from pathlib import Path
from datetime import datetime

NOTES_FILE = Path.home() / ".hx" / "notes.json"


def _load_notes() -> list[dict]:
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text())
    return []


def _save_notes(notes: list[dict]) -> None:
    NOTES_FILE.parent.mkdir(exist_ok=True)
    NOTES_FILE.write_text(json.dumps(notes, indent=2))


def recent_notes(n: int = 10) -> list[dict]:
    notes = _load_notes()
    return sorted(notes, key=lambda x: x["created"], reverse=True)[:n]


@click.command("note")
@click.argument("text", nargs=-1)
@click.option("--tag", "-t", default=None, help="Tag the note")
@click.option("--stdin", is_flag=True, help="Read from stdin")
def note_cmd(text, tag, stdin):
    """Capture a quick note."""
    if stdin:
        import sys
        content = sys.stdin.read().strip()
    else:
        content = " ".join(text)

    if not content:
        click.echo("Error: empty note", err=True)
        return

    notes = _load_notes()
    entry = {
        "id": len(notes) + 1,
        "text": content,
        "tag": tag,
        "created": datetime.now().isoformat(),
    }
    notes.append(entry)
    _save_notes(notes)
    click.echo(f"✅ Note #{entry['id']} saved" + (f" [{tag}]" if tag else ""))


@click.command("notes")
@click.option("--search", "-s", default=None, help="Search notes")
@click.option("--tag", "-t", default=None, help="Filter by tag")
@click.option("--format", "fmt", default="text", type=click.Choice(["text", "json", "md"]))
@click.option("--limit", "-n", default=20, help="Max results")
def notes_group(search, tag, fmt, limit):
    """List and search notes."""
    notes = _load_notes()

    if tag:
        notes = [n for n in notes if n.get("tag") == tag]
    if search:
        notes = [n for n in notes if search.lower() in n["text"].lower()]

    notes = sorted(notes, key=lambda x: x["created"], reverse=True)[:limit]

    if fmt == "json":
        click.echo(json.dumps(notes, indent=2))
    elif fmt == "md":
        for n in notes:
            click.echo(f"- {n['text']}" + (f" `#{n['tag']}`" if n.get('tag') else ""))
    else:
        for n in notes:
            tag_str = f" [{n['tag']}]" if n.get("tag") else ""
            click.echo(f"  {n['id']:>3}. {n['text'][:70]}{tag_str}")
