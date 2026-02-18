## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-05-23 - User Enumeration via Timing Attack
**Vulnerability:** The authentication logic (`apps/api/app/services/auth_service.py`) returned immediately if a user was not found, while valid users triggered a slow bcrypt verification.
**Learning:** Even if `verify_password` uses constant-time comparison, skipping it entirely for invalid users leaks information via response timing.
**Prevention:** Implement `DUMMY_HASH` verification for invalid users to ensure consistent response times regardless of user existence.
