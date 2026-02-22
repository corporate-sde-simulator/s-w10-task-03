# DATA-201: Fix Broken Sales Reporting Queries

**Status:** In Progress · **Priority:** High
**Sprint:** Sprint 31 · **Story Points:** 5
**Reporter:** Finance Team · **Assignee:** You (Intern)
**Labels:** `sql`, `database`, `reporting`, `bug-fix`
**Task Type:** Bug Fix

---

## Description

The quarterly sales dashboard is showing wrong numbers. Three SQL queries in the
reporting module have bugs: wrong JOINs, missing WHERE clauses, and GROUP BY errors.

## Acceptance Criteria

- [ ] Total revenue query returns correct sum per region
- [ ] Customer report includes customers WITH orders (not all)
- [ ] Monthly breakdown groups by month correctly
- [ ] All tests pass
