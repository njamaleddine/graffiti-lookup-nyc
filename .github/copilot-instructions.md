# Copilot Instructions for Graffiti Lookup NYC

## Project Overview
This project provides a Python class and CLI for querying NYC 311 Graffiti Cleanup Requests. The main logic is in the `graffiti_lookup` package, with CLI entry in `graffiti_lookup/__main__.py`, API client logic in `graffiti_lookup/client.py`, and data models in `graffiti_lookup/models.py`.

## Architecture & Data Flow
- **CLI Entrypoint**: `graffiti_lookup/__main__.py` parses arguments and orchestrates requests using the `GraffitiLookup` class.
- **API Client**: `graffiti_lookup/client.py` implements the `GraffitiLookup` class with async HTTP requests to the NYC Graffiti Lookup endpoint, parses HTML responses, and returns structured data.
- **Data Model**: `graffiti_lookup/models.py` defines the `ServiceRequest` dataclass, handling date parsing (input format `%m/%d/%Y` → output format `%Y-%m-%d`) and serialization.
- **Output Formats**: Supports JSON and CSV output, with merging logic for updating files.
- **Testing**: Pytest-style test classes (no unittest.TestCase inheritance) with async test support via `@pytest.mark.asyncio`.

## Key Patterns & Conventions
- **Async HTTP**: Uses `httpx.AsyncClient` for non-blocking requests to external APIs.
- **HTML Parsing**: Relies on `BeautifulSoup` to extract tabular data from HTML responses.
- **ID Handling**: Service request IDs may start with "G"; code sanitizes this prefix before querying.
- **Date Handling**: Dates are parsed as `%m/%d/%Y` in the dataclass `__post_init__` and serialized as `%Y-%m-%d` for output.
- **Field Naming**: Output keys are converted to snake_case from HTML labels using `_convert_to_snake_case()`.
- **File I/O**: CLI supports reading/writing/merging JSON and CSV files, with fieldnames inferred from results.
- **Test Structure**: Uses pytest-style classes with `setup_method()` and `teardown_method()` instead of unittest setUp/tearDown.

## Module Structure
- **`client.py`**: API client wrapper for NYC Graffiti Lookup service (contains `GraffitiLookup` class).
- **`models.py`**: Data models for service requests (contains `ServiceRequest` dataclass).
- **`__main__.py`**: CLI entry point with argument parsing and file operations (contains `main()`, `read_file()`, `write_file()`).
- **`tests/test_client.py`**: Tests for the `GraffitiLookup` API client.
- **`tests/test_models.py`**: Tests for the `ServiceRequest` dataclass.
- **`tests/test_main_cli.py`**: Tests for CLI file operations and main function.

## Developer Workflows
- **Install dependencies**: `pip install -r requirements-dev.txt`
- **Run CLI**: `python -m graffiti_lookup --id "G2589"` or `--ids "G258700,G258801"`
- **Format output**: Pipe to `jq .` for readable JSON.
- **Run tests**: `pytest tests/` or `pytest tests/test_client.py -v`
- **Run with logging**: Enable debug logging to see HTTP requests and parsing details.

## Integration Points
- **External API**: NYC Graffiti Lookup endpoint (`https://a002-oomwap.nyc.gov/TagOnline/Shared/CannotRespond?sr=`)
- **Dependencies**: `httpx`, `beautifulsoup4`, `pytest`, `pytest-asyncio` (see `requirements.txt` and `requirements-dev.txt`)

## Examples
- **Fetch single request**: `python -m graffiti_lookup --id "G2589" | jq .`
- **Fetch multiple**: `python -m graffiti_lookup --ids "G258700,G258801" | jq .`
- **Save to file**: `python -m graffiti_lookup --ids "G258700,G258801" --file-path output.json --file-type json`
- **Merge with existing**: `python -m graffiti_lookup --ids ... --merge-file --file-path ...`
- **Run async tests**: `pytest tests/test_client.py -v` (uses `@pytest.mark.asyncio` for async test methods)

## Important Files
- `graffiti_lookup/client.py`: Core API client logic for making requests and parsing responses
- `graffiti_lookup/models.py`: ServiceRequest dataclass with date handling
- `graffiti_lookup/__main__.py`: CLI entrypoint with argument parsing and file I/O
- `tests/test_client.py`: Tests for GraffitiLookup class
- `tests/test_models.py`: Tests for ServiceRequest dataclass
- `tests/test_main_cli.py`: Tests for CLI functions (file operations, main function)
- `requirements.txt`, `requirements-dev.txt`: Dependencies
- `setup.cfg`: Pytest configuration with asyncio_mode, markers, and testpaths
- `README.md`: Usage examples and setup instructions

## Project-Specific Notes
- **Test Framework**: Uses pytest with pytest-style classes (no unittest inheritance) and `@pytest.mark.asyncio` for async tests. Configure with `setup.cfg` which includes `asyncio_mode = auto`.
- **Output Coupling**: Output fieldnames and formats are tightly coupled to the HTML structure of the external API; changes to the API may require HTML parser updates.
- **Async-First**: All client code is async; avoid blocking calls in `GraffitiLookup` methods.
- **CSV Field Names**: When writing CSV files with `write_file()`, use `isinstance(result, list)` to determine if writing multiple rows or a single row.
- **Date Format Flexibility**: Input dates are `%m/%d/%Y`, output dates are `%Y-%m-%d` for consistency across JSON and CSV formats.
- **ID Sanitization**: IDs with "G" prefix are automatically stripped before API queries but preserved in output data.

---
_Last updated: January 2026. If any section is unclear or needs updates, please provide feedback to improve these instructions._
