**User Roles and Permissions Document**

**1. Federal Super Admin**
    *   **Data Access:**
        *   Full read-only access to all data from all gaming and lottery companies across all states (non-FCT).
        *   Full CRUD access to all data for gaming and lottery companies based in the Federal Capital Territory (FCT).
        *   Access to system-wide configurations and settings.
    *   **Core Data Operations (CRUD):**
        *   Create, Read, Update, Delete (CRUD) operations on company records (full CRUD for FCT, Read-only for other states).
        *   CRUD operations on state records (e.g., adding a new state if necessary, configuring state-specific parameters if any).
        *   CRUD operations on user accounts (Federal Admins, State Admins, Auditors/Analysts).
        *   Ability to correct or annotate revenue data if discrepancies are found (full rights for FCT, potential for read/suggest for other states, with strict audit trails).
    *   **Financial Management:**
        *   **FCT Specific:**
            *   Directly manage and configure FCT tax percentages (e.g., `FCT_Tax_Percentage`).
            *   Oversee and manage invoicing and payment reconciliation processes for companies based in the FCT.
            *   View and manage FCT-specific revenue summaries (Total Sales, Redeemed, Taxable, Due to FCT Admin, Invoiced, Paid, Outstanding).
        *   **National Oversight (Non-FCT States - Read-Only):**
            *   View national-level revenue summaries and state-specific summaries for all states.
            *   Oversee (read-only) invoicing and payment reconciliation processes across all non-FCT states.
        *   **General:**
            *   Configure or update state-level tax percentages (`State_Tax_Percentage`) for all states (including FCT as a "state-level" entity in this context).
            *   Set system-wide financial reporting standards or parameters if applicable.
    *   **User Management:**
        *   Create, activate, deactivate, and assign roles to State Admins and Auditors/Analysts.
        *   Manage user profiles and permissions.
    *   **System Configuration & Monitoring:**
        *   Configure system-wide alert parameters (e.g., thresholds for anomaly detection, payment delays).
        *   Manage and view system-wide audit logs and access tracking.
        *   Monitor system health and performance.
        *   Oversee compliance status of all companies nationally.
    *   **Reporting & Analytics:**
        *   Generate and export comprehensive national-level reports (CSV, PDF, Excel) covering all aspects of revenue, tax, payments, and compliance.
        *   Access predictive analytics and anomaly detection dashboards for all states.
    *   **Alert Management:**
        *   View and manage all system-generated alerts (e.g., late payments, compliance issues, anomalies).
        *   Configure alert notification channels.

**2. State Admin**
    *   **Data Access:**
        *   Access to all data from all gaming and lottery companies *only within their assigned state*.
        *   Access to state-specific configurations and settings.
    *   **Core Data Operations (CRUD within their State):**
        *   Create, Read, Update, Delete (CRUD) operations on company records *within their state*. This includes:
            *   Adding new companies operating in their state.
            *   Updating company details (e.g., contact information, license status if manually managed and not solely from NLRC feed).
            *   Marking companies as active/inactive within their state.
        *   Read operations on their own state's records.
        *   Ability to correct or annotate revenue data for companies *within their state* if discrepancies are found (with strict audit trails, possibly requiring Federal Admin approval for certain changes).
    *   **Financial Management (within their State):**
        *   View and manage state-level revenue summaries (Total Sales, Redeemed, Taxable, Due to State Gov., Invoiced, Paid, Outstanding) for companies in their state.
        *   Configure or update state-specific tax percentages/rules if the system allows such granularity (otherwise, view national settings).
        *   Oversee and verify invoicing and payment reconciliation processes for companies in their state.
    *   **User Management (Limited):**
        *   View Auditors/Analysts assigned to their state (creation/assignment likely by Federal Super Admin).
        *   Potentially manage specific access nuances for Auditors/Analysts *within their state's dataset* if the system allows.
    *   **System Configuration & Monitoring (within their State):**
        *   Configure state-specific alert parameters (e.g., thresholds for anomaly detection, payment delays) if system allows, otherwise use/view federal defaults.
        *   Manage and view audit logs and access tracking related to their state's data and users.
        *   Monitor compliance status of companies within their state.
    *   **Reporting & Analytics (within their State):**
        *   Generate and export comprehensive state-level reports (CSV, PDF, Excel) covering revenue, tax, payments, and compliance for their state.
        *   Access predictive analytics and anomaly detection dashboards for their state.
    *   **Alert Management (within their State):**
        *   View and manage system-generated alerts pertaining to their state.
        *   Configure alert notification channels for state-level alerts.

**3. Auditors & Analysts**
    *   **Data Access:**
        *   Read-only access to designated datasets *within their assigned state(s)*. (Initial feedback: "limited to work within their state data". This implies assignment to one or more specific states by a Federal Super Admin).
        *   The "designated datasets" will include all core revenue data points: Total Sales Volume, Amount Redeemed, Amount Taxable, Amount Due to State Gov., Amount Due to FCT Admin (if applicable to the assigned "state"), Amount Invoiced, Amount Paid, Outstanding Payments, and Compliance Status for companies in their assigned state(s).
    *   **Core Data Operations:**
        *   Strictly Read-only. No Create, Update, or Delete capabilities.
    *   **Financial Management (Read-only):**
        *   View state-level revenue summaries for their assigned state(s).
    *   **Reporting & Analytics (within their assigned State(s)):**
        *   Generate and export reports (CSV, PDF, Excel) based on the data they have access to within their assigned state(s). Specific report templates might be predefined.
        *   View predictive analytics and anomaly detection dashboards relevant to their assigned state(s).
    *   **Alert Management (View only):**
        *   View alerts relevant to their assigned state(s) as configured by Admins. Cannot manage or configure alerts.
    *   **Audit Trail:**
        *   All their access and report generation activities will be logged.

**General Permissions Considerations for All Roles:**
*   **Authentication:** Secure login mechanisms (e.g., multi-factor authentication options).
*   **Password Management:** Policies for password complexity, expiry, and recovery.
*   **Session Management:** Secure handling of user sessions, including timeouts.
*   **Data Export Controls:** While export is a feature, logs must track what data was exported, by whom, and when. Large data exports might require additional approval or trigger alerts.

This document will serve as a foundational reference for building the authentication, authorization, and UI components of the system.
