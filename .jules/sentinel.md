## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-04 - Weak Password Policy
**Vulnerability:** User signup endpoint accepted arbitrary password lengths (e.g., "123").
**Learning:** Pydantic models need explicit validators for business logic rules like password strength; standard types like `str` are insufficient.
**Prevention:** Use `@field_validator` in Pydantic schemas to enforce minimum security requirements (length, complexity) at the input layer.
