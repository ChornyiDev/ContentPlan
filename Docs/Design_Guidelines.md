# Responsive Design Guidelines & UI Principles

## 1. Core Layout Strategy (Max-Widths)
To ensure the app looks professional on large screens, **never let content stretch infinitely**.

*   **Main Content Container (Desktop):**
    *   **Max-Width:** `1200px` or `1400px`.
    *   **Alignment:** Center the container (`Margin Left/Right: Auto` or `Alignment: (0, 0)` in FlutterFlow).
    *   *Why:* Reading lines longer than 800-1000px is difficult for the eye.

*   **Lists & Tables (Ads/Plans):**
    *   **Max-Width:** `1200px`.
    *   **Behavior:** On wider screens, add padding on sides or center the list.

*   **Forms (Create/Edit Ad):**
    *   **Max-Width:** `600px` to `800px`.
    *   *Why:* Input fields look broken if they are too wide. Center the form on the page.

## 2. Breakpoints (FlutterFlow Defaults)
*   **Mobile:** < 479px (Phone Portrait)
*   **Tablet:** 480px - 991px (Tablet / Large Phone Landscape)
*   **Desktop:** > 992px (Laptop / Monitor)

## 3. Navigation Patterns
*   **Desktop (> 992px):**
    *   Use a **Left Sidebar** (fixed width, e.g., 250px).
    *   Allows quick switching between Plans/Campaigns.
*   **Mobile/Tablet (< 991px):**
    *   Use a **Hamburger Menu (Drawer)** or **Bottom Navigation Bar**.
    *   Hide the sidebar to save space.

## 4. Component Behavior

### Lists vs Grids
*   **Mobile:** Use a **List View** (1 column). Cards take full width.
*   **Tablet:** Use a **Wrap** or **Grid View** (2 columns).
*   **Desktop:** Use a **Grid View** (3-4 columns) OR a **Data Table** (rows).

### Cards (Ad Items)
*   **Fixed Height is Risky:** Avoid fixing height if content varies (e.g., long headlines). Let content expand.
*   **Touch Targets:** On mobile, buttons/icons must be at least `44x44px`. On desktop, `32x32px` is acceptable.

## 5. Spacing & Typography
*   **Padding:**
    *   **Mobile:** `16px` horizontal padding.
    *   **Desktop:** `32px` to `64px` horizontal padding (inside the max-width container).
*   **Font Sizes:**
    *   **Headings:** Scale down on mobile (e.g., H1: 32px Desktop -> 24px Mobile).
    *   **Body Text:** Keep readable (14px - 16px).

## 6. Specific to Ad Directory
*   **Filters:**
    *   **Desktop:** Show filters as a sidebar or a top bar (Chips).
    *   **Mobile:** Hide filters inside a "Filter" button/modal (BottomSheet).
*   **Action Buttons (Create Ad):**
    *   **Desktop:** Top-right corner of the list.
    *   **Mobile:** Floating Action Button (FAB) bottom-right.
