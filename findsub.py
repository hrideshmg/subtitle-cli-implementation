import pathlib
import re

import click
import requests
from bs4 import BeautifulSoup
from imdb import Cinemagoer

ROOT_URL = "https://www.opensubtitles.org"


def scrape_webpage(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    results_table = soup.find("table", id="search_results")

    subtitles = []
    try:
        for row in results_table.find_all("tr", id=re.compile("^name")):
            file_info = (
                row.find("td", id=re.compile("^main")).find("br").next_sibling.strip()
            )
            download_link = ROOT_URL + row.find_all("td")[4].a["href"]
            subtitles.append((file_info, download_link))
    except:
        pass
    return subtitles


def download_subtitle(name, url):
    subtitle_data = requests.get(url).content
    with open(name, "wb") as file:
        file.write(subtitle_data)


@click.command()
@click.argument(
    "filename",
    type=click.Path(
        exists=True, dir_okay=False, writable=False, path_type=pathlib.Path
    ),
)
@click.option(
    "-l",
    "--language",
    default="all",
    help="language to filter by, codes specified by ISO 639-2",
)
@click.option(
    "-d",
    "--download",
    default=False,
    is_flag=True,
    help="downloads top subtitle automatically",
)
def find_sub(filename, language, download):
    """Finds the Subtitle given the filename"""

    # removes the path and extension from filename
    filename = filename.stem

    searcher = Cinemagoer()
    movies = searcher.search_movie(filename)
    if not movies:
        click.echo("Could not find IMDb Entry for this movie!")
        return
    imdb_id = movies[0].movieID

    query_url = (
        ROOT_URL + f"/en/search/sublanguageid-{language}/imdbid-{imdb_id}/sort-7/asc-0"
    )
    subtitles = scrape_webpage(query_url)

    if not subtitles:
        click.echo("Could not find any subtitles for movie with specified filters!")
        return

    # If download option is specified don't prompt user with list of subtitles
    if download:
        name, url = subtitles[0]
        download_subtitle(name, url)
    else:
        for index, subtitle in enumerate(subtitles, start=1):
            click.echo(f"{index}: {subtitle[0]}")
        chosen_index = click.prompt(
            "Which subtitle would you like to download?",
            type=click.IntRange(1, len(movies)),
            default=1,
        )
        name, url = subtitles[chosen_index]
        download_subtitle(name, url)


if __name__ == "__main__":
    find_sub()
