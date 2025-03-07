import validators
from flask import Flask, render_template, request, redirect, url_for, flash, \
    abort
from page_analyzer.db import get_db_connection, get_urls, get_url_by_id, \
    get_url_by_name, add_url
from page_analyzer.config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
def index():
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
    return render_template("url.html", url=url)


if __name__ == '__main__':
    app.run(debug=True)