```

```
# Proposal: Media Plan Feature for ellaella.io

## Overview
We propose to introduce a dedicated **Media Plan** module within each Content Plan. This feature will allow agencies and their clients to map out budgets, objectives, and weekly schedules dynamically.

Currently, media planning is often handled in large, complex spreadsheets. While spreadsheets are flexible, they do not translate well into a seamless, accessible Web / Mobile application experience.

Instead of migrating a massive grid into the app (which causes poor readability, scrolling issues, and performance overhead), we propose a modern, hierarchical **"Block & Card" interface**.

## Why We Advise Against a "Spreadsheet Table" UI
1.  **Mobile Unfriendly:** A table with 60+ columns (including 52 weeks) breaks entirely on small screens or laptops.
2.  **Structural Rigidity:** In a spreadsheet, adding a custom field (like "KPI" for one platform but not another) means adding a column for the entire sheet, creating empty, confusing space.
3.  **Visual Overload:** Users are presented with a wall of data. A card-based system uses progressive disclosure—showing only what is needed, when it is needed.

---

## 🏗 The "Pyramid" Solution

We propose structuring the Media Plan hierarchically. This gives the client infinite flexibility to add custom fields without breaking the design.

1.  **Campaign (Top Level):** The overall container (e.g., "Q1 Marketing 2024").
2.  **Budget Block (Mid Level):** E.g., "Meta - 100,000 kr". Users can attach custom fields specifically to this budget.
3.  **Segment (Bottom Level):** E.g., "Audience 1". Contains specific placements and the 52-week timeline.

### Conceptual Structure

```mermaid
graph TD
    classDef campaign fill:#1e293b,stroke:#0369a1,stroke-width:2px,color:#fff;
    classDef budget fill:#0ea5e9,stroke:#0284c7,stroke-width:2px,color:#fff;
    classDef segment fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,color:#333;
    classDef customField fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#333,stroke-dasharray: 5 5;
    classDef schedule fill:#dcfce7,stroke:#22c55e,stroke-width:1px,color:#333;

    C["🎬 Campaign<br>(e.g. 'Spring Collection 2024')"]:::campaign

    %% Budget 1
    B1["💰 Budget Block 1<br>Platform: Meta<br>Amount: 100,000 kr"]:::budget
    CF1["Custom Field: KPI = Sales<br>Custom Field: Region = EU"]:::customField
    B1 --- CF1

    %% Budget 2
    B2["💰 Budget Block 2<br>Platform: TikTok<br>Amount: 50,000 kr"]:::budget

    %% Linking Campaign to Budgets
    C ==> B1
    C ==> B2

    %% Segments for Budget 1
    S1["🎯 Segment 1<br>Audience: 18-24<br>Placement: Stories"]:::segment
    S1CF["Custom Field: Creative = Video A"]:::customField
    S1_Sched["📅 Schedule:<br>[✓] Week 10 [✓] Week 11<br>[✕] Week 12 [✓] Week 13"]:::schedule

    S2["🎯 Segment 2<br>Audience: Retargeting"]:::segment
    S2_Sched["📅 Schedule:<br>[ ] Week 10 [ ] Week 11<br>[✓] Week 12 [✓] Week 13"]:::schedule

    B1 ==> S1
    S1 --- S1CF
    S1 --- S1_Sched

    B1 ==> S2
    S2 --- S2_Sched

    %% Segments for Budget 2
    S3["🎯 Segment 3<br>Audience: Gen Z"]:::segment
    S3_Sched["📅 Schedule:<br>[✓] All Weeks"]:::schedule

    B2 ==> S3
    S3 --- S3_Sched
```

---

## 💻 Design Concept

Based on this architecture, we have created an HTML/CSS Prototype using the existing **Glassmorphism B2B Software** design system of ellaella.io.

### Key Features of the Design:
*   **Sticky Campaign Navigation:** Easily jump between campaigns while keeping the "Total Budget" constantly visible.
*   **Clean Budget Cards:** Each platform budget is separated into its own clean card, making it extremely readable and scannable.
*   **Custom Fields as "Chips":** Instead of empty table columns, custom data like *KPIs* or *Periods* are displayed as neat chips next to the budget.
*   **Horizontal Timeline Scroll:** The 52-week schedule is presented as a scrollable timeline within each segment. It keeps the familiarity of the "spreadsheet blocks" while fitting beautifully on any screen size.

### Prototype Screenshot

![Media Plan UI Design Concept](../UI_Prototypes/Screenshot%202026-03-12%20at%2017.24.36.jpg)

This approach provides the exact same data capability as the current spreadsheet, but wrapped in a premium, flexible SaaS interface.
