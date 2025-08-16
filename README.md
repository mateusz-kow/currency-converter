# Currency Converter CLI Tool

A command-line interface (CLI) application for converting prices from various currencies to Polish Złoty (PLN). It fetches the latest exchange rates from either the National Bank of Poland (NBP) API or a local file and saves the conversion results to a JSON file or a SQLite database.

## Features

-   **Currency Conversion:** Convert any amount from a given currency (e.g., EUR, USD, CZK) to PLN.
-   **Multiple Data Sources:**
    -   `api`: Fetches real-time exchange rates from the NBP Web API.
    -   `db`: Reads exchange rates from a local JSON file (`example_currency_rates.json`).
-   **Persistent Storage:**
    -   `dev` mode: Saves conversion results to a human-readable `database.json` file.
    -   `prod` mode: Saves conversion results to a robust `database.db` SQLite database.
-   **Logging:** All operations are logged to `app.log` for easy debugging and auditing.
-   **Robust Error Handling:** Provides clear error messages and appropriate exit codes for different failure scenarios.

## Project Structure

```
currency-converter/
├── task/                   # Main application source code
│   ├── connectors/         # Modules for connecting to external data sources and databases
│   ├── utils/              # Helper modules for config, parsing, etc.
│   ├── currency_converter.py # Core conversion logic
│   └── __main__.py         # Application entry point
├── tests/                  # Unit tests for the application
├── database.json           # Default database for 'dev' mode
├── example_currency_rates.json # Local source for exchange rates
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Setup and Installation

### Prerequisites

-   Python 3.8+

### Installation Steps

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd currency-converter
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    # On Windows
    source venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The application is run from the command line using `python -m task`.

### Command-Line Arguments

-   `--currency <CODE>`: **(Required)** The 3-letter currency code (e.g., `EUR`).
-   `--price <AMOUNT>`: **(Required)** The amount of money to convert (e.g., `150.75`).
-   `--source <api|db>`: **(Required)** The source for the exchange rate (`api` for NBP, `db` for local file).
-   `--mode <dev|prod>`: (Optional) The database mode (`dev` for JSON, `prod` for SQLite). Defaults to `dev`.

### Examples

1.  **Convert 100 EUR to PLN using the NBP API and save to the JSON database:**
    ```sh
    python -m src --currency EUR --price 100 --source api --mode dev
    ```
    **Expected Output:**
    ```
    100.0 EUR = 428.55 PLN | rate: 4.2855 | date: 2023-10-26
    Database updated successfully
    ```

2.  **Convert 500 CZK to PLN using the local file rates and save to the SQLite database:**
    ```sh
    python -m src --currency CZK --price 500 --source db --mode prod
    ```
    **Expected Output:**
    ```
    500.0 CZK = 95.0 PLN | rate: 0.19 | date: 2023-09-01
    Database updated successfully
    ```

## Running Tests

To ensure all components are working correctly, you can run the built-in unit tests.

```sh
python -m tests
```