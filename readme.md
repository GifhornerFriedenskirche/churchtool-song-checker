# Python Script for Retrieving and Analyzing JSON Data from an API

This Python script retrieves JSON data from an ChurchTool-API, parses it, identifies songs with missing ".sng" files in their arrangements, and categorizes them accordingly. It then outputs the results to predefined ChurchTool-Wiki-Page.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- `requests` library
- `python-dotenv` library

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
    API_URL=your_churchtools_baseurl_here
    USER_NAME=your_churchtools_username_here
    USER_PASSWORD=your_churchtools_password_here
    CATEGORIE=your_churchtools_category_id_here
    PAGE_TITLE=your_churchtools_page_title_here
    ```

    Replace `your_*_here` with your actual configuration.

## Usage

Run the script using the following command:

```bash
python songschecker.py
