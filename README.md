## **Pirate's Dilemma**

Captain Jack Sparrow, a brave soul on the lookout for treasures, has recently laid his hands on the latest cinematic marvel from the vast expanse of[ archive.org](http://archive.org/). A true gem it be, a movie that promises laughter, tears, and the thrill of the high seas. Yet, in a twist of fate, our dear captain finds himself adrift without the crucial companion every movie marauder longs for – subtitles!

The quest is clear – to **scrape** the vast subtitle shores and uncover the hidden text that shall accompany their voyage.


## **Goal**

Create a[ CLI](https://en.wikipedia.org/wiki/Command-line_interface) app using Python that accepts an mp4 file and returns a list of subtitles for it, allowing the user to choose and download their preferred option.


## **Instructions**



* Set up a python virtual environment (venv) in the project folder and install the required modules inside of it
* Utilise the[ click](https://click.palletsprojects.com/en/8.1.x/) module for the CLI interface, the app should take the following parameters:
    1. -l, --language (to filter by language)
    2. -d, --download (automatically downloads top subtitle)
* Find the IMDb ID of the given movie
* Use beautifulsoup4 to scrape[ opensubtitles](https://www.opensubtitles.org/en/search/subs) and obtain the list of subtitles. Make sure to follow these guidelines:
    3. Searching should be done by using prior obtained IMDb ID
    4. Any filters specified by the options should be applied
    5. The results should be sorted by _“Download Times” _in descending order
* Prompt and download the chosen subtitle to the local directory
* Provide a clean user interface, complete with loading indicators and basic error handling
* Validate that the app works by testing it on this file:[ Movie](https://archive.org/download/plan-9-from-outer-space/plan-9-from-outer-space.mpeg4)

_Note: You may add more searching/filtering options like[ movie hash](https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes) if you can, these will add more value to your app_


## **Resources**



* [Open Subtitles](https://www.opensubtitles.org/en/search)
* [Click Documentation](https://click.palletsprojects.com/en/8.1.x/)
* [BS4 Documentation](https://www.crummy.com/software/BeautifulSoup/)

This is by no means an exhaustive list of references; don't be scared to Google and locate the rest yourself! After all, googling is a very important skill to learn for a developer :)
