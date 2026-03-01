## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2025-03-01 - User Enumeration Timing Attack
**Vulnerability:** The `/auth/login` endpoint took significantly less time to respond when an email was not found compared to when it was found. This is a timing attack vulnerability that allows attackers to enumerate valid user emails.
**Learning:** `bcrypt` hashing is computationally expensive. If `verify_password` is skipped when `user` is `None`, the execution time drops by hundreds of milliseconds.
**Prevention:** Implement a constant-time check pattern. When a user is not found, always call `verify_password(password, DUMMY_HASH)` using a pre-computed valid bcrypt hash. This ensures both valid and invalid email lookups incur the same computational cost.
