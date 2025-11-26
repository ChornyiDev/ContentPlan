# Ad Campaign Directory - Content Plan Project
This project is a web-based application for managing ad campaigns and content plans, designed to replace Google Sheets with a more structured and user-friendly interface.

## Documentation

*   **[Database Schema](Docs/Database_schema.md)**
    *   Detailed Firebase Firestore schema definition.
    *   Includes structure for Users, Content Plans, Campaigns, Ads, and Platforms.
    *   Defines platform-specific fields and configuration.

*   **[Implementation Guide: Filtering & Data Types](Docs/Implementation_Filtering.md)**
    *   Guide for implementing dynamic client-side filtering in FlutterFlow.
    *   Definitions for custom Data Types (Structs) required for the project.
    *   Logic for the `filterAdsList` custom function.

## Project Overview
The app allows clients to:
*   View live ads and content plans.
*   Filter ads by dynamic tags (Audience, Product, etc.).
*   Manage "Always On" and specific "Campaign" ads.
*   Handle platform-specific content requirements (Meta, TikTok, etc.).
