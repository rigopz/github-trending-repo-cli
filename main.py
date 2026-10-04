import click
import requests
from datetime import datetime, timedelta
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import sys
from requests.exceptions import RequestException
import msvcrt

def show_banner():
    text = Text()
    text.append("GitHub Trending CLI\n", style="bold cyan")
    text.append("Discover trending repositories on GitHub", style="dim")
    print(Panel(Align.center(text), border_style="cyan"))

def get_since_date(duration):
    days = {'day': 1, 'week': 7, 'month': 30, 'year': 365}
    delta = datetime.today() - timedelta(days=days[duration])
    return delta.strftime('%Y-%m-%d')

def parse_repos(items):
    return [
        {
            "name": repo["full_name"],
            "description": repo["description"] or "No description",
            "stars": repo["stargazers_count"],
            "language": repo["language"] or "Unknown",
            "url": repo["html_url"],
        }
        for repo in items
    ]

def fetch_repos(duration, limit):
    since = get_since_date(duration)
    params = {
        "q": f"created:>{since}",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    try:
        response = requests.get("https://api.github.com/search/repositories", params=params)
        response.raise_for_status()
        return parse_repos(response.json()["items"])
    except RequestException as e:
        print(f"[red]API error:[/red] {e}")
        sys.exit(1)

def display_repos(repos):
    table = Table(title="Trending Repositories",show_lines=True)
    table.add_column("#", style="dim")
    table.add_column("Repo", style="cyan")
    table.add_column("Stars", style="yellow")
    table.add_column("Language", style="green")
    table.add_column("Description")
    table.add_column("Link", style="bright_blue")
    
    for i, repo in enumerate(repos, 1):
        table.add_row(str(i), repo["name"], str(repo["stars"]), repo["language"], repo["description"], repo["url"])
        
    print(table)

@click.command()
@click.option('--duration', default='week', type=click.Choice(['day', 'week', 'month', 'year']), show_default=True,prompt=True)
@click.option('--limit', default=10, type=click.IntRange(1, 100), show_default=True,prompt=True)
def main(duration, limit):
    show_banner()
    repos = fetch_repos(duration, limit)
    display_repos(repos)
    print("\nPress any key to exit...")
    msvcrt.getch()

if __name__ == '__main__':
    main()