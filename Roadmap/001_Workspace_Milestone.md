# Milestone: Implementing a Workspace Level for ellaella.io

## Overview

This document outlines the concrete steps to implement the Workspace level hierarchy for our clients (Agencies). It enables them to manage their own users and content plans within an isolated space.  

## 1. Database & Security Implementation (Firestore)

### 1.1 Collections Structure

* **[NEW] `workspaces` Collection**:
  * `name` (string)
  * `owner_id` (reference): Reference to the original client User Document.
  * `created_at`, `updated_at` (timestamps)

* **[MODIFY] `users` Collection**:
  * Add `workspace_id` (reference): Link a user to a workspace.
  * Add `workspace_role` (enum string): `"owner"`, `"admin"`, or `"user"`.
  * Update Global Admin logic: Add `is_app_admin` (boolean). Set to `true` for Super Admin.
  * *(For Users)* Add `assigned_plans` (array of references): Specifies which Content Plans a `"user"` can access.

* **[MODIFY] `content_plans` Collection**:
  * Add `workspace_ref` (reference).
  * *Deprecation Goal*: Over time, remove the `client_ref` field as everything will hang off `workspace_ref`.

### 1.2 Security Rules (firestore.rules)

* **Super Admin:** If `request.auth` user document has `is_app_admin == true`, allow all read/writes.
* **Workspaces:**  
  * Read: User's `workspace_id` == `resource.id`.
  * Write: User's `workspace_id` == `resource.id` AND `workspace_role == "owner"`.
* **Content Plans**:  
  * Read/Write: `resource.data.workspace_ref` == user's `workspace_id`. If `workspace_role == "user"`, the `resource.id` must also exist in the user's `assigned_plans` array.
* **Ads/Campaigns**:
  * Currently, they sit via path (`content_plans/{planId}/ads/{adId}`). Inherit the Content Plan read/write rules.

---

## 2. API & Backend (Cloud Functions)

### User Management Functions

We will modify an existing Cloud Function or Backend action to handle user invitations for Workspaces.

1. **Modify `inviteWorkspaceUser` Function**:
    * *Input*: `email`, `workspace_role` (Admin/User), optional `assigned_plans`.
    * *Action*: Reuses the existing logic to create a Firebase Auth user, then creates the `users` document in Firestore assigned to the current Workspace's `workspace_id` and the selected role. Since a user can only belong to one workspace, `workspace_id` is a direct reference.

## 3. Global Admin Dashboard (App Admin)

1. **Workspaces Listing**: A view for Super Admins querying the `workspaces` collection.
2. **Navigation (Impersonation)**:
    * Clicking a workspace sets an App State variable (e.g., `active_workspace_id`).
    * The Admin Panel then dynamically filters `content_plans` where `workspace_ref == active_workspace_id`.
    * Provides full CRUD rights over roles and plans.

## 4. Workspace Panel (Owner / Admin)

1. **Dashboard Refactoring**:
    * Update queries: Instead of fetching `content_plans` where `client_ref == current_user`, fetch where `workspace_ref == current_user.workspace_id`.
2. **Team Management Tab**:
    * List view of `users` belonging to the current `workspace_id`.
    * Owner/Admin can trigger the modified invitation function.
    * Owner/Admin can edit a team member (change role, revoke access, edit `assigned_plans`).

## 5. Content Plan Refactoring (Full-Screen Form)

### Dynamic Tag Editing

1. **Local State Component**: Migrate from narrow modals to a full-screen or expanded form. Store the `enabled_tags` configuration in a Local State Variable while editing.
2. **Drag & Drop Ordering**: Use the built-in `ReorderableListView` in FlutterFlow, mapped to the options list of `TagStruct`, to allow users to correctly and intuitively rearrange tags.  

### Extended Explanations (Tooltips)

* Add UX hints using FlutterFlow Tooltips to explain "Always On" vs Campaigns, Tag structures, and single/multi-selection modes, catering to Agency clients who are less familiar with the system backend.

## 6. Migration Script (Python)

Before deploying, we will run a Python migration script to convert existing users to the workspace model:

1. Iterate over all existing `users` (clients).
2. Create a `Workspaces` document for each.
3. Set the client's `workspace_id` to that new document + `workspace_role = "owner"`.
4. Update their `content_plans` by populating the new `workspace_ref` field.
