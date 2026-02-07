## 2026-01-31 - Hardcoded Secret Discrepancy
**Vulnerability:** Hardcoded `SECRET_KEY` in `apps/api/app/core/auth.py` ("CHANGE_ME_LATER") despite `DEPLOYMENT.md` instructions to use `JWT_SECRET_KEY` env var.
**Learning:** Documentation and implementation were out of sync. `DEPLOYMENT.md` described a secure setup that the code did not support.
**Prevention:** Always verify that documentation instructions are reflected in the actual codebase configuration logic.

## 2026-02-07 - Insecure Library Compatibility
**Vulnerability:** Incompatible `httpx` version (0.28.1) caused `TestClient` tests to fail when used with `starlette==0.27.0` (via `fastapi==0.104.1`).
**Learning:** Backend dependencies must be carefully pinned to compatible versions. Newer versions of `httpx` break `TestClient` constructor signature for older `starlette`.
**Prevention:** Pin `httpx<0.28.0` (e.g., `0.27.2`) in `requirements.txt` when using `fastapi<=0.104.1` / `starlette<=0.27.0`.
