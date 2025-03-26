"""Main app logic"""
import requests
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, \
    abort
from page_analyzer.db import get_urls, get_url_by_id, \
    get_url_by_name, add_url, add_check, get_checks_for_url
from page_analyzer.page_parser import parse_page
from page_analyzer.url import validate_url, normalize_url
from page_analyzer.config import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=["GET"])
def index():
    """Show the Main page  with form"""
    return render_template("index.html")


@app.route('/urls', methods=["POST"])
def process_url():
    """Process and add URL"""
    url = request.form["url"]

    is_valid_url, error_message = validate_url(url)
    if not is_valid_url:
        flash(error_message, "danger")
        return render_template("index.html", url=url), 422

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
        return render_template("index.html", url=url), 422


@app.route('/urls')
def urls_index():
    """Display all URLs"""
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
        page_data = parse_page(response.text)

        add_check(url_id, status_code,
                  page_data['h1'],
                  page_data['title'],
                  page_data['description'])

        flash('Страница успешно проверена', 'success')
    except requests.RequestException:
        flash('Произошла ошибка при проверке страницы', 'danger')

    return redirect(url_for('url_show', url_id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
