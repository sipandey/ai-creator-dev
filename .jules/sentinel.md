## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-15 - Missing Password Validation
**Vulnerability:** `SignupRequest` model accepted any string as a password, including single characters, allowing for extremely weak passwords.
**Learning:** Pydantic models require explicit `Field` constraints or validators for string fields; default type hints only enforce the type, not the content.
**Prevention:** Always use `Field(..., min_length=X)` for string inputs that have security requirements, and add regex validators for complexity.
