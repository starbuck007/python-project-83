import psycopg
from psycopg.rows import dict_row
from page_analyzer.config import DATABASE_URL


def get_db_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_urls():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM urls ORDER BY id DESC')
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
