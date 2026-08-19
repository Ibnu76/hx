"""Quick calculations and conversions."""

import click
import re


@click.command("calc")
@click.argument("expression", nargs=-1)
def calc_cmd(expression):
    """Quick math, conversions, date arithmetic."""
    expr = " ".join(expression)

    # Date math
    if "days" in expr or "weeks" in expr or "months" in expr:
        result = _date_math(expr)
    # Unit conversion
    elif " in " in expr:
        result = _convert(expr)
    # Plain math
    else:
        result = _math(expr)

    click.echo(result)


def _math(expr: str) -> str:
    """Evaluate math expression safely."""
    # Only allow safe characters
    allowed = set("0123456789.+-*/() %")
    clean = "".join(c for c in expr if c in allowed)
    try:
        return str(eval(clean))  # noqa: S307
    except Exception as e:
        return f"Error: {e}"


def _convert(expr: str) -> str:
    """Basic unit conversion."""
    match = re.match(r"([\d.]+)\s*(\w+)\s+in\s+(\w+)", expr)
    if not match:
        return "Format: <value> <from_unit> in <to_unit>"

    value, from_u, to_u = float(match.group(1)), match.group(2).upper(), match.group(3).upper()

    conversions = {
        ("MB", "GB"): 1 / 1024,
        ("GB", "MB"): 1024,
        ("GB", "TB"): 1 / 1024,
        ("KB", "MB"): 1 / 1024,
        ("KG", "LBS"): 2.205,
        ("LBS", "KG"): 0.4536,
    }

    key = (from_u, to_u)
    if key in conversions:
        return f"{value * conversions[key]:.4f} {to_u}"
    return f"Unknown conversion: {from_u} → {to_u}"


def _date_math(expr: str) -> str:
    """Date arithmetic."""
    from datetime import datetime, timedelta
    match = re.match(r"(.+?)\s*[+\-]\s*(\d+)\s*(days?|weeks?|months?)", expr)
    if not match:
        return "Format: <date> +/- <n> days/weeks/months"

    date_str, num, unit = match.group(1).strip(), int(match.group(2)), match.group(3)
    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()

    if "day" in unit:
        delta = timedelta(days=num)
    elif "week" in unit:
        delta = timedelta(weeks=num)
    else:
        delta = timedelta(days=num * 30)

    if "-" in expr:
        result = date - delta
    else:
        result = date + delta

    return result.strftime("%Y-%m-%d %H:%M")
