## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-12 - User Enumeration via Timing Discrepancy
**Vulnerability:** The authentication flow (`authenticate_user` in `apps/api/app/services/auth_service.py`) returned immediately if a user was not found, creating a ~340ms timing difference compared to password verification for existing users.
**Learning:** Bcrypt hashing is computationally expensive by design. Skipping it on user-not-found creates a massive side channel.
**Prevention:** Always ensure "user not found" and "invalid password" paths take roughly the same amount of time by performing a dummy verification against a pre-calculated hash.
