# hackernewsscraper

## Overview
`hackernewsscraper` is a web scraping project that extracts data from Hacker News and stores it in a PostgreSQL database. The project includes several pipelines for processing the scraped data and a command-line interface (CLI) for interacting with the stored data.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yogiiieee/hackernewsscraper.git
    cd hackernewsscraper
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    ```
    Linux:
    ```
    source venv/bin/activate
    ```
    Windows:
    ```
    venv/Scripts/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    Create a `.env` file in the root directory and add your PostgreSQL database URL:
    ```env
    DATABASE_URL=postgresql://username:password@localhost:5432/database_name
    ```

## Usage
### Running the Scraper
To run the scraper, use the following command:
```sh
scrapy crawl hackernewsspider
```

## Command-Line Interface (CLI)
The CLI provides commands to list and aggregate posts stored in the database.

### List Posts
To list posts with optional limit, offset, and sorting:
```sh
python cli/cli.py list --limit 10 --offset 0 --sort_by points
```

### Aggregate Posts
To aggregate posts by date with a minimum number of posts:
```sh
python cli/cli.py aggr --greater_than 1
```

## Pipeline
The project includes several pipelines for processing the scraped data:
- HackernewsscraperPipeline: Default pipeline.
- ExtractCountAndDatePipeline: Extracts and formats the points, comments, and date fields.
- HandleMissingSubdataPipeline: Handles missing subdata fields.
- JSONFormatterPipeline: Formats the data into a JSON file.
- PostgresDBPipeline: Stores the data in a PostgreSQL database.