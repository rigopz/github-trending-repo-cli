# GitHub Trending CLI

A command-line tool to discover trending GitHub repositories by time range.

## Installation

```bash
git clone https://github.com/rigopz/github-trending-repo-cli.git
cd github-trending-cli
pip install -r requirements.txt
python main.py
```

## Usage

```bash
trending-repos [OPTIONS]
```

### Options

| Option       | Default | Description                                |
| ------------ | ------- | ------------------------------------------ |
| `--duration` | `week`  | Time range: `day`, `week`, `month`, `year` |
| `--limit`    | `10`    | Number of repositories to display (1–100)  |

### Examples

```bash
# Top 10 trending this week (default)
trending-repos

# Top 20 trending this month
trending-repos --duration month --limit 20

# Top 5 trending today
trending-repos --duration day --limit 5
```

## Requirements

- Python 3.8+
- `click`
- `requests`
- `rich`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Build .exe

```bash
pip install pyinstaller
pyinstaller --onefile --name trending-repos main.py
```

Output: `dist/trending-repos.exe`

## Notes

- Uses the [GitHub Search API](https://docs.github.com/en/rest/search/search) — no authentication required.
- Rate limit: 10 requests/minute unauthenticated.
- Results are sorted by star count in descending order.
