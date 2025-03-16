# Page Analyzer
A web app for checking websites for SEO suitability.
Demo: [Page Analyzer](https://python-project-83-i00p.onrender.com/)
### Hexlet tests and linter status:
[![Actions Status](https://github.com/starbuck007/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/starbuck007/python-project-83/actions)

##  Features
- URL validation
- HTTP response status code checking
- Extraction of key SEO elements (H1, title, meta description)
- History of checks for each URL
- List of all checked URLs with their latest check status

## Technologies
- Python 3.8+
- Flask
- PostgreSQL
- Bootstrap
- BeautifulSoup
- Psycopg
- Gunicorn
- Validators
- Dotenv
- Requests
- uv

## Installation

Clone the repository:
```bash
git clone https://github.com/username/page-analyzer.git
cd page-analyzer
```

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:
```bash
uv sync
```

Create `.env` file in the project root and add:
```
DATABASE_URL=postgresql://username:password@localhost:5432/page_analyzer
SECRET_KEY=your_secret_key
```

Create the database `page_analyzer`

## Usage

Start the development server:
```bash
make dev
```

For production use:
```bash
make start
```