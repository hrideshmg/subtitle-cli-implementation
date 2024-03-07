import pathlib

import bs4
import click
from imdb import Cinemagoer


@click.command()
@click.argument(
    "filename",
    type=click.Path(
        exists=True, dir_okay=False, writable=False, path_type=pathlib.Path
    ),
)
@click.option("-l", "--language", help="language to filter by")
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
    for index, movie in enumerate(movies, start=1):
        click.echo(f"{index}: {movie['title']}")
    chosen_index = click.prompt(
        "Which one of these is your movie?",
        type=click.IntRange(1, len(movies)),
        default=1,
    )
    imdb_id = movies[chosen_index].movieID

    print(imdb_id)


if __name__ == "__main__":
    find_sub()
