# Implementation Plan - Dynamic Tag Filtering & Data Types

## Goal Description
Implement a flexible filtering system for Ad Content Plans using client-side logic in FlutterFlow. This approach handles dynamic tag categories (e.g., "Audience", "Product") defined by the user. Additionally, define the necessary Data Types (Structs) for FlutterFlow to ensure type safety.

## Proposed Changes

### 1. Data Types (FlutterFlow Custom Data Types)
We need to define these structures in FlutterFlow to parse the Maps from Firestore correctly.

#### `TagConfiguration` (For `content_plans.enabled_tags`)
Used to store the available options for dropdowns.
*   **Structure**: List<Struct> (Array of Objects)
*   **Fields**:
    *   `category` (String)
    *   `options` (List<String>)
*   **Why**: Lists of objects are easier to iterate through in FlutterFlow UI (e.g., generating a ListView of Dropdowns) compared to Maps.

#### `AdTags` (For `ads.tags`)
Used to store the selected tags for an ad.
*   **Structure**: Map<String, List<String>>
*   **Example**: `{"Audience": ["B2B"], "Product": ["Shoes"]}`

#### `PlatformConfig` (For `platforms.field_config`)
*   `label` (String)
*   `max_chars` (Integer)
*   `max_items` (Integer)
*   `is_active` (Boolean)

### 2. Client-Side Filtering Logic (Custom Function)
Since tag categories are dynamic, we cannot use standard Firestore "Where" clauses easily for all combinations.

**Function Name:** `filterAdsList`
**Inputs:**
*   `adsList`: List of Ad Documents
*   `selectedFilters`: Map<String, String> (Key: Category, Value: Selected Option)

**Logic:**
```dart
List<AdRecord> filterAdsList(List<AdRecord> adsList, Map<String, String>? selectedFilters) {
  if (selectedFilters == null || selectedFilters.isEmpty) {
    return adsList;
  }

  return adsList.where((ad) {
    // Check if Ad matches ALL selected filters
    for (var entry in selectedFilters.entries) {
      String category = entry.key;
      String selectedOption = entry.value;

      // Get tags for this ad (assuming ad.tags is a Map or JSON)
      // Note: Adjust based on actual Data Type implementation
      var adTags = ad.tags; 
      
      if (adTags == null || !adTags.containsKey(category)) {
        return false; // Ad doesn't have this category tag
      }
      
      // Check if the list of tags for this category contains the selected option
      List<dynamic> tagsForCategory = adTags[category];
      if (!tagsForCategory.contains(selectedOption)) {
        return false;
      }
    }
    return true;
  }).toList();
}
```

### 3. UI Implementation Steps
1.  **Fetch Data**: Query `ads` collection at the Page level (ContentPlanDetails).
2.  **State Variable**: Create a Page State variable `selectedFilters` (DataType: Map<String, String> or JSON).
3.  **Filter UI**:
    *   Use a `ListView` to generate Dropdowns based on `content_plan.enabled_tags`.
    *   On Dropdown change -> Update `selectedFilters`.
4.  **Ads List**:
    *   Use the `filterAdsList` custom function as the Source for the Ads ListView.
    *   Pass the raw Firestore list and the `selectedFilters` state.

## Verification Plan
### Manual Verification
- Create a Content Plan with tags: `{"Audience": ["B2B", "B2C"]}`.
- Create Ad 1 with `tags: {"Audience": ["B2B"]}`.
- Create Ad 2 with `tags: {"Audience": ["B2C"]}`.
- In the App, select "B2B" in the filter.
- Verify only Ad 1 is shown.
