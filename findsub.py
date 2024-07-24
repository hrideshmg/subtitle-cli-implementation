import os
import pathlib
import re
import os
from hasher import hashFile_url
from hasher import hashFile_url
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
            first_column = row.find("td", id=re.compile("^main"))
            file_info = first_column.find("span")
            if file_info:
                file_info = file_info["title"]
            else:
                file_info = first_column.find("a").text
            download_link = ROOT_URL + row.find_all("td")[4].a["href"]
            subtitles.append((file_info.replace("\n", " "), download_link))
    except Exception as e:
        print(e)
    return subtitles


def download_subtitle(name, url, output):
    subtitle_data = requests.get(url).content
    path = os.path.join(output, name)
    with open(path, "wb") as file:
        file.write(subtitle_data)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, writable=False, path_type=pathlib.Path),
)
@click.option(
    "-l",
    "--language",
    default="all",
    help="language to filter by, codes specified by ISO 639-2",
)
@click.option(
    "-s", "--file-size", default=False, is_flag=True, help="filter by the file bytesize"
)
@click.option(
    "-h", "--match-by-hash", default=False, is_flag=True, help="filter by the file hash"
)
@click.option(
    "-b",
    "--batch-download",
    default=False,
    is_flag=True,
    help="Enables batch download, specify directory instead of file",
)
@click.option(
    "-o",
    "--output",
    help="specifies the output directory for the subtitle",
    default=".",
    type=click.Path(exists=True, dir_okay=True, path_type=pathlib.Path),
)
def cli(path, language, file_size, match_by_hash, batch_download, output):
    """Finds the Subtitle given the filename"""

    def find_sub(filename):
        searcher = Cinemagoer()
        movies = searcher.search_movie(filename)
        if not movies:
            click.echo("Could not find IMDb Entry for this movie!")
            return
        imdb_id = movies[0].movieID

        query_url = ROOT_URL + f"/en/search/sublanguageid-{language}/imdbid-{imdb_id}"
        if file_size:
            bytes = os.path.getsize(file)
            query_url += f"/moviebytesize-{bytes}"
        if match_by_hash:
            file_hash = hashFile_url(file)
            query_url += f"/moviehash-{file_hash}"
        query_url += "/sort-7/asc-0"

        return scrape_webpage(query_url)

    if batch_download:
        if not os.path.isdir(path):
            click.echo("Given path is not a directory!")
        else:
            files = os.listdir(path)
            for file in files:
                subtitles = find_sub(file.split(".")[0])
                if not subtitles:
                    click.echo(
                        f"Could not find any subtitles for {path} with specified filters!"
                    )
                else:
                    name, url = subtitles[0]
                    download_subtitle(os.path.join(path, name), url)

    else:
        filename = path.stem
        subtitles = find_sub(filename)
        if not subtitles:
            click.echo(
                f"Could not find any subtitles for {path} with specified filters!"
            )
            return

        for index, subtitle in enumerate(subtitles, start=1):
            click.echo(f"{index}: {subtitle[0]}")
        chosen_index = click.prompt(
            "Which subtitle would you like to download?",
            type=click.IntRange(1, len(subtitles)),
            default=1,
        )
        name, url = subtitles[chosen_index - 1]
        download_subtitle(name, url, output)


if __name__ == "__main__":
    cli()
