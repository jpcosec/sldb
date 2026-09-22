"""Optional bearer-token auth for the HTTP surface of `sldb serve`.

Off by default: with no token configured the server behaves exactly as before.
When a token is configured (`--token <TOKEN>` or `SLDB_SERVE_TOKEN`, the flag
winning) every GET/POST must present `Authorization: Bearer <token>`, compared
with `hmac.compare_digest`; otherwise the server answers 401 with
`{"ok": false, "error": "unauthorized"}` and never touches the store.

The OPTIONS preflight is deliberately exempt: browsers do not attach
credentials to a preflight, so requiring the token there would break every CORS
client while protecting nothing (OPTIONS only reports the allowed methods).
"""

from __future__ import annotations

import hmac
import os
from http.server import BaseHTTPRequestHandler

ENV_VAR = "SLDB_SERVE_TOKEN"
HEADER = "Authorization"
SCHEME = "Bearer "


def resolve_token(flag_value: str | None) -> str | None:
    """The CLI flag wins over the env var; empty or missing means no auth."""
    token = flag_value if flag_value is not None else os.environ.get(ENV_VAR)
    return token or None


def is_authorized(handler: BaseHTTPRequestHandler, token: str | None) -> bool:
    """True when no token is configured, or the request presents it."""
    if not token:
        return True
    return hmac.compare_digest(_presented(handler).encode("utf-8"), token.encode("utf-8"))


def _presented(handler: BaseHTTPRequestHandler) -> str:
    header = handler.headers.get(HEADER, "")
    return header[len(SCHEME):] if header.startswith(SCHEME) else ""
