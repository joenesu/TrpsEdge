**System Architecture and Data Flow**

This document outlines the proposed system architecture, data flow, and data synchronization strategies for the National Gaming & Lottery Revenue Monitoring Dashboard.

**1. High-Level System Architecture Components**

The system will be composed of the following key components:

*   **Frontend Application:**
    *   **Technology:** React.js (as per `technology_stack_proposal.md`).
    *   **Function:** User interface for administrators and analysts. Displays dashboards, reports, visualizations, alerts. Allows data interaction based on user roles (viewing, managing FCT tax rates, etc.).
*   **Backend API Layer:**
    *   **Technology:** Python with FastAPI (as per `technology_stack_proposal.md`).
    *   **Function:** Handles all client requests from the frontend. Implements business logic, authentication, authorization (RBAC), data validation, and orchestration of services. Exposes RESTful APIs for the frontend.
*   **Data Ingestion Service/Layer:**
    *   **Technology:** Python (potentially using Celery/ARQ with FastAPI for scheduling and background tasks).
    *   **Function:** Responsible for fetching data from all external APIs (Gaming Companies, NLRC, FIRS/State IRS, Banks). Handles scheduling of data pulls, data transformation into canonical formats, initial validation, and error handling during ingestion.
*   **Operational Database:**
    *   **Technology:** PostgreSQL (as per `technology_stack_proposal.md`).
    *   **Function:** Stores core operational data: user accounts, roles, permissions, company information, state information, FCT configurations, license details (mirror from NLRC), issued invoices (mirror from FIRS/IRS), payment confirmations (mirror from Banks/FIRS/IRS), and potentially recent/hot transactional data for quick display. Also stores audit logs in a dedicated, secure schema.
*   **Data Warehouse (DWH):**
    *   **Technology:** Apache Druid / ClickHouse or Cloud-based solution (e.g., BigQuery, Redshift) – to be finalized based on infrastructure/policy (as per `technology_stack_proposal.md`). For MVP, could be an optimized schema within PostgreSQL.
    *   **Function:** Stores historical and aggregated data optimized for analytical queries, reporting, dashboard visualizations, and predictive analytics. Data is periodically loaded from the Operational DB and/or directly from the Data Ingestion Layer.
*   **Cache:**
    *   **Technology:** Redis (as per `technology_stack_proposal.md`).
    *   **Function:** Caches frequently accessed data (e.g., aggregated dashboard figures, user sessions, permissions) to improve frontend performance and reduce load on the Operational Database and DWH.
*   **External APIs:**
    *   Gaming Companies' APIs
    *   NLRC API
    *   FIRS / State IRS APIs
    *   Bank / Payment Gateway APIs
    *   **Function:** Provide the raw data that fuels the monitoring system. (Simulated initially).
*   **Alerting System:**
    *   **Technology:** Integrated within the Backend API Layer, potentially using a library or service for managing notifications.
    *   **Function:** Generates and dispatches alerts (in-app, email, SMS) based on predefined triggers (late payments, compliance changes, anomalies).
*   **Admin Console (Part of Frontend):**
    *   **Function:** Specific UI sections for Federal Super Admins to manage users, configure tax rates (State/FCT), set alert thresholds, and view system-wide audit logs.

**2. Data Flow**

1.  **Data Ingestion:**
    *   The **Data Ingestion Service** periodically polls (or receives data via webhooks, if supported by external APIs) the **External APIs**.
    *   Fetched raw data is transformed into a standardized internal format.
    *   Basic validation occurs (e.g., presence of key fields, data types). Errors are logged, and retry mechanisms are implemented.
    *   Cleaned, standardized data is then typically:
        *   Stored in the **Operational Database** if it's core entity data (like license status, latest invoice update) or needed for immediate operational logic.
        *   Sent directly to the **Data Warehouse** if it's voluminous transactional data (like individual sales records, if that granularity is pulled) or batched for ETL processing.

2.  **Data Processing & Storage:**
    *   The **Backend API Layer** processes data from the Operational DB to calculate derived metrics (e.g., Amount Taxable, Outstanding Payments) if not already done at ingestion.
    *   An ETL (Extract, Transform, Load) process (which can be managed by the Backend API Layer or a dedicated ETL tool/scripts) regularly moves data from the **Operational Database** to the **Data Warehouse**, structuring it for analytical querying (e.g., creating fact and dimension tables).

3.  **User Interaction & Data Presentation (Frontend):**
    *   User logs in via the **Frontend Application**.
    *   The Frontend sends requests to the **Backend API Layer**.
    *   The Backend API Layer handles authentication/authorization, then fetches data:
        *   For dashboards and reports requiring complex aggregations or historical data, queries are made to the **Data Warehouse**.
        *   For specific entity details, user information, or recent transactions, queries are made to the **Operational Database**.
        *   The **Cache (Redis)** is checked first for frequently accessed data to reduce direct database hits. If data is not in the cache, it's fetched from the DB/DWH and then cached.
    *   The Backend API Layer returns data to the Frontend for display.

4.  **Alerting:**
    *   The **Backend API Layer** (or a dedicated microservice) continuously evaluates conditions for alerts based on data in the Operational DB or DWH.
    *   When an alert condition is met, the **Alerting System** sends notifications through configured channels (in-app, email, SMS).

5.  **Administrative Actions:**
    *   Federal Super Admins use the **Admin Console** (Frontend) to manage users, roles, and system settings (e.g., tax rates).
    *   These actions are processed by the **Backend API Layer** and result in updates to the **Operational Database**. All such changes are logged in the audit trail.

**3. Data Ingestion Strategy (from External APIs)**

*   **Polling Frequency:**
    *   **Gaming Companies' API (Sales, Redemptions):** Near real-time is ideal, but depends on API capabilities and rate limits. Proposal: Batch pulls every **5-15 minutes**. If APIs support webhooks/push, that would be preferred.
    *   **NLRC API (Compliance Status):** Less frequent updates expected. Proposal: Batch pulls **once or twice daily**.
    *   **FIRS / State IRS API (Invoices, Payments):** Depends on how frequently invoices are issued and payments are updated. Proposal: Batch pulls **every 1-4 hours**.
    *   **Banks / Payment Gateways API (Payments):** Similar to FIRS/IRS, or potentially more frequent if reconciliation needs to be faster. Proposal: Batch pulls **every 1-4 hours**.
*   **Data Transformation:**
    *   Raw data from diverse external APIs will be transformed into a consistent internal JSON or object model before storage or further processing. This includes standardizing field names, data types, date formats, etc. Pydantic models in FastAPI will be heavily used for this.
*   **Error Handling:**
    *   Implement retry mechanisms with exponential backoff for transient API errors.
    *   Log all errors during ingestion (API unavailability, authentication failures, malformed data).
    *   For critical data sources, implement alerts if data fetching fails for an extended period.
    *   Define a strategy for handling malformed but partially usable data (e.g., quarantine, attempt repair, or reject with notification).

**4. Data Synchronization Strategy (Addressing User Query)**

*   **"Should data sync be real-time or batched every X minutes?"**
    *   **Answer:** A hybrid approach is best. True real-time for all data sources is often impractical due to external API limitations, rate limits, and the sheer volume of data.
    *   **Proposed Strategy:**
        *   **Near Real-Time (Batched - Short Intervals, e.g., 5-15 minutes):** Revenue data (Total Sales, Amount Redeemed) from Gaming Companies. This provides a frequently updated view of core financial metrics.
        *   **Batched - Medium Intervals (e.g., 1-4 hours):** Invoice and payment data from FIRS/State IRS and Banks. This allows for timely reconciliation of payments against dues.
        *   **Batched - Long Intervals (e.g., Daily):** Compliance data from NLRC, which typically changes less frequently.
        *   **On-Demand/Event-Driven (if possible):** If any APIs support webhooks, this would be used for instant updates for specific events.
    *   **Dashboard Labeling:** The dashboard will clearly indicate the last updated time for different data segments so users understand the data's freshness. For instance, "Gaming Revenue updated: 2 mins ago," "Compliance Status updated: Today 08:00 AM."
    *   **User Expectation Management:** It's crucial to communicate that "real-time" in this context means "as fast as technically feasible and sensible" given dependencies on external systems.

This architecture aims for a balance between providing timely data, system robustness, and efficient use of resources. The Data Ingestion Service is critical for decoupling the core system from the complexities of external APIs.
