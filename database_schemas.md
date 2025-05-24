**Preliminary Database Schemas**

This document outlines the preliminary conceptual schemas for the operational database (PostgreSQL) and the Data Warehouse. These are subject to refinement during detailed design and implementation.

**Part 1: Operational Database (PostgreSQL)**

The operational database is designed for transactional data, user management, and current state information.

**1. `users` Table**
    *   `user_id` (UUID, Primary Key)
    *   `username` (VARCHAR, Unique, Not Null)
    *   `password_hash` (VARCHAR, Not Null)
    *   `email` (VARCHAR, Unique, Not Null)
    *   `first_name` (VARCHAR)
    *   `last_name` (VARCHAR)
    *   `role_id` (UUID, Foreign Key to `roles` table)
    *   `state_id` (UUID, Foreign Key to `states` table, Nullable - only if role is State Admin or Auditor for a specific state)
    *   `is_active` (BOOLEAN, Default: True)
    *   `last_login` (TIMESTAMP)
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**2. `roles` Table**
    *   `role_id` (UUID, Primary Key)
    *   `role_name` (VARCHAR, Unique, Not Null) - e.g., "Federal Super Admin", "State Admin", "Auditor/Analyst"
    *   `permissions` (JSONB, Nullable) - Detailed permissions if not fully implicit by role_name.
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**3. `states` Table (Includes FCT)**
    *   `state_id` (UUID, Primary Key)
    *   `state_name` (VARCHAR, Unique, Not Null) - e.g., "Lagos", "Kano", "FCT Abuja"
    *   `current_tax_percentage` (DECIMAL, Nullable) - Configurable by Federal Admin. For FCT, this is the FCT tax.
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**4. `companies` Table**
    *   `company_id` (UUID, Primary Key) - Could also be a unique string if companies have existing identifiers.
    *   `company_name` (VARCHAR, Not Null)
    *   `registration_number` (VARCHAR, Unique)
    *   `contact_email` (VARCHAR)
    *   `contact_phone` (VARCHAR)
    *   `address` (TEXT)
    *   `state_id` (UUID, Foreign Key to `states` table) - State of operation / incorporation.
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**5. `licenses` Table (Data from NLRC)**
    *   `license_id` (UUID, Primary Key)
    *   `company_id` (UUID, Foreign Key to `companies` table)
    *   `license_number` (VARCHAR, Unique, Not Null)
    *   `status` (VARCHAR, Not Null) - e.g., "Active", "Expired", "Suspended", "Unlicensed"
    *   `issue_date` (DATE)
    *   `expiry_date` (DATE)
    *   `last_synced_at` (TIMESTAMP) - From NLRC API
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**6. `revenue_data` Table (Aggregated from Gaming Companies)**
    *   `revenue_data_id` (UUID, Primary Key)
    *   `company_id` (UUID, Foreign Key to `companies` table)
    *   `state_id` (UUID, Foreign Key to `states` table) - State where revenue was generated
    *   `report_date` (DATE, Not Null)
    *   `total_sales_volume` (DECIMAL, Not Null)
    *   `amount_redeemed` (DECIMAL, Not Null)
    *   `amount_taxable` (DECIMAL, Calculated: `total_sales_volume - amount_redeemed`)
    *   `currency` (VARCHAR(3), Default: "NGN")
    *   `source_api_payload` (JSONB, Nullable) - To store raw payload from company for audit/reconciliation
    *   `ingested_at` (TIMESTAMP, Default: NOW())
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())
    *   *Index on (`company_id`, `report_date`)*
    *   *Index on (`state_id`, `report_date`)*

**7. `invoices` Table (Data from FIRS/State IRS)**
    *   `invoice_id` (UUID, Primary Key) - Or use external invoice ID if consistently unique.
    *   `external_invoice_number` (VARCHAR, Unique, Not Null)
    *   `company_id` (UUID, Foreign Key to `companies` table)
    *   `state_id` (UUID, Foreign Key to `states` table) - Issuing state (or FCT)
    *   `tax_type` (VARCHAR) - e.g., "State Gaming Tax", "FCT Gaming Tax"
    *   `tax_period_start_date` (DATE)
    *   `tax_period_end_date` (DATE)
    *   `amount_due` (DECIMAL, Not Null)
    *   `date_issued` (DATE)
    *   `date_due` (DATE)
    *   `last_synced_at` (TIMESTAMP) - From FIRS/IRS API
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**8. `payments` Table (Data from Banks/Payment Gateways or FIRS/State IRS)**
    *   `payment_id` (UUID, Primary Key)
    *   `invoice_id` (UUID, Foreign Key to `invoices` table, Nullable if payment cannot be directly reconciled)
    *   `external_payment_reference` (VARCHAR, Unique)
    *   `company_id` (UUID, Foreign Key to `companies` table)
    *   `amount_paid` (DECIMAL, Not Null)
    *   `payment_date` (TIMESTAMP, Not Null)
    *   `payment_method` (VARCHAR, Nullable)
    *   `reconciliation_status` (VARCHAR, Default: "Pending") - e.g., "Pending", "Reconciled", "Partial"
    *   `last_synced_at` (TIMESTAMP)
    *   `created_at` (TIMESTAMP, Default: NOW())
    *   `updated_at` (TIMESTAMP, Default: NOW())

**9. `audit_logs` Table**
    *   `log_id` (BIGSERIAL, Primary Key) - Using BIGSERIAL for high volume.
    *   `user_id` (UUID, Foreign Key to `users` table, Nullable for system actions)
    *   `timestamp` (TIMESTAMP WITH TIME ZONE, Default: NOW())
    *   `action_type` (VARCHAR, Not Null) - e.g., "LOGIN", "VIEW_REPORT", "UPDATE_TAX_RATE", "API_DATA_INGESTION"
    *   `target_entity_type` (VARCHAR, Nullable) - e.g., "Company", "User", "StateTaxRate"
    *   `target_entity_id` (VARCHAR, Nullable)
    *   `details` (JSONB, Nullable) - For additional context, parameters, old/new values.
    *   `ip_address` (VARCHAR, Nullable)
    *   `status` (VARCHAR) - e.g., "SUCCESS", "FAILURE"

**Part 2: Data Warehouse (DWH) Schema (Conceptual)**

The DWH is designed for analytical queries and will likely use a star or snowflake schema. Data is ETL'd from the operational DB.

**1. `FactRevenue` Table**
    *   `revenue_fact_id` (PK)
    *   `date_key` (FK to `DimDate`) - Day of revenue report
    *   `company_key` (FK to `DimCompany`)
    *   `state_key` (FK to `DimState`)
    *   `license_key` (FK to `DimLicense`) - License status at the time of revenue
    *   `total_sales_volume` (DECIMAL)
    *   `amount_redeemed` (DECIMAL)
    *   `amount_taxable` (DECIMAL)
    *   `calculated_amount_due_state` (DECIMAL) - Based on state tax % at the time
    *   `calculated_amount_due_fct` (DECIMAL) - Based on FCT tax % at the time (if applicable)
    *   `ingestion_timestamp` (TIMESTAMP)

**2. `FactPayments` Table**
    *   `payment_fact_id` (PK)
    *   `invoice_date_key` (FK to `DimDate`) - Date invoice was issued
    *   `payment_date_key` (FK to `DimDate`) - Date payment was made
    *   `due_date_key` (FK to `DimDate`)
    *   `company_key` (FK to `DimCompany`)
    *   `state_key` (FK to `DimState`) - Issuing state/FCT of invoice
    *   `amount_invoiced` (DECIMAL)
    *   `amount_paid` (DECIMAL)
    *   `days_to_pay` (INTEGER)
    *   `is_late_payment` (BOOLEAN)

**3. `DimDate` Dimension Table**
    *   `date_key` (PK, e.g., YYYYMMDD)
    *   `full_date` (DATE)
    *   `day_of_week` (VARCHAR)
    *   `month` (INTEGER)
    *   `quarter` (INTEGER)
    *   `year` (INTEGER)

**4. `DimCompany` Dimension Table**
    *   `company_key` (PK)
    *   `company_id_operational` (UUID) - Link back to operational DB's company_id
    *   `company_name` (VARCHAR)
    *   `registration_number` (VARCHAR)
    *   Other relevant company attributes that change slowly.

**5. `DimState` Dimension Table (Includes FCT)**
    *   `state_key` (PK)
    *   `state_id_operational` (UUID) - Link back to operational DB's state_id
    *   `state_name` (VARCHAR)
    *   `current_tax_percentage` (DECIMAL) - Could be snapshot if it changes over time and needs historical accuracy.

**6. `DimLicense` Dimension Table**
    *   `license_key` (PK)
    *   `license_id_operational` (UUID)
    *   `license_number` (VARCHAR)
    *   `status` (VARCHAR)
    *   `issue_date` (DATE)
    *   `expiry_date` (DATE)
    *   `valid_from` (DATE) - For SCD Type 2 if tracking history of license changes
    *   `valid_to` (DATE) - For SCD Type 2

**Notes on DWH:**
*   The DWH schema will be populated by ETL processes from the operational database.
*   Dimension tables will handle historical changes using Slowly Changing Dimensions (SCD) techniques where appropriate (e.g., for company details, license status changes over time).
*   Further aggregation tables might be created for very common dashboard queries to improve performance.

This preliminary schema provides a starting point. It will evolve as implementation details are worked out and specific query patterns for analytics become clearer.
