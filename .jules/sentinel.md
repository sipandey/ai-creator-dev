## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-05 - User Enumeration via Timing Attacks
**Vulnerability:** `authenticate_user` returned immediately when a user was not found, while executing expensive `bcrypt` verification for existing users.
**Learning:** This discrepancy allowed attackers to distinguish between valid and invalid emails by measuring response time.
**Prevention:** Implement a `DUMMY_HASH` constant generated at startup and verify against it when a user is not found to normalize response times.
