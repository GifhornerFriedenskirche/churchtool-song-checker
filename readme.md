# Python Script for Retrieving and Analyzing JSON Data from an API

This Python script retrieves JSON data from an ChurchTool-API, parses it, identifies songs with missing ".sng" files in their arrangements, and categorizes them accordingly. It then outputs the results to a Markdown file.

## Prerequisites

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

3. Create a `.env` file in the root directory with the following contents:

    ```
    AUTH_TOKEN=your_auth_token_here
    API_URL=your_churchtool_baseurl_here
    ```

    Replace `your_auth_token_here` with your actual authentication token and `your_churchtool_baseurl_here` with the API endpoint URL.

## Usage

Run the script using the following command:

```bash
python songschecker.py
