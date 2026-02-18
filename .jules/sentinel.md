## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-05-23 - User Enumeration via Timing Attack
**Vulnerability:** `authenticate_user` returned immediately if a user was not found, while verifying the password (slow bcrypt) if the user existed.
**Learning:** Even with secure hashing libraries (bcrypt), the logic flow can leak information. Secure coding requires constant-time execution paths for sensitive operations.
**Prevention:** Always perform a dummy verification (e.g., against a `DUMMY_HASH`) in the failure path of authentication to equalize timing.
