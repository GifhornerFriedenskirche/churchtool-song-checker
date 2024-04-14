# ChurchTools Song Checker
[![CodeQL](https://github.com/GifhornerFriedenskirche/churchtool-song-checker/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/GifhornerFriedenskirche/churchtool-song-checker/actions/workflows/github-code-scanning/codeql)

This Python script retrieves JSON data from an ChurchTool-API, parses it, identifies songs with missing ".sng" files in their arrangements, and categorizes them accordingly. It then outputs the results to predefined ChurchTool-Wiki-Page.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- `requests` library
- `python-dotenv` library
- `dotenv` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/GifhornerFriedenskirche/churchtoolScripts.git
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following contents, based on the `.env.example` file:

    ```
    # basic configuration
    API_URL=your_churchtools_baseurl_here
    USER_NAME=your_churchtools_username_here
    USER_PASSWORD=your_churchtools_password_here
    
    # wiki related configuration
    UPDATE_WIKI=True|False # set to True if you want to update a wiki page with the status of the songs. If you want to use this, you need to create a wiki page first.
    CATEGORY=your_churchtools_wiki_category_here # id of the category where the page is located. Can be found in the URL of the wiki page.
    PAGE_TITLE=your_churchtools_wiki_page_title_here # title of the wiki page where the status of the songs will be updated.

    # tag related configuration
    MODIFY_TAGS=True|False # set to True if you want to modify tags
    TAG_MISSING_SNG=your_tag_for_missing_songs_here # tag that will be added to songs that are missing a sng file
    TAG_LICENCE_CHECK=Lizenz-prüfen # tag that will be added to songs that need a licence check
    ```

    Replace `your_*_here` with your actual configuration.
    Choose a value at the switches (`UPDATE_WIKI` and `MODIFY_TAGS`) `True` or `False`.

## Usage

Run the script using the following command:

```bash
python songschecker.py
```