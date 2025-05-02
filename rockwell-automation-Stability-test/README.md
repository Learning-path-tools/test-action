# Automation Framework for Rockwell Automation

This framework uses Selenium with Python to automate tests on the Rockwell Automation website.

## Project Structure

- `config/`: Project configurations
- `pages/`: Page Object Model pattern implementation
- `tests/`: Test cases
- `utils/`: General utilities
- `reports/`: Execution reports (automatically generated)

## Prerequisites

- Python 3.8 or higher
- Browsers: Chrome, Firefox, Edge

## Environment Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Running Tests

To run all tests:
```
pytest tests/
```

To run a specific test case:
```
pytest tests/test_login.py --url-index=3
```

To run a all test cases:
```
pytest tests/test_login.py --all-url

## Report Generation

Reports are automatically generated in the `reports/` folder after test execution.

## Parallelization

Parallelization: To run tests on multiple URLs in parallel, you can use pytest-xdist:
```
pip install pytest-xdist
```
And then run:
```
pytest tests/test_site_title.py --all-urls -n 4  # Runs in 4 parallel processes
```

## Author

Jose David Angarita Pertuz