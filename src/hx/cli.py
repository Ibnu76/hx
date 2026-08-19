"""Main CLI entrypoint."""

import click
from pathlib import Path

from hx.notes import notes_group, note_cmd
from hx.remind import remind_group
from hx.scrape import scrape_cmd
from hx.calc import calc_cmd

HX_DIR = Path.home() / ".hx"


@click.group()
@click.version_option()
def cli():
    """Personal CLI multitool."""
    HX_DIR.mkdir(exist_ok=True)


cli.add_command(note_cmd, "note")
cli.add_command(notes_group, "notes")
cli.add_command(remind_group, "remind")
cli.add_command(scrape_cmd, "scrape")
cli.add_command(calc_cmd, "calc")


@cli.command()
@click.option("--sections", "-s", default="reminders,notes", help="Comma-separated sections")
def daily(sections: str):
    """Morning brief: reminders, recent notes, weather."""
    parts = [s.strip() for s in sections.split(",")]
    click.echo("\n☀️  Daily Brief\n" + "─" * 40)
    
    if "reminders" in parts:
        from hx.remind import list_active
        active = list_active()
        click.echo(f"\n📌 Reminders ({len(active)} active)")
        for r in active[:5]:
            click.echo(f"   • {r['text']}")

    if "notes" in parts:
        from hx.notes import recent_notes
        notes = recent_notes(5)
        click.echo(f"\n📝 Recent Notes")
        for n in notes:
            click.echo(f"   • {n['text'][:60]}")

    click.echo()


if __name__ == "__main__":
    cli()
