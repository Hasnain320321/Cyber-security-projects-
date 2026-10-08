# Windows Privilege Escalation Hunt — Screenshot Evidence

**Status: No screenshots collected or committed for this project yet.**

This directory is deliberately separate from:
- `SOC-Home-Lab/screenshots/`
- `Windows-Authentication-Investigation/screenshots/`

## Proposed evidence plan

1. `01-audit-policy.png` — Windows audit policy checked before any change.
2. `02-existing-admin-membership.png` — Approved baseline/permissions (review for sensitive identity data).
3. `03-event-4732-security-log.png` — Event 4732, member, subject and group fields.
4. `04-wazuh-4732-event.png` — SIEM visibility.
5. `05-custom-group-change-alert.png` — Custom Wazuh rule, if actually deployed.
6. `06-event-4733-rollback.png` — Removal event.
7. `07-restored-admin-membership.png` — Confirm post-test group membership matches intended state.
8. `08-negative-test.png` — Evidence a nonprivileged change does not alert as an Administrators change.

The list is **planned**, not proof that any action was performed. Review screenshots for identifiable/sensitive account details before publicly uploading them.
