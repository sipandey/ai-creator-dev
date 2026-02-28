## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.
## 2024-03-01 - Mitigated User Enumeration Timing Attack
**Vulnerability:** The `/login` endpoint returned `None` immediately if a user was not found, whereas it spent ~300ms computing a bcrypt hash if the user existed, allowing attackers to enumerate valid email addresses via timing discrepancies.
**Learning:** In authentication services, the code path execution time should be roughly identical regardless of whether an account exists. Even when an account is missing, we must perform the slow hashing operation (e.g. bcrypt) to mask the non-existence.
**Prevention:** Use a globally initialized `DUMMY_HASH` and invoke the hashing function against it when a requested user is not found, before returning an error.
