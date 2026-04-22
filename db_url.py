from __future__ import annotations

"""
Postgres URL helpers for cloud hosting (e.g. Render) -> Supabase.

Render may fail with IPv6 ("Network is unreachable"). Passing hostaddr via
SQLAlchemy connect_args (not the URI query string) matches libpq/psycopg2 best.
"""
import socket
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


def normalize_database_url(url: str) -> str:
    """postgres:// -> postgresql://, add sslmode=require. No hostaddr in URL."""
    if not url or url.startswith("sqlite"):
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if not url.startswith("postgresql://"):
        return url
    p = urlparse(url)
    if not p.hostname:
        return url
    q = dict(parse_qsl(p.query, keep_blank_values=True))
    if "sslmode" not in q:
        q["sslmode"] = "require"
    new_q = urlencode(list(q.items()))
    return urlunparse(p._replace(query=new_q))


def ipv4_hostaddr_for_hostname(hostname: str, port: int = 5432):
    """Return first IPv4 for hostname, or None if not available."""
    if not hostname:
        return None
    try:
        infos = socket.getaddrinfo(
            hostname, port, socket.AF_INET, socket.SOCK_STREAM
        )
        if infos:
            return infos[0][4][0]
    except OSError:
        pass
    return None
