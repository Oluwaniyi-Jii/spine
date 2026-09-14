# Power BI Dashboard Specification — Shelf Data Warehouse

This document outlines the visual layout, report pages, DAX measures, and filter configurations for the 3 core Power BI dashboard pages in Shelf.

---

## Page 1: Publishing Landscape Overview
- **Header KPIs**:
  - Total Works (`Total Works`)
  - Total Editions (`Total Editions`)
  - Total Authors (`Total Authors`)
  - Active Publishers (`DISTINCTCOUNT(dim_publisher)`)
- **Main Visuals**:
  - **Editions by Publication Decade**: Column chart (`dim_date[decade]` vs `Total Editions`).
  - **Top 10 Publishers by Output**: Horizontal bar chart (`dim_publisher[canonical_name]` vs `Total Editions`).
  - **Editions by Physical/Digital Format**: Donut chart (`dim_format[format_name]`).
  - **Language Distribution**: Treemap (`dim_language[language_name]`).

---

## Page 2: Publishing Timeline Centerpiece
- **Interactive Slicers**:
  - Search Work Title (Dropdown / Search box)
  - Author Slicer
  - Publication Year Range Slider (1800 - 2030)
- **Main Visual**:
  - **Work Publishing Timeline**: Scatter / Gantt plot (`mart_publishing_timeline`).
    - X-axis: `edition_publication_year`
    - Y-axis: `work_title`
    - Legend: `publisher_name`
    - Tooltip details: Title, Format, ISBN, Page Count, Language.

---

## Page 3: Authors & Literary Analytics
- **Main Visuals**:
  - **Author Career Span Scatter**: Scatter plot (`first_edition_year` vs `publishing_career_span_years`, bubble size = `total_editions_published`).
  - **Readability Index vs Publication Era**: Line chart (`publication_year` vs `Avg Readability Score`).
  - **Dialogue Percentage by Literary Subject**: Bar chart (`subject_name` vs `Avg Dialogue Percentage`).
