Kilopyte Wiki
=============
Overview
--------
**Goal:** A minimal, but complete, WikiWikiWeb implemented in python,
using the WSGI standard and only standard library.

A minimal and complete wiki will have:
 - Editable pages
 - Simple, but non-GUI markup
 - A limited history (1 week, 1 month, 1 year TBD)
 - A Recent changes page

**Status:** Struggling to figure out the right way to test this
 - Uncertain on how to test HTML or HTML responsiveness
 - Struggling to figure out which features to implement next
 - Feature list and scenarios unclear

**Actions:** 
 - Research testing
 - Create some sort of story list or story map
 - Find other open source tools and approachs

Functional Requirements:
------------------------
```
 - POST to a valid WikiWord URL to create or edit a page.
    ✓ Also accept posts to `/` to create or edit the welcome page.
    - Validate wikiwords
 - GET to a valid WikiWord URL to get the current contents.
    - If no page yet exists, redirect to an edit page.
    - Validate wikiwords
 - Renderable HTML5.
 - Syntax is a subset of the wikicreole markup language.
 - Immune to XSS or injection attacks.
 - Saves pages to a persistent database file.
 - Is WSGI service.
 - Runnable from wsgiref
```

Non-functional Requirements:
----------------------------
```
 - Tests are full-stack
```
