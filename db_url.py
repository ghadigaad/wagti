from __future__ import annotations

"""
Postgres URL helpers for cloud hosting (e.g. Render) -> Supabase.

Render is often IPv4-only; Supabase direct `db.*.supabase.co` can resolve to IPv6
first, causing "Network is unreachable". Libpq can connect over IPv4 by setting
`hostaddr` to an A record while keeping the original host for TLS SNI.
Set WAGTI_DB_NO_HOSTADDR=1 to skip this (e.g. IPv6-only networks).
"""
import os
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


def ipv4_preferred_connect_args_for_url(normalized_url: str) -> dict:
    """
    If the hostname has an IPv4 (A) record, return connect_args to use that
    address. Empty dict if disabled, not Postgres, or no A record (use
    Supabase Session pooler from an IPv4-only host in that case).
    """
    if os.environ.get("WAGTI_DB_NO_HOSTADDR") == "1":
        return {}
    if not normalized_url or normalized_url.startswith("sqlite"):
        return {}
    p = urlparse(normalized_url)
    if not p.hostname:
        return {}
    h = ipv4_hostaddr_for_hostname(p.hostname, p.port or 5432)
    return {"hostaddr": h} if h else {}
