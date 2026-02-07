## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-06 - Input Validation Gap in Script Generation
**Vulnerability:** The `POST /script` endpoint accepted raw `dict` payload, bypassing validation and allowing potential processing of invalid data (e.g. missing `topic`).
**Learning:** Using `payload: dict` in FastAPI endpoints defeats the purpose of Pydantic validation. It shifts the burden of validation to business logic, which is error-prone.
**Prevention:** Always define and use Pydantic models for request bodies, even for simple payloads.
