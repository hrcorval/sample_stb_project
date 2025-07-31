# Test Automation Framework

## Overview

This is a test automation framework built with Python, Selenium, and Behavex for behavior-driven development (BDD).

## Setup

1. Install Python 3.10+
2. Install dependencies: `pipenv install`
3. Activate virtual environment: `pipenv shell`

## Running Tests

```bash
# Run all tests
behavex

# Run specific feature
behavex features/login.feature

# Run with tags
behavex --tags=@CHECKOUT

# Run tests in parallel
behavex --parallel-processes=4

# Run with specific output format
behavex --output=output
```

## Sample Project Structure

```
├── features/
│   ├── login.feature
│   ├── steps/
│   │   ├── login_steps.py
│   │   └── pages/
│   │       ├── base_page.py
│   │       ├── login_page.py
│   │       └── web_utils.py
│   └── environment.py
├── config/
│   └── config.cfg
├── .cursorrules
├── .pre-commit-config.yaml
├── Pipfile
└── README.md
```

## Guidelines

- Follow the Page Object Model pattern
- Use meaningful step definitions
- Tag scenarios appropriately
- Write clean, maintainable code
- Use behavex for parallel test execution 