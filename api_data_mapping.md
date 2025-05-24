**API Data Mapping and Mock Endpoints**

This document outlines the mock API endpoints for simulating external data sources and details the mapping of data fields from the sample JSON responses (`sample_*.json`) to the operational database tables defined in `database_schemas.md`.

**General Mock API Base URL:** `/sim/v1` (Simulators will be hosted under this base path)

---

**1. Gaming Companies API**

*   **Mock Endpoint:** `GET /sim/v1/gamingco/{companyId}/revenue?reportDate={YYYY-MM-DD}`
    *   `{companyId}`: Path parameter for the company's unique identifier.
    *   `reportDate`: Query parameter for the specific date of the revenue report. If not provided, simulator might return latest or a sample.
*   **Sample JSON Source:** `sample_gaming_company_api.json`
    ```json
    {
      "companyId": "GAMCO-001",
      "reportDate": "2024-07-29",
      "totalSalesVolume": 1250000.75,
      "totalAmountRedeemed": 450000.50,
      "currency": "NGN"
    }
    ```
*   **Target Operational Database Table:** `revenue_data`
*   **Field Mapping:**
    | Sample JSON Field      | DB `revenue_data` Field | Notes                                                                 |
    |------------------------|-------------------------|-----------------------------------------------------------------------|
    | `companyId`            | `company_id`            | Link to `companies.company_id`. Assumes `companyId` exists in `companies` table. |
    | `reportDate`           | `report_date`           |                                                                       |
    | `totalSalesVolume`     | `total_sales_volume`    |                                                                       |
    | `totalAmountRedeemed`  | `amount_redeemed`       |                                                                       |
    | `currency`             | `currency`              |                                                                       |
    | *N/A*                  | `state_id`              | To be derived from the `companies` table (`companies.state_id` for the given `company_id`). |
    | *N/A*                  | `amount_taxable`        | Calculated: `total_sales_volume - amount_redeemed`.                     |
    | *Entire JSON object*   | `source_api_payload`    | Store the original payload for auditing.                                |

---

**2. NLRC (National Lottery Regulatory Commission) API**

*   **Mock Endpoint:** `GET /sim/v1/nlrc/licenses?companyId={companyId}`
    *   `companyId`: Query parameter for the company's unique identifier. If not provided, might return a list of all sample licenses.
*   **Sample JSON Source:** `sample_nlrc_api.json`
    ```json
    {
      "companyId": "GAMCO-001",
      "licenseNumber": "NLRC-LIC-00123",
      "companyName": "BestBet Nigeria PLC", // May be used for cross-referencing but primary link is companyId
      "licenseStatus": "Active",
      "issueDate": "2023-01-15",
      "expiryDate": "2025-01-14"
    }
    ```
*   **Target Operational Database Table:** `licenses`
*   **Field Mapping:**
    | Sample JSON Field | DB `licenses` Field | Notes                                                                 |
    |-------------------|---------------------|-----------------------------------------------------------------------|
    | `companyId`       | `company_id`        | Link to `companies.company_id`. Assumes `companyId` exists in `companies` table. |
    | `licenseNumber`   | `license_number`    |                                                                       |
    | `licenseStatus`   | `status`            |                                                                       |
    | `issueDate`       | `issue_date`        |                                                                       |
    | `expiryDate`      | `expiry_date`       |                                                                       |
    | *N/A*             | `last_synced_at`    | System timestamp when data is fetched.                                  |

---

**3. FIRS (Federal Inland Revenue Service) / State IRS API**

*   **Mock Endpoint:** `GET /sim/v1/irs/invoices?companyId={companyId}&taxType={taxType}`
    *   `companyId`: Query parameter.
    *   `taxType`: Query parameter ("State" or "FCT").
*   **Sample JSON Source:** `sample_firs_irs_api.json`
    ```json
    {
      "invoiceId": "INV-FCT-2024-00789", // External Invoice ID
      "companyId": "GAMCO-003",
      "taxPeriod": "2024-Q2", // May need parsing for start/end dates
      "taxType": "FCT", 
      "amountInvoiced": 75000.00,
      "amountPaid": 75000.00, // This field indicates payment status on the invoice itself
      "dateIssued": "2024-07-15",
      "dateDue": "2024-08-15",
      "paymentDate": "2024-08-10", // Date when amountPaid was settled
      "currency": "NGN"
    }
    ```
*   **Target Operational Database Tables:** `invoices`, `payments` (conditionally)
*   **Field Mapping (`invoices` table):**
    | Sample JSON Field  | DB `invoices` Field         | Notes                                                                 |
    |--------------------|-----------------------------|-----------------------------------------------------------------------|
    | `invoiceId`        | `external_invoice_number`   |                                                                       |
    | `companyId`        | `company_id`                | Link to `companies.company_id`.                                       |
    | `taxType`          | `tax_type`                  | e.g., "State Gaming Tax", "FCT Gaming Tax"                            |
    | `taxPeriod`        | `tax_period_start_date` / `tax_period_end_date` | Requires parsing logic (e.g., "2024-Q2" -> 2024-04-01 / 2024-06-30). |
    | `amountInvoiced`   | `amount_due`                |                                                                       |
    | `dateIssued`       | `date_issued`               |                                                                       |
    | `dateDue`          | `date_due`                  |                                                                       |
    | *N/A*              | `state_id`                  | Derived from `companies.state_id` or based on `taxType` (FCT is a specific state_id). |
    | *N/A*              | `last_synced_at`            | System timestamp.                                                       |

*   **Conditional Field Mapping (`payments` table, if `amountPaid` > 0 and `paymentDate` is present):**
    | Sample JSON Field      | DB `payments` Field           | Notes                                                                 |
    |------------------------|-------------------------------|-----------------------------------------------------------------------|
    | `invoiceId` (from above) | `invoice_id` (FK)             | Link to the created/updated invoice in `invoices` table.                |
    | `companyId`            | `company_id`                  | Link to `companies.company_id`.                                       |
    | `amountPaid`           | `amount_paid`                 |                                                                       |
    | `paymentDate`          | `payment_date`                |                                                                       |
    | `invoiceId`            | `external_payment_reference`| Use external invoice ID as reference if no other payment ref exists.    |
    | *N/A*                  | `reconciliation_status`       | Set to "Reconciled" if `amountPaid` >= `amountInvoiced`.                |
    | *N/A*                  | `last_synced_at`              | System timestamp.                                                       |
    *Note: This assumes the IRS API provides payment status per invoice. If Banks API is the sole source for payments, this mapping to `payments` table from IRS data might be omitted or handled differently.*

---

**4. Banks / Payment Gateways API**

*   **Mock Endpoint:** `GET /sim/v1/payments/transactions?companyId={companyId}&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}`
    *   `companyId`: Query parameter.
    *   `startDate`, `endDate`: Query parameters to fetch payments within a date range.
*   **Sample JSON Source:** `sample_bank_api.json`
    ```json
    {
      "paymentId": "BANKPAY-001-XYZ",
      "companyId": "GAMCO-001",
      "amountPaid": 50000.00,
      "paymentDate": "2024-07-28T10:30:00Z",
      "referenceNumber": "REF-STATE-INV-2024-001", // Used to link to an invoice
      "currency": "NGN"
    }
    ```
*   **Target Operational Database Table:** `payments`
*   **Field Mapping:**
    | Sample JSON Field   | DB `payments` Field           | Notes                                                                 |
    |---------------------|-------------------------------|-----------------------------------------------------------------------|
    | `paymentId`         | `external_payment_reference`  |                                                                       |
    | `companyId`         | `company_id`                  | Link to `companies.company_id`.                                       |
    | `amountPaid`        | `amount_paid`                 |                                                                       |
    | `paymentDate`       | `payment_date`                |                                                                       |
    | `referenceNumber`   | `invoice_id` (FK)             | Logic needed to map `referenceNumber` to an `invoices.invoice_id` or `invoices.external_invoice_number`. May require a lookup. If no direct link, `invoice_id` might be null initially. |
    | *N/A*               | `reconciliation_status`       | Set to "Pending" by default, updated by a separate reconciliation process. |
    | *N/A*               | `last_synced_at`              | System timestamp.                                                       |

---

This mapping will guide the development of the data ingestion modules and the API simulators.
