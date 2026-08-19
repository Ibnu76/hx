# hx

Personal CLI multitool. Notes, reminders, web scraping, quick math, and daily automation — all from one command.

## Install

```bash
pip install hx-cli
```

## Commands

### Notes

```bash
# Quick capture
hx note "idea: use merkle trees for config diffing"

# List recent
hx notes

# Search
hx notes -s "merkle"

# Tag-based
hx note "review PR #42" -t work
hx notes -t work

# Edit in $EDITOR
hx note edit 3
```

### Reminders

```bash
# Set reminder
hx remind "deploy staging" --in 2h
hx remind "standup" --at 09:00 --daily

# List active
hx reminders

# Done
hx remind done 5
```

### Scrape

```bash
# Quick page scrape to markdown
hx scrape https://docs.example.com/api --format md

# Extract specific selector
hx scrape https://news.ycombinator.com --select ".titleline > a" --format json

# Monitor page changes
hx watch https://status.example.com --interval 5m --notify

# Batch URLs from file
hx scrape --urls urls.txt --output results/
```

### Calculate

```bash
# Quick math
hx calc "1500 * 12 * 0.85"

# Unit conversion
hx calc "32 ETH in USD"
hx calc "500MB in GB"

# Date math
hx calc "2024-03-15 + 90 days"
```

### Clipboard

```bash
# Pipe-friendly
echo "data" | hx clip        # copy
hx clip                       # paste
hx clip --history             # clipboard history
```

### Daily

```bash
# Morning brief: weather, calendar, reminders, unread
hx daily

# Custom brief
hx daily --sections weather,reminders,github
```

## Storage

Everything lives in `~/.hx/` as plain-text JSON:

```
~/.hx/
├── notes.json        # all notes
├── reminders.json    # active + completed
├── scrape/           # cached scrape results
├── clips.json        # clipboard history
└── config.yaml       # preferences
```

## Config

```yaml
# ~/.hx/config.yaml
editor: nvim
date_format: "%Y-%m-%d %H:%M"

notifications:
  method: terminal  # or "telegram", "ntfy"
  
scrape:
  user_agent: "hx/0.1"
  timeout: 10
  
daily:
  sections: [weather, reminders, github]
  weather_city: "Jakarta"
```

## Pipes & Composability

```bash
# Feed scrape into notes
hx scrape https://api.example.com/status --format json | hx note --stdin -t monitoring

# Export notes as markdown
hx notes -t project --format md > project-notes.md

# Reminder from git log
git log --oneline -1 | hx remind --stdin --in 1h
```

## License

MIT
