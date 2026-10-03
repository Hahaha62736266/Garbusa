# Final Project Retrospective

**Project:** Aquaflow Tracker
**Phase:** 6 (Retrospective & Demo)
**Date:** 2026-10-03

---

## 🧐 What went well?

1.  **Architecture & Separation of Concerns:** Building the backend controllers first (Phase 2) and thoroughly testing them with `pytest` made wiring up the frontend (Phase 3) significantly easier. We knew the APIs were robust before we even built the HTML.
2.  **AI Scaffolding:** Using AI to scaffold the initial boilerplate for Tailwind UI components (like the Dashboard and Orders Table) saved hours of CSS tweaking, allowing us to focus on the JavaScript `fetch` bindings and application state logic.
3.  **Security Foundations:** Implementing hashed passwords with `werkzeug.security` and strictly using the `SUPABASE_SECRET_KEY` on the backend ensured we never accidentally exposed the database to public clients.

## 🤔 What didn't go well?

1.  **State Management Complexity:** Handling Loading, Error, and Empty states purely with Vanilla JavaScript (`classList.add('hidden')`) became verbose quickly. There are many IDs to track in `orders.html`.
2.  **Testing the UI:** While our backend integration tests were excellent, manually testing the UI was tedious and prone to human error (e.g., forgetting to test a boundary condition).

## 💡 What would we change next time?

1.  **Frontend Framework:** For an application with this much dynamic state (Orders, Live Charts, Action Modals), migrating from static HTML + Vanilla JS to a lightweight framework like React, Vue, or Alpine.js would significantly reduce the boilerplate code needed to manage the UI state.
2.  **Automated UI Tests:** We would implement a tool like Playwright or Cypress to automate the adversarial UI tests rather than relying solely on a manual QA matrix.

## 🎓 Concrete Lessons Learned (No Blame)

*   **Lesson 1:** *Never trust the client.* Even with HTML5 `required` and `min="1"` attributes, the backend MUST re-validate every piece of data. We saw this when we submitted negative numbers via Postman.
*   **Lesson 2:** *Disable submit buttons immediately.* Network requests take time. If you don't disable a button the millisecond it is clicked, users *will* click it twice and create duplicate records.
*   **Lesson 3:** *Always parse error responses.* A `500` error is useless to a user. Grabbing the specific `422` error message from the JSON body (`data.error`) and displaying it in a toast/modal turns a frustrating bug into an actionable fix.
