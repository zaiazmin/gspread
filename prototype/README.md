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

1.  Start the application:
    ```bash
    python app.py
    ```
2.  Open your web browser and navigate to:
    ```
    http://localhost:5000
    ```

## Features Demonstrated

*   **Dark Industrial Theme:** UI styling matching professional CNC software (Haas/Siemens).
*   **Live Data Loading:** Fetches inventory data from `design_specs/sample_data.json`.
*   **Dashboard Metrics:** Calculates "Total Tools", "Inserts Stock", and "Low Stock Alerts" dynamically.
*   **Inventory Tables:** Displays the Tool Catalog and Active Low Stock warnings.

## Note

This is a prototype. The backend is a lightweight Flask wrapper around the static JSON dataset. Changes are not persisted to a database in this version.
