"""Web scraping utilities."""

import click
import json
from pathlib import Path


@click.command("scrape")
@click.argument("url")
@click.option("--select", "-s", default=None, help="CSS selector to extract")
@click.option("--format", "fmt", default="text", type=click.Choice(["text", "md", "json", "html"]))
@click.option("--output", "-o", default=None, help="Output file")
def scrape_cmd(url, select, fmt, output):
    """Scrape a web page."""
    import urllib.request
    from html.parser import HTMLParser

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hx/0.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return

    if select:
        # Simple extraction (production would use beautifulsoup)
        result = _extract_selector(html, select)
    else:
        result = _html_to_text(html)

    if fmt == "json":
        output_text = json.dumps({"url": url, "content": result}, indent=2)
    elif fmt == "md":
        output_text = f"# {url}\n\n{result}"
    else:
        output_text = result

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(output_text)
        click.echo(f"✅ Saved to {output}")
    else:
        click.echo(output_text)


def _html_to_text(html: str) -> str:
    """Strip HTML tags, return plain text."""
    import re
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:5000]


def _extract_selector(html: str, selector: str) -> str:
    """Basic selector extraction (simplified)."""
    # In production, use beautifulsoup4
    return f"[selector extraction requires beautifulsoup4: pip install bs4]"
