# ellaella.io - Design System & UI Guide

## Overview
This document defines the core **Design Tokens** (Colors, Typography, Shadows, Spacing, and Radii) used for the new Workspace level (Super Admin & Workspace Admin Panels). 

This system leans into a clean, modern B2B SaaS aesthetic using **Glassmorphism** for depth and premium feel, while maintaining high contrast and accessibility. These exact values should be implemented in **FlutterFlow's Theme Settings**.

---

## 1. Typography 
**Primary Typeface:** `Plus Jakarta Sans`
Google Font URL: `https://fonts.google.com/specimen/Plus+Jakarta+Sans`

*   **Weights Used:**
    *   `Light (300)` - Rarely used, mostly for large decorative numbers.
    *   `Regular (400)` - Body text, descriptions, standard input fields.
    *   `Medium (500)` - Subtitles, secondary buttons, list items.
    *   `SemiBold (600)` - Table headers, small button text, badges.
    *   `Bold (700)` - Page Titles (`h1`), Card Titles (`h3`), Primary Call-to-Action (CTA) buttons.

*   **Sizing Scale (Reference):**
    *   `xs` (12px) - Details, helper texts, badge labels, timestamps.
    *   `sm` (14px) - Table rows, standard text within cards.
    *   `base` (16px) - Primary body text, input fields.
    *   `lg` (18px) - Card Titles.
    *   `xl` (20px) - Section Headers (e.g., "Users", "Content Plans").
    *   `3xl` (30px) - Page Titles (e.g., "Workspace Dashboard").

---

## 2. Color Palette

### 🔵 Brand / Action Colors (Blue/Sky theme)
Used for Primary CTAs, active states, and brand accents.
*   **Brand 50:** `#f0f9ff` (Hover background for brand items)
*   **Brand 100:** `#e0f2fe` (Badge backgrounds)
*   **Brand 500:** `#0ea5e9` (Icons, minor accents)
*   **Brand 600:** `#0284c7` (Hover states)
*   **Brand 700 / Primary:** `#0369A1` **(Main CTA Buttons, Active Links)**
*   **Brand 800:** `#075985` (Hover state for Primary CTA)

### 🔘 Neutrals (Slate theme)
Used for backgrounds, borders, and typography. Gives a cooler, more professional feel than standard gray.
*   **Slate 50:** `#F8FAFC` **(Main App Background)**
*   **Slate 100:** `#f1f5f9` (Card hover backgrounds, alternating table rows)
*   **Slate 200:** `#e2e8f0` (Borders, dividers, empty avatar backgrounds)
*   **Slate 400:** `#94a3b8` (Muted icons, placeholders)
*   **Slate 500:** `#64748b` (Secondary text, helper text)
*   **Slate 600:** `#475569` (Sub-headers, inactive tabs)
*   **Slate 900:** `#0F172A` **(Primary Text, Headings)**
*   **Slate 950:** `#020617` (Darkest text, inverted buttons)

### 🚥 Semantic Colors (Status)
Used for badges and indicating state.
*   **Success (Emerald):** Background `#d1fae5`, Text `#065f46` (e.g., "Active")
*   **Warning (Amber/Orange):** Background `#fef3c7`, Text `#92400e` (e.g., "On Hold", "Reviewing")
*   **Danger (Red):** Text `#ef4444`, Hover `#b91c1c` (e.g., Delete Icons)

---

## 3. Shape & Radii (Border Radius)
*   **Cards & Panels (Glassmorphism containers):** `16px` (Rounded-2xl) or `12px` (Rounded-xl). Gives a friendly yet structured feel.
*   **Standard Content Cards (e.g., Content Plan Card):** `12px` (Rounded-xl).
*   **Buttons & Inputs:** `8px` (Rounded-lg).
*   **Small Badges/Tags:** `4px` (Rounded-sm) or fully rounded (Pill shape).
*   **Avatars:** `50%` (Fully rounded circle).

---

## 4. Spacing & Padding
*   **Page Margins:** 
    *   Max Width: `1280px` (7xl) centered.
    *   Horizontal Padding: `24px` (desktop), `16px` (mobile).
*   **Section Gaps:** `24px` to `32px` between major UI sections (e.g., between Header and Table).
*   **Card Internal Padding:** `24px` (p-6) for large widgets, `20px` (p-5) for smaller cards.
*   **Item Gaps (Flexbox):** `8px` to `16px` between elements like icons and text, or buttons in a row.

---

## 5. UI Effects & Elevation (Shadows & Glass)

### Glassmorphism Panel (Navbars & Sticky Elements)
To achieve the premium frosted-glass look in FlutterFlow:
*   **Fill Color:** `#FFFFFF` (White) at **75% Opacity**.
*   **Backdrop Blur:** `16px`.
*   **Border:** `1px solid rgba(255, 255, 255, 0.5)`.
*   **Shadow:** Light drop shadow (Y: 4, Blur: 6, Color: Black at 5% opacity).

### Main Content Cards (Solid / Subtle Glass)
*   **Fill Color:** `#FFFFFF`.
*   **Border:** `1px solid #e2e8f0` (Slate 200).
*   **Shadow:** None by default.
*   **Hover State:** 
    *   Transform: Move up slightly (`Translate Y: -2px`).
    *   Shadow: `0 4px 12px rgba(0,0,0, 0.05)`.
    *   Border: Changes to Brand color at 30% opacity `rgba(3, 105, 161, 0.3)`.

### Inputs & Form Fields
*   **Standard Input Focus State:**
    *   **Border:** `1px solid #0ea5e9` (Brand 500)
    *   **Focus Ring (Shadow):** `0 0 0 2px rgba(14, 165, 233, 0.2)` (Creates an accessibility-friendly glow)
*   **Search Bar / Floating Inputs:**
    *   **Shadow:** `0 1px 2px 0 rgba(0, 0, 0, 0.05)` (A subtle lift to stand out from normal inputs)

---

## 6. Icons
*   **Library:** Lucide Icons (or equivalent clean, outline-style SVG icons like Heroicons).
*   **Default Size:** `16px` (w-4) or `20px` (w-5).
*   **Stroke Width:** `2px` for consistent readability.
*   **Color:** Default to `Slate 400` or `Slate 500`. On hover, change to `Brand 600` or `Slate 900` depending on the action.
