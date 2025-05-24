# API Simulators for Revenue Monitoring Dashboard

This document provides instructions on how to run the mock API simulators for the National Gaming & Lottery Revenue Monitoring Dashboard project. These simulators mimic the behavior of external APIs that the main application will interact with.

## Prerequisites

Ensure you have Python installed. You will also need Flask.

**Install Flask:**
```bash
pip install Flask
```

## Running the Simulators

Each simulator is a standalone Flask application and should be run in a separate terminal window. They are configured to run on different ports to avoid collisions.

The sample JSON files (`sample_gaming_company_api.json`, `sample_nlrc_api.json`, `sample_firs_irs_api.json`, `sample_bank_api.json`) are expected to be in the same directory as the simulator Python scripts.

1.  **Gaming Company API Simulator**
    *   Serves data for company revenue.
    *   Runs on port `5001`.
    *   Command:
        ```bash
        python gaming_co_simulator.py
        ```

2.  **NLRC (License) API Simulator**
    *   Serves data for company licenses.
    *   Runs on port `5002`.
    *   Command:
        ```bash
        python nlrc_simulator.py
        ```

3.  **IRS (Invoices) API Simulator**
    *   Serves data for tax invoices.
    *   Runs on port `5003`.
    *   Command:
        ```bash
        python irs_simulator.py
        ```

4.  **Bank (Payments) API Simulator**
    *   Serves data for payment transactions.
    *   Runs on port `5004`.
    *   Command:
        ```bash
        python bank_simulator.py
        ```

## Mock API Endpoints Reference

Once running, the simulators provide the following endpoints:

1.  **Gaming Company API Simulator (Port 5001)**
    *   `GET /sim/v1/gamingco/{companyId}/revenue`
        *   Simulates fetching revenue data for a specific company.
        *   Example: `curl http://localhost:5001/sim/v1/gamingco/GAMCO-001/revenue`
        *   Path Parameter: `companyId` (e.g., `GAMCO-001` based on sample)
        *   Query Parameter (optional, ignored in basic sim): `reportDate` (e.g., `YYYY-MM-DD`)
        *   Occasionally returns a `500 Internal Server Error`.

2.  **NLRC API Simulator (Port 5002)**
    *   `GET /sim/v1/nlrc/licenses`
        *   Simulates fetching license data.
        *   Example: `curl http://localhost:5002/sim/v1/nlrc/licenses?companyId=GAMCO-001`
        *   Query Parameter: `companyId` (e.g., `GAMCO-001` based on sample)
        *   Occasionally returns a `503 Service Unavailable` error.

3.  **IRS API Simulator (Port 5003)**
    *   `GET /sim/v1/irs/invoices`
        *   Simulates fetching invoice data.
        *   Example: `curl http://localhost:5003/sim/v1/irs/invoices?companyId=GAMCO-003&taxType=FCT`
        *   Query Parameters:
            *   `companyId` (e.g., `GAMCO-003` based on sample)
            *   `taxType` (e.g., `FCT` based on sample)
        *   Occasionally returns a `429 Too Many Requests` error.

4.  **Bank API Simulator (Port 5004)**
    *   `GET /sim/v1/payments/transactions`
        *   Simulates fetching payment transaction data.
        *   Example: `curl http://localhost:5004/sim/v1/payments/transactions?companyId=GAMCO-001`
        *   Query Parameters:
            *   `companyId` (e.g., `GAMCO-001` based on sample)
            *   `startDate` (optional, ignored in basic sim, e.g., `YYYY-MM-DD`)
            *   `endDate` (optional, ignored in basic sim, e.g., `YYYY-MM-DD`)
        *   Occasionally returns a `401 Unauthorized` error.

## Notes

*   The simulators are designed to return data based on the content of their respective `sample_*.json` files.
*   The occasional errors are introduced randomly to help test the main application's error handling capabilities.
*   `debug=True` is enabled in the Flask apps, meaning changes to the Python files will automatically reload the simulator. For production simulation, `debug` should be `False`.
```
