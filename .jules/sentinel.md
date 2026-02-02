## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-02 - Missing Input Validation in Script Generation
**Vulnerability:** The /script endpoint accepted raw dict payload without validation, allowing potential DoS (long inputs) or invalid data.
**Learning:** Using `payload: dict` in FastAPI bypasses Pydantic validation. Always use a Pydantic model for request bodies.
**Prevention:** Enforce Pydantic models for all POST/PUT bodies with explicit field constraints (min_length, max_length).
