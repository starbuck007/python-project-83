"""Main app logic"""
import validators
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, \
    abort
from bs4 import BeautifulSoup
from page_analyzer.db import get_urls, get_url_by_id, \
    get_url_by_name, add_url, add_check, get_checks_for_url
from page_analyzer.config import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
def index():
    """GET and POST requests for the main page, validating URLs."""
    if request.method == "POST":
        url = request.form["url"]
        if not validators.url(url):
            flash("Некорректный URL", "danger")
            return render_template("index.html", url=url)
        if len(url) > 255:
            flash("URL превышает 255 символов", "danger")
            return render_template("index.html", url=url)

        # Проверка на существование URL в базе
        existing_url = get_url_by_name(url)
        if existing_url:
            flash("Страница уже существует", "info")
            return redirect(url_for("url_show", id=existing_url['id']))

        try:
            url_id = add_url(url)
            flash("Страница успешно добавлена", "success")
            return redirect(url_for("url_show", id=url_id))
        except Exception:
            flash("Произошла ошибка при добавлении страницы", "danger")
            return render_template("index.html", url=url)

    return render_template("index.html")


@app.route('/urls')
def urls_index():
    urls = get_urls()
    return render_template("urls.html", urls=urls)


@app.route('/urls/<int:id>')
def url_show(id):
    url = get_url_by_id(id)
    if not url:
        abort(404)
    checks = get_checks_for_url(id)
    return render_template("url.html", url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_check(id):
    url = get_url_by_id(id)
    if not url:
        abort(404)

    try:
        response = requests.get(url['name'], timeout=5)
        status_code = response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else ''

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ''

        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag[
            'content'] if description_tag and 'content' in description_tag.attrs else ''

        add_check(id, status_code, h1, title, description)

        flash('Страница успешно проверена', 'success')
    except requests.RequestException:
        flash('Произошла ошибка при проверке страницы', 'danger')
    except Exception as e:
        flash(f'Неизвестная ошибка: {str(e)}', 'danger')

    return redirect(url_for('url_show', id=id))


if __name__ == '__main__':
    app.run(debug=True)
