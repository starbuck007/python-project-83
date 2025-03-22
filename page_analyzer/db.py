"""Database module for app."""
import psycopg2
import psycopg2.extras
from page_analyzer.config import DATABASE_URL


def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(DATABASE_URL,
                            cursor_factory=psycopg2.extras.DictCursor)


def get_urls():
    """Get all URLs with information about their last check."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    urls.id,
                    urls.name,
                    TO_CHAR(urls.created_at, 'YYYY-MM-DD') 
                        AS created_at,
                    TO_CHAR(checks.created_at, 'YYYY-MM-DD')
                        AS last_check_created_at,
                    checks.status_code AS last_check_status_code
                FROM urls
                LEFT JOIN (
                    SELECT DISTINCT ON (url_id) url_id, created_at, status_code
                    FROM url_checks
                    ORDER BY url_id, created_at DESC
                ) checks ON urls.id = checks.url_id
                ORDER BY urls.id DESC
            ''')
            urls = cur.fetchall()
    return urls


def get_url_by_id(url_id):
    """Get URL by ID."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    id,
                    name,
                    TO_CHAR(created_at, 'YYYY-MM-DD') AS created_at
                FROM urls WHERE id = %s
                ''', (url_id,))
            url = cur.fetchone()
    return url if url is None else dict(url)


def get_url_by_name(name):
    """Get URL by URL-address."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT * FROM urls WHERE name = %s''', (name,))
            url = cur.fetchone()
    return url if url is None else dict(url)


def add_url(url):
    """Add new URL to the database."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO urls (name, created_at) 
                VALUES (%s, NOW()) RETURNING id
                ''', (url,))
            url_id = cur.fetchone()[0]
            conn.commit()
    return url_id


def add_check(url_id, status_code, h1, title, description):
    """Add new URL check to the database."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO url_checks 
                    (url_id, status_code, h1, title, description, created_at) 
                    VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING id
                    ''', (url_id, status_code, h1, title, description))
            check_id = cur.fetchone()[0]
            conn.commit()
    return check_id


def get_checks_for_url(url_id):
    """Get all checks for URL."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT
                    id, 
                    url_id, 
                    status_code, 
                    h1,title,
                    description,
                    TO_CHAR(created_at, 'YYYY-MM-DD') AS created_at
                FROM url_checks 
                WHERE url_id = %s 
                ORDER BY created_at DESC
                ''', (url_id,))
            checks = cur.fetchall()
    return [dict(check) for check in checks]
