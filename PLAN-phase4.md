# Phase 4 Plan — Booking, Contact, Login

## Current State Summary

### Booking (`templates/main_app/booking.html`)
- 217 lines. Hero contains fabricated stats ("24h response time", "48h cancellation", "25% deposit").
- Sidebar has fake phone/email ("+1 555 123-4567", "bookings@justtech.com"), duplicated booking policies.
- "Most popular" card section at the bottom adds noise vs. form clarity.
- Success state (`components/booking_success.html`) promises "within 24 hours" — fabricated.
- HTMX: `hx-post` → `#booking-form-container` outerHTML swap. Service-price HTMX on `#id_service` change.
- `forms.py`: BookingForm with `.form-input` / `.form-label` on all widgets, placeholders.
- `views.py`: Pre-selects service via `?service=slug`, passes `popular_services` (is_popular) and `faqs` (contact category).

### Contact (`templates/main_app/contact.html`)
- 248 lines. Hero promises "one business day" reply — fabricated.
- Sidebar has fake address ("123 Tech Avenue"), fake phone, fake emails, fake business hours, `#` social links.
- "Quick links" section (Book/Services/Pricing) distracts from form purpose.
- FAQ has fabricated fallback questions when DB empty.
- Success state (`components/contact_success.html`) promises "within one business day" — fabricated.
- `views.py`: passes `contact_faqs` (FAQ category='contact').

### Login (`templates/main_app/login.html`)
- 67 lines. Centered card layout — works well structurally.
- "Sign in to manage your bookings and registrations" — promises nonexistent features.
- "Remember me" checkbox has no backend support.
- "Forgot password?" links to /contact — misleading since no recovery exists.
- Custom `login_view` using `authenticate()`/`login()`. Works fine.

### CSS
- `.form-input` (631-696): full width, 0.75rem 1rem padding, `margin-bottom: 0.75rem`, focus ring with `--primary`, dark mode support, select/date styling. Well-defined.
- `.form-label` (660-670): block, 0.8125rem, weight 600, dark mode support.
- No error-specific or required-indicator CSS yet.

---

## Changes

### 1. `templates/main_app/booking.html` — Full Rewrite

**Hero** — Compact:
- Eyebrow: BOOK JUSTTECH
- Headline: Tell us what you need.
- Supporting: Share the details of your event, setup or project and we'll have the information needed to understand the request.
- Remove all fabricated stats (24h/48h/25%).
- Keep gradient background (consistent with homepage/services/learning/about).

**Form section** — Two-column layout (lg:grid-cols-5), form left (col-span-3), info right (col-span-2):
- Form card: Eyebrow "Book now", heading "Reserve your slot".
- Remove redundant group label "Your information" — use individual labels directly.
- Each field in its own div. Labels visible (not just placeholders). Required fields marked with red asterisk via new `.form-required` CSS.
- Per-field error rendering: `{% if form.name.errors %}<p class="form-error">{{ form.name.errors.0 }}</p>{% endif %}` below each input.
- Top-level error summary removed (replaced by per-field).
- Submit button: "Submit request" with calendar icon.
- Keep HTMX attributes unchanged: `hx-post="{% url 'booking' %}"`, `hx-target="#booking-form-container"`, `hx-swap="outerHTML"`, `method="POST"`, `action="{% url 'booking' %}"`.
- Keep `{% csrf_token %}`.
- Keep service_price HTMX include and JS listener script.

**Info panel** (right column) — Replace fabricated sidebar with:
- "What happens next" — 3 numbered steps:
  1. Send your request
  2. JustTech reviews the details
  3. The next step is discussed with you
- Keep the phone/email links from SiteSettings but remove fabricated fallback defaults. Only show if `site_settings.phone` / `site_settings.booking_email` exist. If no SiteSettings row, hide the entire info panel and let the form go full-width (or show only the "What happens next" section).
- Remove "Booking policies" section (fabricated).

**Remove** "Most popular" card section at the bottom (distracts from form clarity on a functional page).

**Success state** (`components/booking_success.html`):
- Change "Booking confirmed!" → "Booking request received"
- Remove "Our team will contact you within 24 hours" → "Your booking request has been received. We'll review the details and follow up."
- Add three action buttons: Return Home, Explore Services, Contact Us.
- Keep green panel styling.

### 2. `templates/main_app/contact.html` — Full Rewrite

**Hero** — Compact:
- Eyebrow: CONTACT
- Headline: Let's talk about what you need.
- Supporting: Whether it's an event, a system, a custom PC or something you want to learn, send us the details.
- Remove "we usually reply within one business day" promise.

**Form section** — Two-column layout (lg:grid-cols-5), info left (col-span-2), form right (col-span-3):
- Form card: Eyebrow "Send a message", heading "Tell us what you need".
- Per-field errors (same pattern as booking).
- Submit button: "Send message" with paper-plane icon.
- Keep HTMX: `hx-post="{% url 'contact' %}"`, `hx-target="#contact-form-container"`, `hx-swap="outerHTML"`.

**Info panel** (left column) — Contact details:
- Only render contact blocks if `site_settings` values exist (phone, email, address).
- Each block: `{% if site_settings.phone %}...{% endif %}`.
- If no SiteSettings row exists at all, the info column content is hidden — form goes full-width or info column shows just the "What happens next" section.
- Remove fabricated fallback defaults entirely.
- Remove social media links section (all `#` — no real data).
- Remove business hours section (fabricated).
- Remove "Quick links" section (Book/Services/Pricing cards).

**FAQ section** — Wrap in `{% if contact_faqs %}`:
- Only show when real FAQ data exists in DB.
- Remove all fabricated fallback questions.
- Remove entire FAQ section when empty.

**Success state** (`components/contact_success.html`):
- Remove "within one business day" promise.
- Safe wording: "Your message has been received."
- Keep Return Home button.

### 3. `templates/main_app/login.html` — Rewrite

**Layout** — Keep centered card (max-w-md), but:
- Remove full-screen hero marketing copy.
- Eyebrow: SECURE LOGIN
- Headline: Welcome back
- Remove "Sign in to manage your bookings and registrations" — replace with "Access is provided to authorised users."
- Remove "Remember me" checkbox (no backend support).
- Remove "Forgot password?" link (no recovery functionality).
- Keep "Don't have an account? Contact us to get access." (reflects reality).
- Add show/hide password toggle (accessible, no external libs):
  - `<button type="button" aria-label="Show password">` positioned in password field.
  - JS toggles input type between `password` and `text`.
  - Updates aria-label on toggle.
- Keep error display (existing `{% if error %}` block).
- Keep `{% csrf_token %}`, `method="POST"`, `action="{% url 'login' %}"`.
- Keep `next` hidden input handling.

### 4. `static/css/styles.css` — Add Shared Form Utilities

Add after existing `.form-label` rules (~line 670):

```css
.form-error {
    font-size: 0.8125rem;
    color: #dc2626;
    margin-top: -0.375rem;
    margin-bottom: 0.75rem;
}

.dark .form-error {
    color: #f87171;
}

.form-required::after {
    content: '*';
    color: #dc2626;
    margin-left: 0.25rem;
}

.dark .form-required::after {
    color: #f87171;
}
```

That's it — two small utility classes. No over-engineering.

### 5. No Backend Changes

- `forms.py` — No changes needed. All widgets already have `.form-input` / `.form-label`.
- `views.py` — No changes needed. All three views (booking, contact, login_view) work correctly.
- `models.py` — No changes needed.
- `urls.py` — No changes needed.

---

## Files Changed

| File | Action | Lines (approx) |
|------|--------|----------------|
| `templates/main_app/booking.html` | Full rewrite | ~180 |
| `templates/main_app/components/booking_success.html` | Rewrite | ~20 |
| `templates/main_app/contact.html` | Full rewrite | ~170 |
| `templates/main_app/components/contact_success.html` | Rewrite | ~15 |
| `templates/main_app/login.html` | Rewrite | ~75 |
| `static/css/styles.css` | Add 2 small rules | +15 |

No Python files modified.

---

## Verification Checklist

1. `manage.py check` — 0 issues
2. All routes return 200 (test client, HTTP_HOST='localhost')
3. Booking: form renders, service pre-selection works, HTMX submission works, success fragment renders
4. Booking: dynamic service price updates via HTMX still work
5. Booking: per-field errors render (test with empty POST)
6. Contact: form renders, HTMX submission works, success fragment renders
7. Contact: per-field errors render (test with empty POST)
8. Contact: FAQ section hidden when DB empty
9. Contact: fake contact details hidden when no SiteSettings
10. Login: form renders, valid login works, invalid login shows error
11. Login: no "Remember me", no "Forgot password?", no registration promise
12. Login: show/hide password toggle works (if implemented)
13. No fabricated content in any template (grep for fake phone, fake email, fake address, "24 hours", "one business day", "Netflix", "founded")
14. Templates compile
15. Mobile: forms full-width on mobile, no horizontal overflow, buttons tap-friendly
