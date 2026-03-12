# Content Plan Creation & Editing Form Specification

## Overview
This specification details the structure, fields, and behavior for the single page used to **create** and **edit** a Content Plan within the Workspace Admin Panel. The specification is aligned with `Docs/Database_schema.md` and the UI visual references provided.

## General Behaviors
- **Modes:** The form handles both "Create" (empty state, creates a new document) and "Edit" (pre-filled state, updates an existing document).
- **Save Action:** 
  - Submits the main payload to the `content_plans` collection.
  - Submits associated campaign changes to the `campaigns` subcollection of that plan.
- **Draggable Tag Lists:** All custom list "chips" (Statuses, Products, Audiences, Funnel steps, custom tags) must utilize a drag-and-drop library/behavior so users can manually reorder the presentation of the tags.
- **Workspace Context:** The document automatically associates with the current workspace via `workspace_ref`.

---

## 1. Core Information

### Name
- **Label:** Name
- **Type:** Text Input
- **Placeholder:** `Testplan` (or blank)
- **Database Mapping:** `name` (string)
- **Validation:** Required

### Plan Status
- **Label:** Status
- **Type:** Dropdown/Internal State
- **Default Value:** `Draft`
- **Database Mapping:** `status` (enum: `"Active" | "Archived" | "On Hold" | "Draft"`)
- **Validation:** Required

---

## 2. Filters Block
This section defines the metadata parameters that will be available for tagging individual ads inside the Content Plan. 

*Note: UI shows a "Default" label in the corners of these groups, implying they can be reset or inherit workspace-level defaults.*

### Statuses
- **Description:** Custom status lifecycle steps for ads.
- **UI Controls:** 
  - Text Input ("Status name...") + `[+]` button.
  - Rendered as a list of draggable chips with `X` to remove.
- **Database Mapping:** `enabled_statuses` (array of strings)
- **Example Output Data:** `["In progress", "Approved", "Live", "Paused"]`

### Platforms
- **Description:** Target ad platforms.
- **UI Controls:**
  - Predefined multi-select toggle buttons (pill shape). 
  - Active state shown with a solid color (e.g., brand blue).
- **Database Mapping:** `enabled_platforms` (array of strings)
- **Predefined Options:** `Tiktok`, `Meta`, `Google Display (responsive)`, `Google Display (only image/html5)`, `Pinterest`, `Snapchat`, `Linkedin`, `Youtube`.

### Products (Customizable Alias)
- **Description:** Products featured in the plan's ads. *(Note: Technically, an alias field will be added to the database so this could be renamed to something like "Services" or "Offers" per workspace, but conventionally designed as "Products".)*
- **UI Controls:** 
  - Text Input ("Product name...") + `[+]` button.
  - Rendered as a draggable chip list.
- **Database Mapping:** `enabled_products` (array of strings)
- **Example Output Data:** `["Car", "Home", "Bank"]`

### Audiences
- **Description:** Target audiences for the ads.
- **UI Controls:**
  - Text Input ("Audience name...") + `[+]` button.
  - Rendered as a draggable chip list.
- **Database Mapping:** `enabled_audiences` (array of strings)
- **Example Output Data:** `["Young", "Family", "Senior", "18+"]`

### Funnel Steps
- **Description:** Marketing funnel stages.
- **UI Controls:**
  - Text Input ("Step name...") + `[+]` button.
  - Rendered as a draggable chip list.
- **Database Mapping:** `enabled_funnel_steps` (array of strings)
- **Example Output Data:** `["Conversion", "Consideration", "Awareness"]`

## 2.5 Custom Categories Block
Allows administrators to register entirely new tagging dimensions specific to this plan, beyond the built-in ones.

- **Description:** Create custom tags and define how they behave when assigned to an ad.
- **Selection Types:**
  - **Button (single select):** Enables choosing only 1 value per ad (e.g., Objective).
  - **Dropdown (multi select):** Enables assigning multiple values per ad (e.g., Regions).
- **UI Controls:**
  1. Text Input ("Create new category...")
  2. Dropdown / Select ("Button (Single Select)", "Dropdown (Multi Select)")
  3. `[+]` Add button.
  *(Adding this creates a new custom block where the admin can add values as draggable chips, similar to "Audiences" or "Products" above)*
- **Database Mapping:** Pushes to the `enabled_tags` array.
- **Data Structure Example:**
  ```json
  // TagStruct
  [
    {
      "category": "Objectives",
      "type": "single",
      "options": ["Form Fills", "Traffic"]
    },
    {
      "category": "Regions",
      "type": "multi",
      "options": ["North America", "EMEA"]
    }
  ]
  ```

---

## 3. Campaigns Block
Stores high-level campaigns under this plan. 

- **UI Controls:**
  - Text Input ("New Campaign name...") + `[+]` button.
  - List of active campaigns displayed directly below (e.g., as pills or cards).
- **Default Entry:** "Always On" is typically present as a default bucket.
- **Database Mapping:** 
  - Saves to the Subcollection: `content_plans/{planId}/campaigns/{campaignId}`
  - Example document payload per campaign added:
    ```json
    {
      "name": "Campaign Name",
      "type": "campaign" // or "always_on"
    }
    ```

---

## 4. External Resources Block
External links used for quick access buttons on the plan's main page.

- **UI Controls:**
  - Two adjacent inputs per row attempt:
    - Text Input 1 ("New button lable...")
    - Text Input 2 ("New Url...")
  - Add `[+]` button.
  - Renders a list below with options to remove `X` or edit existing pairs.
- **Database Mapping:** `external_resources` (array of `ExternalResourceStruct` objects)
- **Data Structure:**
  ```json
  [
    {
      "label": "String",
      "url": "String (URL)"
    }
  ]
  ```

---

## Technical/FlutterFlow Considerations
1. **Local State for Forms:** Since the payload includes multiple arrays (Chips) and subcollection items (Campaigns), data should be stored in the page/component Page State (`List<String>`, `List<DataType>`) as the user edits. Database writes should ONLY occur when the user clicks **"Save Content Plan"**.
2. **ReorderableListView:** For the drag-and-drop lists, use FlutterFlow's `ReorderableListView` widget mapped to the specific Page State lists so user sorting updates the local array order automatically.
3. **Draft Status:** While editing/creating, ensure the system can distinguish logic rules if creating a completely back-end `Draft` status vs simply modifying Page State.
