# CNC Inventory System - Prototype

This is a **Functional Proof of Concept (PoC)** of the dashboard designed in `design_specs/CNC_INVENTORY_DESIGN.md`.
It serves as a "Runnable" version of the design to visualize the User Interface and Data Architecture.

## Prerequisites

*   Python 3.x
*   Pip

## Installation

1.  Navigate to the `prototype` directory:
    ```bash
    cd prototype
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Initialize the database (first run only):
    ```bash
    python init_db.py
    ```
    *This creates `inventory.db` and seeds it with data from `../design_specs/sample_data.json`.*

2.  Start the application:
    ```bash
    python app.py
    ```

3.  Open your web browser and navigate to:
    ```
    http://localhost:5000
    ```

## Testing

This project includes a test suite using `pytest`.

To run the tests:
```bash
pytest
```

## Features Demonstrated

*   **Dark Industrial Theme:** UI styling matching professional CNC software (Haas/Siemens).
*   **Database Integration:** Uses SQLite and SQLAlchemy to store and retrieve inventory data.
*   **Dashboard Metrics:** Calculates "Total Tools", "Inserts Stock", and "Low Stock Alerts" dynamically from the database.
*   **Inventory Tables:** Displays the Tool Catalog and Active Low Stock warnings.

## Note

This is a prototype. It uses a local SQLite database (`inventory.db`) which is persistent between runs. To reset the data, simply delete `inventory.db` and run `python init_db.py` again.
