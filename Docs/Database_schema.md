# Database Schema Design

## Overview
This schema is designed for **Firebase Firestore**. It prioritizes **low read costs** and **flexible filtering** for the Ad Campaign Directory.

### Core Architecture: Subcollections
We use a hierarchical structure where `ads` and `campaigns` are subcollections of `content_plans`. This ensures data isolation between clients and simplifies security rules.

## Collections Structure

### 1. `users` (Root Collection)
Stores user profile information.
*   **Document ID**: `auth_user_id` (from Firebase Auth)
*   **Fields**:
    *   `email` (string): User's email.
    *   `display_name` (string): User's full name.
    *   `role` (string): `"admin"` | `"client"`.
    *   `created_at` (timestamp).
    *   `last_login` (timestamp).

### 2. `content_plans` (Root Collection)
Represents a workspace for a specific client.
*   **Document ID**: Auto-generated (e.g., `plan_123`)
*   **Fields**:
    *   `name` (string): Name of the content plan (e.g., "Client X Master Plan").
    *   `status` (enum): `"Active"` | `"Archived"` | `"On Hold"`.
    *   `client_ref` (reference): Reference to `users/{client_user_id}`.
    *   `created_at` (timestamp).
    *   `updated_at` (timestamp).
    *   `enabled_statuses` (array of strings): List of available statuses for ads in this plan (e.g., `["Draft", "In Review", "Approved", "Live"]`).
    *   `enabled_platforms` (array of strings): List of platform IDs enabled for this plan (e.g., `["meta", "tiktok"]`). If empty, all platforms are available.
    *   `enabled_tags` (array of objects): Configuration for dropdowns unique to this plan.
        ```json
        [
          {
            "category": "Funnel step",
            "options": ["Awareness", "Conversion"]
          },
          {
            "category": "Audience",
            "options": ["B2B", "B2C"]
          }
        ]
        ```

### 3. `campaigns` (Subcollection of `content_plans`)
Stores metadata for campaigns. "Always On" is treated as a special campaign or just a specific document here.
*   **Path**: `content_plans/{planId}/campaigns/{campaignId}`
*   **Fields**:
    *   `name` (string): Campaign name (e.g., "Black Friday 2024", "Always On").
    *   `type` (enum): `"always_on"` | `"campaign"`.
    *   `start_date` (timestamp, optional).
    *   `end_date` (timestamp, optional).
    *   `budget` (number, optional).
    *   `status` (enum): `"active"` | `"completed"` | `"planned"`.

### 4. `ads` (Subcollection of `content_plans`)
Stores the actual ad content.
*   **Path**: `content_plans/{planId}/ads/{adId}`
*   **Note**: Ads are placed directly under the Content Plan (not inside Campaigns) to allow easy querying of "All Ads" for a client. They are linked to campaigns via `campaign_id`.
*   **Fields**:
    *   **Metadata**
        *   `campaign_ref` (reference): Reference to `campaigns/{campaignId}`.
        *   `created_at` (timestamp).
        *   `updated_at` (timestamp).
        *   `status` (enum): `"In_Progress"` | `"Approved_by_lf"` | `"Live"` | `"Paused"` | `"Ended"`.
    
    *   **Core Data**
        *   `ad_name` (string): Internal name for the ad.
        *   `img` (string): URL to the image.
        *   `platform` (array of strings): `"meta"` | `"snapchat"` | `"tiktok"` | `"youtube"` | `"pinterest"`.
        *   `media_type` (string): `"image"` | `"video"` | `"carousel"`.
        *   `landing_page` (string): URL.
        *   `assets_link` (string): URL to Google Drive/Dropbox.
        *   `comments` (string): Internal notes.

    *   **Tags** (List of Structs)
        *   `tags` (array of objects): List of selected tags using the same Data Type as `content_plans`.
            *   **FlutterFlow Type**: `List <Data Type: Tag>`
            *   **Structure**:
            ```json
            [
              {
                "category": "Audience",
                "options": ["B2B"] 
              },
              {
                "category": "Product",
                "options": ["Shoes"]
              }
            ]
            ```
            *Note: Even though we select only one option usually, keeping it as a list `options` allows for multi-select in the future and reuses the same Data Type.*

    *   **Platform Specific Data** (Map)
        *   `platform_content` (map): Structure depends on `platform` field.

            **If `platform` contains "meta"**
            ```json
            {
              "meta": {
                 "preview_text": ["Text 1", "Text 2", ...], // Max 5
                 "headlines": ["Headline 1", "Headline 2", ...] // Max 5
              }
            }
            ```

            **If `platform` contains "snapchat"**
            ```json
            {
              "snapchat": {
                 "headlines": ["Headline 1"] // Max 1
              }
            }
            ```

            **If `platform` contains "tiktok"**
            ```json
            {
              "tiktok": {
                 "ad_text": ["Ad text content"] // Max 1
              }
            }
            ```

            **If `platform` contains "youtube"**
            ```json
            {
              "youtube": {
                 "headline": ["Main Headline"],
                 "short_headline": ["Short version"],
                 "long_headline": ["Long version"]
              }
            }
            ```

            **If `platform` contains "pinterest"**
            ```json
            {
              "pinterest": {
                 "headline": ["Main Headline"],
                 "description": ["Description text"]
              }
            }
            ```

## Querying Strategy (FlutterFlow)

1.  **View "All Ads"**:
    *   Query `content_plans/{planId}/ads`.
    *   Filter by `status` if needed.

2.  **View "Always On"**:
    *   Query `content_plans/{planId}/ads`.
    *   Filter by `campaign_id` == ID of the "Always On" campaign.

3.  **View Specific Campaign**:
    *   Query `content_plans/{planId}/ads`.
    *   Filter by `campaign_id` == `{selectedCampaignId}`.

4.  **Filter by Tags**:
    *   Query `content_plans/{planId}/ads`.
    *   Filter by `tags.Audience` == `"B2B"`.

## Security Rules (Brief)
*   **Users**: Can read/write their own document.
*   **Content Plans**: Users can read/write if `client_ref` matches their auth ID (or if they are admin).
*   **Subcollections (ads, campaigns)**: Inherit access from the parent `content_plan`.

### 5. `platforms (Optional)` (Root Collection - Configuration)
This collection acts as the **Source of Truth** for available platforms.
*   **Document ID**: MUST be one of the standard IDs below.
*   **Fields**:
    *   `name` (string): Display name (e.g., "Meta").
    *   `icon_url` (string): URL to icon.
    *   `field_config` (map): Defines which fields are active and their limits.

#### Standard Platform IDs & Configuration (Reference)
These IDs are hardcoded in the App's Conditional Visibility logic.

| Platform ID | Name            | Fields (in `platform_content`)                            |
| :---------- | :-------------- | :-------------------------------------------------------- |
| `meta`      | Meta (FB/Insta) | `preview_text` (1-5), `headline` (1-5)                    |
| `snapchat`  | Snapchat        | `headline` (1)                                            |
| `tiktok`    | TikTok          | `ad_text` (1)                                             |
| `youtube`   | YouTube         | `headline` (1), `short_headline` (1), `long_headline` (1) |
| `pinterest` | Pinterest       | `headline` (1), `description` (1)                         |

#### Linking Strategy
1.  **Global Config**: The `platforms` collection stores the limits (e.g., Meta Headline = 40 chars).
2.  **Client Access**: The `content_plans` document has `enabled_platforms: ["meta", "tiktok"]`. This filters the Dropdown in the UI.
3.  **Ad Data**: The `ads` document saves `platform: "meta"` and stores data in `platform_content`.

**Example `platforms` document (meta):**
```json
{
  "name": "Meta",
  "field_config": {
    "headline": { "label": "Rubrik", "max_chars": 40, "max_items": 5, "is_active": true },
    "preview_text": { "label": "Förtext", "max_chars": 125, "max_items": 5, "is_active": true }
  }
}
```

