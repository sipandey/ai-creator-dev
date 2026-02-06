## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-06 - Untyped Dict Payload Injection
**Vulnerability:** `generate_reel_script` in `script.py` used `payload: dict` instead of a Pydantic model, allowing execution with missing or invalid fields and bypassing validation.
**Learning:** Using raw `dict` for payloads bypasses FastAPI's automatic validation and documentation generation, leading to fragile code and potential errors.
**Prevention:** Strictly enforce Pydantic models for all request bodies; review new endpoints for loose typing.
