# Super Admin Dashboard & Workspace Config

## Overview
The Super Admin Dashboard is the central control hub solely accessible by the Global App Administrator (e.g., you). Its primary purpose is to oversee, manage, and configure all Workspaces (Agencies/Clients) operating on the `ellaella.io` platform.

This dashboard provides a high-level view of system usage and allows the Super Admin to step into any workspace to provide support or manage configurations.

---

## Key Views & Components

### 1. Workspaces Overview (Main Screen)
This is the primary listing view.
*   **Metrics & Stats:**
    *   Total Active Workspaces
    *   Total Global Users
    *   Total Active Content Plans
*   **Workspace List/Grid:**
    *   Displays Cards/Rows for each Workspace.
    *   *Visible Info:* Workspace Name, Owner Email, Number of Team Members, Number of Active Content Plans, Last Updated Date, Status (Active/On Hold).
*   **Global Actions:**
    *   `+ Create Workspace`: Opens a modal/page to initialize a new Workspace (Name, assign Owner email).
    *   `Global Search`: Quickly find a workspace or a specific user email across the entire database.

### 2. Workspace Detail / Impersonation Mode
When you click on a specific Workspace card, you "enter" that workspace as a Super Admin.
*   **Action:** The app sets the `active_workspace_id` to this chosen workspace.
*   **View:** You see the exact same Workspace Admin Panel that the Owner/Admin sees (Users list, Content Plans list), but with full read/write privileges override due to your `is_app_admin` flag.
*   **Support Capability:** You can create/edit content plans, rename tags, or debug user access issues directly within their environment.

---

## 3. Workspace Settings (Basic Configuration)

As a Super Admin (and eventually exposed to Workspace Owners), you need the ability to configure the basic properties of a Workspace.

These settings are managed in a dedicated **Settings Tab / Modal** within the Workspace Detail view.

### Base Configuration (Milestone 1)
*   **Workspace Profile:**
    *   **Name:** Rename the Workspace (e.g., updating "Agency X" to "Agency X Global").
    *   **Logo / Avatar:** Upload a custom logo (Stored in Firebase Storage). This logo can replace default icons in their specific dashboard or on exported documents.
*   **Status & Lifecycle (Super Admin Only):**
    *   **Status Toggle:** Mark a workspace as `Active`, `On Hold` (read-only mode), or `Archived`.
    *   **Delete Workspace:** Irreversible action. Requires confirmation typing the workspace name. *Must handle cascaded deletion of subcollections (users, content_plans, ads).*

### Ownership Transfer
*   **Transfer Owner Role:** Ability to reassign the `"Owner"` role to another Admin user within the same workspace. Useful if the primary point of contact at the agency changes.

---

## Future Expandability (Post-Milestone 1)
*This structure is designed to easily accommodate future settings without breaking the UI:*
*   **Billing & Subscriptions:** Connect Stripe Customer IDs to the Workspace document.
*   **Global Tag Presets:** Define default Tags (e.g., standard funnel steps) that auto-populate when the agency creates a *new* Content Plan.
*   **Platform Restrictions:** Toggles to globally disable specific platforms (e.g., Snapchat) for the entire agency, hiding them from UI dropdowns.
*   **White-labeling:** Setting custom primary colors for the client portal.
