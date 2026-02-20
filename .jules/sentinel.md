## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-01 - User Enumeration via Timing Attack
**Vulnerability:** `authenticate_user` returned immediately if a user was not found (~1ms), while verifying a password for an existing user took significantly longer (~340ms due to bcrypt). This allowed attackers to enumerate valid email addresses.
**Learning:** Security mechanisms like bcrypt (slow hashing) can inadvertently create side-channel vulnerabilities if not applied consistently across all code paths.
**Prevention:** Implement constant-time comparison logic (e.g., verifying a dummy hash) for failure cases to mask the difference between "user not found" and "wrong password".
