"""CLI entry point of `sldb serve`: bind the handler and serve forever."""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from typing import Any

from sldb.cli.serve.auth import resolve_token
from sldb.cli.serve.http_server import build_handler


class ServeCLI:
    def run(self, args: Any) -> int:
        token = resolve_token(getattr(args, "token", None))
        handler = build_handler(args.store, args.pythonpath, getattr(args, "cors", False), token)
        httpd = ThreadingHTTPServer((args.host, args.port), handler)
        print(_banner(args, token))
        _serve_forever(httpd)
        return 0


def _banner(args: Any, token: str | None) -> str:
    auth = "on (bearer token required)" if token else "off"
    return f"sldb serve on http://{args.host}:{args.port} (store={args.store or 'auto'}, auth={auth})"


def _serve_forever(httpd: ThreadingHTTPServer) -> None:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
