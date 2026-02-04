## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2025-02-18 - Missing Password Complexity Validation
**Vulnerability:** `SignupRequest` model accepted empty and short passwords due to missing validation on the Pydantic model.
**Learning:** Pydantic models in this codebase may rely solely on type hints (`str`) without implementing specific validators (like `min_length` or `field_validator`).
**Prevention:** Always verify Pydantic models include validation rules (using `Field` constraints or `@field_validator`) for sensitive inputs, not just type definitions.
