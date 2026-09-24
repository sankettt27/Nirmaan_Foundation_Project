# Assignment 4: Our Projects Page + Project Content Management System

## Overview
This assignment extends the Nirmaan Foundation CMS by adding a Project Management module. This feature allows administrators to manage ongoing, completed, and upcoming projects dynamically without touching the frontend code.

The module provides full CRUD capabilities, including image uploads via a related `ProjectImage` model. The frontend `projects.html` showcases all the projects in a modern, responsive, and categorized grid layout, ensuring the public stays informed about the foundation's impact.

## Deliverables
- **Models:** Added `Project` and `ProjectImage` to `cms/models.py`.
- **Forms:** Added `ProjectForm` and `ProjectImageForm` to `cms/forms.py` using Django `ModelForm`.
- **Views:** Added comprehensive CRUD views to `cms/views.py` (`project_list_view`, `project_create_view`, `project_edit_view`, `project_delete_view`, `project_images_view`, `project_image_delete_view`).
- **URLs:** Appended new routes in `cms/urls.py` for CMS operations and `home/urls.py` for the public page.
- **Templates:**
  - `templates/cms/project_list.html`: Displays projects with filtering.
  - `templates/cms/project_images.html`: Interface to manage multiple images per project.
  - `templates/cms/cms_dashboard.html`: Added a new card to direct admins to the Projects CMS.
  - `templates/cms/_sidebar.html`: Appended a quick link in the navigation sidebar.
  - `templates/home/projects.html`: Created a public, fully responsive project showcase layout.
  - `templates/home/base_page.html`: Added navigation links to the header and footer.
- **Tests:** Added `tests/test_assignment4.py` to cover unit testing and view assertions.

## Implementation Details
1. **Backend Integration (Models & Forms):** The `Project` model handles core fields such as title, description, location, status, and dates. The `ProjectImage` model features a `ForeignKey` back to the `Project`, featuring `on_delete=models.CASCADE` ensuring all uploaded images are deleted if the parent project is removed.
2. **Access Control:** All CMS views are wrapped with `@role_required('admin')` to ensure security. Unauthenticated or non-admin access is rejected.
3. **Frontend Design:** The `projects.html` interface utilizes CSS grids, interactive hover states, and dynamic status badging (`Ongoing`, `Completed`, `Upcoming`). It dynamically queries projects via the view based on `?status=` URL parameters.
4. **Dashboard Integration:** Navigating the CMS is streamlined by injecting a new `cms-section-card` representing Projects right into the existing grid of the admin dashboard. The count of projects is dynamically populated in the context.

## Constraints Adhered To
- 🚫 Did NOT use React, Angular, Vue, or any external frontend libraries.
- 🚫 Did NOT create a separate frontend application.
- 🚫 Maintained the existing structure for routing, models, and template rendering.
- ✅ Respected previous assignments (Assignments 1–3) without breaking any existing models or templates.
- ✅ Successfully handled database migrations natively using Django's ORM on the provided MySQL database.
