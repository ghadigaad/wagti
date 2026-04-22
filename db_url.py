"""
Normalize Postgres URLs for cloud hosting (e.g. Render) -> Supabase.

Render free tier often cannot reach Supabase over IPv6 ("Network is unreachable").
Resolving the DB hostname to IPv4 and setting libpq "hostaddr" forces IPv4.
"""
import socket
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


def normalize_database_url(url: str) -> str:
    if not url or url.startswith("sqlite"):
        return url

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    if not url.startswith("postgresql://"):
        return url

    p = urlparse(url)
    if not p.hostname:
        return url

    # Merge query
    q = dict(parse_qsl(p.query, keep_blank_values=True))
    if "sslmode" not in q:
        q["sslmode"] = "require"

    if "hostaddr" not in q:
        try:
            prt = p.port or 5432
            infos = socket.getaddrinfo(
                p.hostname, prt, socket.AF_INET, socket.SOCK_STREAM
            )
            if infos:
                q["hostaddr"] = infos[0][4][0]
        except OSError:
            pass

    new_q = urlencode(list(q.items()))
    return urlunparse(p._replace(query=new_q))
