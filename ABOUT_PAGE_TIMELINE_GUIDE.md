# About Page Timeline Guide

## Overview
The About page now features a beautiful timeline structure that tells your life story across three main periods:
- **My Past** - Your history and formative experiences
- **My Present** - What you're doing now
- **My Future (Aspirations)** - Your goals and vision

## How to Add Timeline Entries

### 1. Access the Admin Panel
Go to: http://127.0.0.1:8000/admin/

### 2. Navigate to Timeline Entries
- Click on "Timeline Entries" in the Portfolio section
- Click "Add Timeline Entry" button

### 3. Fill in the Fields

#### Required Fields:
- **Period**: Choose from:
  - My Past (for historical entries)
  - My Present (for current activities)
  - My Future (Aspirations) (for goals and vision)
  
- **Year**: The year this entry represents (e.g., 2013, 2022, 2030, 2050)

- **Title**: A descriptive title for this period
  - Examples: "Me as a Kid", "Me in 2022", "Me in 2050"

- **Content**: Rich text description of this period
  - Supports HTML formatting through TinyMCE editor
  - Tell your story, share experiences, describe aspirations

#### Optional Fields:
- **Image**: Upload a photo representing this period
- **Order**: Control the display order within each period (lower numbers first)
- **Is Active**: Toggle to show/hide this entry

### 4. Short Bio Section
In the Profile section, you can now add a "Short Bio" that appears at the top of the About page, before the timeline. This is separate from your main bio.

## Example Timeline Structure

### My Past
- **Me as a Kid (2005)**: Early childhood memories and interests
- **Me in 2013**: High school years and discovering passions
- **Me in 2018**: Starting university journey
- **Me in 2022**: Graduation and first career steps

### My Present
- **Me in 2025**: Current role as Research Assistant and AI student

### My Future (Aspirations)
- **Me in 2030**: Career goals and research ambitions
- **Me in 2040**: Long-term professional vision
- **Me in 2050**: Legacy and impact aspirations
- **Me in 2070**: Life wisdom and reflections

## Design Features

### Visual Styling:
- **Past entries**: Blue badges and standard cards
- **Present entries**: Green badges with green borders
- **Future entries**: Yellow/warning badges with yellow borders

### Interactions:
- Cards have hover effects (lift up slightly)
- Smooth animations on scroll (AOS library)
- Responsive design for mobile and desktop

### Layout:
- Images appear on the left (if provided)
- Content flows naturally with rich text formatting
- Year badges prominently displayed
- Clean, modern card-based design

## Tips for Great Content

1. **Be Authentic**: Share genuine experiences and aspirations
2. **Use Images**: Photos make entries more engaging and personal
3. **Vary Length**: Some entries can be brief, others more detailed
4. **Balance Periods**: Don't need equal numbers in each section
5. **Update Regularly**: As life changes, update your Present and Future sections
6. **Rich Formatting**: Use bold, italics, lists in the content editor

## Technical Details

### Models:
- `TimelineEntry`: Stores each timeline entry
- `Profile.short_bio`: New field for About page intro

### Admin Features:
- List view shows: Title, Period, Year, Active status, Order
- Filter by: Period, Active status, Year
- Search: Title and content
- Bulk edit: Order and Active status

### URL:
View your About page at: http://127.0.0.1:8000/about/

## Empty State
If no timeline entries exist, the page shows a friendly message encouraging you to add entries through the admin panel.

---

**Ready to tell your story!** Start adding timeline entries in the admin panel to create your personal journey timeline.
