## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-01 - User Enumeration via Timing Attack
**Vulnerability:** `authenticate_user` returned immediately if a user was not found, while valid users underwent a slow `bcrypt` verification. This allowed attackers to enumerate valid email addresses based on response time.
**Learning:** Security controls like `bcrypt` introduce significant latency, making timing differences extreme (~800x) if not mirrored in failure paths.
**Prevention:** Always ensure that authentication failure paths (user not found vs. wrong password) take approximately the same amount of time by performing a dummy verification.
