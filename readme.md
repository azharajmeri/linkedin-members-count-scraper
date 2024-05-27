# LinkedIn Scraper

This project is a LinkedIn scraper that extracts member details from a 
list of companies provided in an Excel file.

## Requirements

- Python 3.12

## Installation

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuration

Update the `config.py` file with your LinkedIn credentials and file paths:

```python
LINKEDIN_EMAIL = "your_linkedin_email"
LINKEDIN_PASSWORD = "your_linkedin_password"
INPUT_FILE_PATH = "./input/List of companies 5.xlsx"
OUTPUT_FILE_PATH = "./output/members_details.xlsx"
```

## Usage

Run the scraper script:

- For Windows:

```bash
python main.py
```

- For Ubuntu:

```bash
python3 main.py
```
