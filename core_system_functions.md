**Core System Functions**

This document outlines key system-level functions required for the National Gaming & Lottery Revenue Monitoring Dashboard.

**1. Predictive Analytics & Anomaly Detection**
    *   **Scope:** To identify unusual patterns or deviations from expected revenue figures, transaction volumes, or payment behaviors that might indicate errors, fraud, or emerging trends.
    *   **Functionality:**
        *   **Trend Analysis:** Basic forecasting of revenue streams (e.g., based on historical data using time series models like moving averages, ARIMA - though initial implementation might be simpler). Display expected vs. actual revenue.
        *   **Anomaly Detection Rules:**
            *   Significant deviation from average revenue for a specific company or state (e.g., +/- X% from 30-day moving average). Thresholds (X%) should be configurable by Federal Super Admins.
            *   Sudden drop in reported sales volume for a typically consistent company.
            *   Unusually high redemption rates for a company compared to its historical baseline or peers.
            *   Payments significantly deviating from invoiced amounts (beyond a tolerance).
            *   Absence of data reporting from a company for X consecutive periods.
        *   **Visualization:** Dashboards to highlight detected anomalies and trends.
        *   **Machine Learning (Future Scope):** While initial implementation will be rule-based, the architecture should allow for future integration of more advanced ML models for anomaly detection as more data is gathered.
    *   **Required Data Sources/System Capabilities:**
        *   Historical revenue data (Sales, Redeemed, Taxable, Paid) stored in the Data Warehouse.
        *   Configurable thresholds for anomaly rules.
        *   Data processing engine capable of performing calculations and comparisons.
        *   Integration with the alerting system.

**2. Real-time Alerts**
    *   **Scope:** To notify relevant government officials immediately about critical events or detected anomalies requiring attention.
    *   **Functionality:**
        *   **Alert Triggers (Initial Set):**
            *   **Late Payments:** When `Outstanding Payments` remain for a company past a configurable due date from `Amount Invoiced`.
            *   **Compliance Status Change:** When a company's `Compliance Status` (from NLRC feed) changes to "Unlicensed," "Suspended," or "Expired."
            *   **Data Reporting Failure:** If a company fails to submit required data for a configurable period.
            *   **Critical Anomalies Detected:** Triggered by the Anomaly Detection system based on severity (e.g., revenue drop > Y%).
            *   **Large Outstanding Balances:** When `Outstanding Payments` for a company exceed a configurable threshold.
            *   **Security Events (Optional but Recommended):** e.g., multiple failed login attempts for an admin account.
        *   **Notification Channels:**
            *   In-app notifications on the dashboard.
            *   Email notifications.
            *   SMS notifications (for high-priority alerts, if required and budgeted).
        *   **Alert Management:**
            *   Federal Super Admins and State Admins (for their respective areas) can view, acknowledge, and potentially escalate alerts.
            *   Configurable alert severities (e.g., Low, Medium, High, Critical).
            *   Configurable recipients for different alert types (e.g., payment alerts to finance teams, compliance alerts to regulatory teams).
    *   **Required Data Sources/System Capabilities:**
        *   Real-time data feeds for payments, compliance status, and revenue.
        *   Integration with Anomaly Detection module.
        *   User database with contact information (email, phone for SMS).
        *   Notification service integration (email gateway, SMS gateway).
        *   Configurable business rules for alert conditions.

**3. Audit Logs & Access Tracking**
    *   **Scope:** To maintain a comprehensive, immutable record of all significant actions performed within the system for security, accountability, and troubleshooting.
    *   **Functionality:**
        *   **Logged Actions (Examples):**
            *   User login attempts (success/failure), logouts.
            *   Data viewing/access by any user (what data was seen, e.g., "State Admin X viewed Company Y's revenue for June 2024").
            *   All CRUD operations (Create, Read, Update, Delete) on data (e.g., "Federal Admin Z updated Tax Rate for State A").
            *   Report generation and data exports (who exported what, when).
            *   User management actions (creation, role changes, deactivation).
            *   System configuration changes (e.g., alert threshold modifications).
            *   Alert generation, acknowledgement, and resolution.
        *   **Log Details:** Each log entry must include:
            *   Timestamp (accurate to the second).
            *   User ID and role performing the action.
            *   IP address of the user.
            *   Action performed (e.g., "LOGIN_SUCCESS", "UPDATE_COMPANY_DATA").
            *   Details of the entity affected (e.g., Company ID, Report ID, User ID managed).
            *   Outcome of the action (success/failure).
        *   **Log Storage & Retention:**
            *   Stored in a secure, tamper-evident manner (e.g., dedicated append-only log database or specialized logging service).
            *   Configurable retention policy (e.g., retain logs for 7 years, as per potential legal requirements – this needs clarification).
        *   **Access & Review:**
            *   Federal Super Admins have full access to review all audit logs.
            *   State Admins may have access to logs pertaining to their state's data and users.
            *   Dedicated audit console/interface for searching and filtering logs.
    *   **Required Data Sources/System Capabilities:**
        *   Integration points within all system modules to trigger log events.
        *   Secure log storage solution.
        *   Clock synchronization across all system components.

**4. Export (CSV, PDF, Excel)**
    *   **Scope:** To allow users to extract data from the system for offline analysis, reporting, or archival.
    *   **Functionality:**
        *   **Exportable Data:**
            *   Tabular data from reports (e.g., revenue summaries, company lists, payment histories).
            *   Details from drill-down views.
            *   Potentially, filtered views of dashboards (e.g., a PDF snapshot of a specific state's performance).
        *   **Formats:**
            *   CSV: For raw data, easily importable into spreadsheets or other analysis tools.
            *   Excel (XLSX): For formatted reports, potentially with multiple sheets.
            *   PDF: For printable, paginated reports and dashboard snapshots.
        *   **Role-Based Access to Export:**
            *   **Federal Super Admin:** Can export any data from any part of the system.
            *   **State Admin:** Can export data pertaining only to their assigned state.
            *   **Auditors & Analysts:** Can export data they have read-only access to (i.e., within their assigned state).
        *   **Export Controls:**
            *   Logging of all export actions (who, what, when) in the Audit Log.
            *   Potential limits on export size or frequency if system performance is a concern (configurable).
    *   **Required Data Sources/System Capabilities:**
        *   Access to the Data Warehouse and operational database.
        *   Libraries/tools for generating CSV, XLSX, and PDF files.
        *   Integration with the RBAC system to enforce export permissions.

This document will inform the selection of specific tools and technologies, as well as the detailed design of these system functionalities.
