# QAQC Report Generator — Pre-Release UI/UX Feedback

> **Date:** 2026-02-10  
> **Branch:** `pre-release`  
> **Tested by:** Automated testing walkthrough (Antigravity agent)

---

## Summary

During comprehensive testing of the QAQC Report Generator web UI, 7 issues were identified across 3 severity categories. This document serves as the official feedback record.

---

## 🐛 Bugs (Priority: High)

### 1. React Hook Order Error During Navigation
**Severity:** High  
**Location:** Session creation / page transitions  
**Description:** A React hook ordering error occasionally fires during session creation or when navigating between pages. The error doesn't crash the app but can briefly blank the page content.  
**Impact:** First-time users may think the app is broken.  
**Workaround:** Page reload recovers the UI.  
**Fix:** Audit conditional hook calls in components that render during navigation.

### 2. Report Generation — No Success Feedback
**Severity:** High  
**Location:** Report Export page → "Generate JORC Report (DOCX)" button  
**Description:** After clicking the generate button, the UI provides no visual feedback — no toast notification, no progress bar, no download prompt. Console logs show processing activity, but the user sees nothing.  
**Impact:** Users cannot tell if the report was generated successfully.  
**Fix:** Add a toast notification on success/error and trigger browser file download.

---

## 😕 Confusing UX Flows (Priority: Medium)

### 3. Report Options Split Across Two Pages
**Severity:** Medium  
**Location:** Settings page + Report page  
**Description:** "Include Cover Page" and "Include JORC Table 1" toggles are on the **Settings** page, but all other report configuration (Author, Company, format, etc.) is on the **Report** page. Users must navigate between two pages to fully configure a report.  
**Impact:** Unintuitive workflow; settings feel disconnected from report generation.  
**Fix:** Duplicate the report option toggles onto the Report page (keep them in Settings as defaults).

### 4. Sample Data Skips Preview & Column Mapping
**Severity:** Low  
**Location:** Data Import → Sample data selection  
**Description:** When loading sample data (e.g. "Gold Fire Assay"), the app skips the data preview table and column mapping steps, jumping directly to Analysis Setup. There's no indication that steps were skipped.  
**Impact:** Testers may not find those features; users may wonder what happened.  
**Fix:** Show a brief info toast: "Sample data loaded — preview and column mapping skipped."

---

## 💡 Minor Polish (Priority: Low)

### 5. CRM Search — No Clear Button
**Severity:** Low  
**Location:** CRM Database → search input  
**Description:** After typing in the CRM search bar, there's no "×" clear button to reset the filter. Users must manually select and delete the text.  
**Fix:** Add a clear/reset button to the search input.

### 6. Backend Status Wording Inconsistency
**Severity:** Low  
**Location:** Multiple pages  
**Description:** The backend connectivity indicator uses different labels:
- Dashboard / CRM Database: `"Server Connected"` (green badge)
- Settings: `"Backend Connection: Connected"` (text label)  
**Fix:** Standardise the label to `"Server Connected"` everywhere.

---

## Test Coverage Matrix

| Feature | Tested | Issues Found |
|---------|:------:|:------------:|
| Session Management | ✅ | #1 |
| Data Import | ✅ | #4 |
| Analysis Setup | ✅ | — |
| Results Dashboard | ✅ | — |
| CRM Database | ✅ | #5 |
| Settings | ✅ | #6 |
| Report Export | ✅ | #2, #3 |
| CLI Workflow | ✅ | — |
