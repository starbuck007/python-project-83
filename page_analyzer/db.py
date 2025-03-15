import psycopg
from psycopg.rows import dict_row
from page_analyzer.config import DATABASE_URL


def get_db_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_urls():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT 
                urls.id, 
                urls.name, 
                urls.created_at,
                checks.created_at AS last_check_created_at,
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
    conn.close()
    return urls


def get_url_by_id(id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        url = cur.fetchone()
    conn.close()
    return url


def get_url_by_name(name):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (name,))
        url = cur.fetchone()
    conn.close()
    return url


def add_url(url):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, NOW()) RETURNING id',
                   (url,))
        id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return id


def add_check(url_id, status_code, h1, title, description):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO url_checks '
            '(url_id, status_code, h1, title, description, created_at) '
            'VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING id',
            (url_id, status_code, h1, title, description)
        )
        id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return id


def get_checks_for_url(url_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            'SELECT * FROM url_checks '
            'WHERE url_id = %s '
            'ORDER BY created_at DESC',
            (url_id,)
        )
        checks = cur.fetchall()
    conn.close()
    return checks
