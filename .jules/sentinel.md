## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2025-02-28 - [HIGH] Weak Password Requirements in User Onboarding
**Vulnerability:** The `SignupRequest` in `apps/api/app/schemas/auth.py` had no validation rules for passwords, accepting very weak and easily guessable passwords (e.g., "1"). Weak passwords can lead to unauthorized access and account takeovers.
**Learning:** In fast-paced startup architectures leveraging pure Pydantic schemas without forms libraries, standard password complexity validation is often completely omitted unless explicitly written.
**Prevention:** Always include strong password complexity rules via a `@field_validator` on any Pydantic models handling new passwords or password resets. A minimum of 8 characters, at least 1 digit, and at least 1 uppercase letter is a standard baseline.
