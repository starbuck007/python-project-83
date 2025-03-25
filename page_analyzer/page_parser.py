"""Module for parse HTML-content"""
from bs4 import BeautifulSoup


def parse_page(html_content):
    """Parse HTML content and extract SEO data"""
    soup = BeautifulSoup(html_content, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = h1_tag.text.strip() if h1_tag else ''

    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if (description_tag and
                       'content' in description_tag.attrs) else ''

    return {
        'h1': h1,
        'title': title,
        'description': description
    }
