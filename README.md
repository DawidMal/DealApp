# Deal Finder

A lightweight FastAPI application that showcases how to compare product prices across multiple stores in an area. The service returns the cheapest price for every product along with the store that offers it.

## Features

- List supported areas with pricing data.
- Retrieve all products for an area and highlight the lowest price for each one.
- Query a specific product in an area to discover the cheapest store.

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to interact with the automatically generated Swagger UI.

### Running Tests

```bash
pytest
```

## Extending

The demo uses static in-memory data located in `app/data.py`. Replace this with calls to a database or external APIs to integrate real store pricing information.
