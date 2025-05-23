# Rockwell Automation Testing Guide

## How to Run the Stability Test (Simple Mode)

This test automatically checks several key steps in the Rockwell Automation web application to ensure its stability. You can easily run it from GitHub Actions.

### Steps to Run:

1. **Go to the "Actions" Tab**: On the main page of this repository on GitHub, find and click the "Actions" tab at the top.

2. **Select the Workflow**: In the left-hand menu, find and click on the workflow named "🤖Rockwell Automation General Tests".

3. **Start the Workflow**: You will see a button that says "Run workflow" on the right. Click on it.

4. **Choose the Server (URL Index)**: A field named "URL Index (e.g., 1-20) for testing" will appear. Here, you need to type the number of the specific server you want to test.

   **Which number to enter?** The number corresponds to the ftdspprodXXX server. For example:
   - If you want to test ftdspprod001, type `1`.
   - If you want to test ftdspprod005, type `5`.
   - If you want to test ftdspprod020, type `20`.

   Type only the number (without leading zeros if it's less than 10). The default value is 1.


5. **Run**: Click the green "Run workflow" button below the index field.

### What Happens Next?

The test will start running automatically. You can watch the progress in the same "Actions" tab.

- It will take several minutes to complete.
- Once finished (successfully or with errors), files called "Artifacts" will appear on the summary page of the run.
  - **test-logs-[index]**: Contains detailed log files from the execution.
  - **test-screenshots-[index]**: Contains screenshots taken during the test, especially if something failed.

You can download these files by clicking on their names.

That's it! With these steps, you can launch the test for the server you need.

## Automation Framework for Rockwell Automation

This framework uses Selenium with Python to automate tests on the Rockwell Automation website.

### Project Structure

- **config/**: Project configurations
- **pages/**: Page Object Model pattern implementation
- **tests/**: Test cases
- **utils/**: General utilities
- **reports/**: Execution reports (automatically generated)

### Prerequisites

- Python 3.8 or higher
- Browsers: Chrome, Firefox, Edge

### Environment Setup

Install dependencies: `pip install -r requirements.txt`

### Running Tests

To run all tests:
```
pytest tests/
```

To run a specific test case:
```
pytest tests/test_login.py --url-index=3
```

To run all test cases:
```
pytest tests/test_login.py --all-url
```

### Report Generation

Reports are automatically generated in the `reports/` folder after test execution.

### Parallelization

To run tests on multiple URLs in parallel, you can use pytest-xdist:

```
pip install pytest-xdist
```

And then run:

```
pytest tests/test_site_title.py --all-urls -n 4  # Runs in 4 parallel processes
```

### Author

Jose David Angarita Pertuz

### Flow Description:

1. **Start**: The test begins.
2. **Login**: Opens the page, handles Single Sign-On (SSO) if necessary, enters email and password.
3. **Project Creation**: Clicks "New Project", assigns a random name, and creates it. Closes a pop-up dialog (Dismiss).
4. **Validation & Copilot**: Verifies that the project syncs with GitLab and then uses Copilot to generate a smart object and a program.
5. **UI Verification**: Checks that certain interface elements (Device, Explorer, Library views, and the "Local changes" text) are present.
6. **Add Controller**: Navigates to the device view, adds a new controller (L85E), configures it, and finishes.
7. **Version Control (VCS)**: Commits the changes with an automatic message and then pushes to the repository.
8. **End**: Takes a final screenshot, and the test finishes.