**Security Architecture**

This document outlines the security architecture for the National Gaming & Lottery Revenue Monitoring Dashboard, covering Role-Based Access Control (RBAC), data encryption, API key management, regulatory compliance, and secure audit log storage.

**1. Role-Based Access Control (RBAC)**

*   **Framework Integration:**
    *   RBAC will be implemented within the chosen backend framework (Python/FastAPI).
    *   FastAPI's dependency injection system will be used to create middleware or route dependencies that verify user roles and permissions for each API endpoint.
*   **User Roles & Permissions Storage:**
    *   User roles (`Federal Super Admin`, `State Admin`, `Auditor/Analyst`) are defined in the `roles` table (as per `database_schemas.md`).
    *   Permissions associated with each role will be a combination of:
        *   Implicit permissions derived from the role name (e.g., Federal Super Admin has access to all states).
        *   Explicit permissions potentially stored in the `roles.permissions` JSONB field if finer-grained control is needed beyond the role's general scope (e.g., permission to configure specific alert types).
*   **Authentication:**
    *   Users will authenticate using username and password. OAuth2 Password Grant flow will be used to issue JWTs.
    *   Passwords will be stored securely using a strong hashing algorithm (e.g., bcrypt or Argon2) with per-user salts in the `users.password_hash` field.
*   **Authorization (JWT & Middleware):**
    *   Upon successful login, a JSON Web Token (JWT) is issued to the client. This token will contain `user_id`, `role`, and `state_id` (if applicable) and an expiry time.
    *   The JWT must be included in the `Authorization` header (Bearer token) for all subsequent API requests.
    *   A FastAPI middleware will intercept every request to:
        *   Validate the JWT signature and expiry.
        *   Extract user information from the token.
        *   Verify that the user's role has the necessary permissions to access the requested endpoint and resource. For example:
            *   A State Admin attempting to access data for a state other than their assigned `state_id` will be denied.
            *   An Auditor/Analyst attempting a POST/PUT/DELETE request will be denied.
*   **State-Based Scoping:**
    *   For State Admins and Auditors/Analysts, data access will be strictly scoped to their assigned `state_id` (stored in the `users` table). Database queries will automatically include `WHERE state_id = :user_state_id` clauses based on the authenticated user's context.
*   **Federal Admin Access (FCT vs. Other States):**
    *   Federal Super Admins will have a special condition:
        *   Full management capabilities (CRUD) for FCT data.
        *   Read-only access to data from all other states. This distinction will be enforced in the API logic.

**2. Data Encryption**

*   **Data in Transit:**
    *   All communication between the client (browser), the backend API, and any external API (where supported by the external API) will be encrypted using **TLS 1.2 or higher (preferably TLS 1.3)**.
    *   Strong cipher suites will be configured on the web server and API gateways.
    *   HTTPS will be enforced sitewide.
*   **Data at Rest:**
    *   **Operational Database (PostgreSQL):**
        *   Utilize Transparent Data Encryption (TDE) features if provided by the PostgreSQL hosting environment (e.g., cloud provider managed PostgreSQL often includes this).
        *   Alternatively, encrypt sensitive columns (e.g., PII in `users` table, financial figures if deemed necessary beyond database-level access controls) using PostgreSQL's `pgcrypto` extension or application-level encryption before storing. However, full database or filesystem-level encryption is generally preferred for operational simplicity if available. **AES-256** is the target algorithm.
    *   **Data Warehouse:** Similar to the operational database, leverage TDE if available, or encrypt sensitive data at the application level before loading into the DWH. **AES-256** is the target.
    *   **Backups:** All database and file storage backups will be encrypted using AES-256.
    *   **Cache (Redis):** If Redis stores sensitive data, secure its communication (TLS) and consider encryption at rest if the Redis version and hosting environment support it.
    *   **File Storage (Exports, Logs if stored as files):** Any sensitive files (e.g., exported reports, temporarily stored log files) will be encrypted using AES-256.

**3. Secure API Key Management (for accessing External APIs)**

*   **Storage:**
    *   API keys and secrets for accessing external services (Gaming Companies, NLRC, FIRS, Banks) will **NOT** be stored in code repositories.
    *   They will be stored in a secure secret management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or environment variables in a secure hosting environment).
    *   The application will retrieve these secrets at runtime.
*   **Access Control:**
    *   Access to the secret management system will be tightly controlled.
    *   The application's runtime environment/service account will have the minimum necessary permissions to read these secrets.
*   **Rotation:**
    *   Establish a policy and procedure for regular rotation of these external API keys, where supported by the providers.
*   **Backend Only:** External API keys will only be used by the backend Data Ingestion Service. They will never be exposed to the frontend application.

**4. Regulatory Compliance (e.g., NDPR)**

*   **Data Minimization:** Collect and store only the data essential for the system's defined functionality.
*   **Purpose Limitation:** Data collected will be used only for the revenue monitoring and regulatory purposes outlined.
*   **User Consent:** While this is a government system, ensure clarity on data handling if any PII is collected beyond official user accounts.
*   **Data Subject Rights:** If NDPR applies to any personal data processed (e.g., user admin accounts), ensure mechanisms for access, rectification, and erasure (where legally applicable) are considered.
*   **Data Residency:**
    *   Clarify with the Nigerian government if there are strict data residency requirements (i.e., data must be stored within Nigeria).
    *   If so, the choice of hosting (cloud region or on-premise) must comply. This will heavily influence DWH and other managed service selections.
*   **Data Protection Impact Assessment (DPIA):** Recommend conducting a DPIA to systematically identify and mitigate data protection risks.
*   **Breach Notification:** Establish a procedure for responding to and reporting data breaches as per NDPR requirements.

**5. Secure Audit Log Storage**

*   **Database Storage:**
    *   Audit logs will be stored in the `audit_logs` table within the PostgreSQL operational database, as defined in `database_schemas.md`.
*   **Append-Only (Conceptual):**
    *   While true append-only is hard to enforce at the application level in a standard SQL database, implement strict access controls:
        *   The application user/role connecting to the database for logging purposes should only have `INSERT` permissions on the `audit_logs` table.
        *   `UPDATE` and `DELETE` permissions on this table should be denied to the application's general operational roles.
        *   Only highly privileged database administrator roles (separate from application roles) should have modify/delete rights on this table, for archival or emergency maintenance, with such actions themselves being heavily audited.
*   **Integrity:**
    *   Consider techniques like hashing log entries or chains of log entries if a higher degree of tamper evidence is required, though this adds complexity.
*   **Access Control & Monitoring:**
    *   Access to audit logs will be restricted via RBAC (primarily Federal Super Admins).
    *   Monitor access to the audit logs themselves.
*   **Retention:**
    *   Define and implement a log retention policy based on legal and regulatory requirements (e.g., 7 years). Old logs may be archived to a separate, cheaper storage tier and eventually purged.
*   **Regular Review:** Implement procedures for regular review of audit logs to detect suspicious activities.

This security architecture provides a comprehensive approach to protecting the system and its data. It will be continuously reviewed and updated as the system evolves and new threats emerge.
