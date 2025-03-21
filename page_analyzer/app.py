"""Main app logic"""
from urllib.parse import urlparse
import validators
import requests
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, \
    abort, get_flashed_messages
from bs4 import BeautifulSoup
from page_analyzer.db import get_urls, get_url_by_id, \
    get_url_by_name, add_url, add_check, get_checks_for_url
from page_analyzer.config import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
def index():
    """Processing requests on the main page."""
    if request.method == "POST":
        url = request.form["url"]
        if not validators.url(url):
            flash("Некорректный URL", "danger")
            return redirect(url_for("urls_index"))
        if len(url) > 255:
            flash("URL превышает 255 символов", "danger")
            return render_template("index.html", url=url)

        normalized_url = normalize_url(url)

        existing_url = get_url_by_name(normalized_url)
        if existing_url:
            flash("Страница уже существует", "info")
            return redirect(url_for("url_show", url_id=existing_url['id']))

        try:
            url_id = add_url(normalized_url)
            flash("Страница успешно добавлена", "success")
            return redirect(url_for("url_show", url_id=url_id))

        except (psycopg2.Error, ValueError):
            flash("Произошла ошибка при добавлении страницы", "danger")
            return render_template("index.html", url=url)

    return render_template("index.html")


@app.route('/urls')
def urls_index():
    """Display all URLs or form with incorrect link"""
    has_url_error = any('Некорректный URL' in msg[1] for msg
                        in get_flashed_messages(with_categories=True)
                        if msg[0] == 'danger')
    if has_url_error:
        return render_template("index.html"), 422

    urls = get_urls()
    return render_template("urls.html", urls=urls)


@app.route('/urls/<int:url_id>')
def url_show(url_id):
    """Display information about the URL and its checks."""
    url = get_url_by_id(url_id)
    if not url:
        abort(404)
    checks = get_checks_for_url(url_id)
    return render_template("url.html", url=url, checks=checks)


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_check(url_id):
    """Checks the URL and saves the results in a database."""
    url = get_url_by_id(url_id)
    if not url:
        abort(404)

    try:
        response = requests.get(url['name'], timeout=5)
        response.raise_for_status()

        status_code = response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else ''

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ''

        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag[
            'content'] if (description_tag and
                           'content' in description_tag.attrs) else ''

        add_check(url_id, status_code, h1, title, description)

        flash('Страница успешно проверена',
              'success')
    except requests.RequestException:
        flash('Произошла ошибка при проверке страницы',
              'danger')

    return redirect(url_for('url_show', url_id=url_id))


def normalize_url(url):
    """Get hostname from URL"""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


if __name__ == '__main__':
    app.run(debug=True)
