import sys
sys.path.append("/usr/lib/python3/dist-packages")
import requests
import bs4

url = "https://habr.com/ru/all"

HEADER = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'fAAn']


def get_article_date(article_):
    return article_.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title'].split(',')[0]


def is_keyword_in(seq):
    seq = str(seq).lower()
    for w in KEYWORDS:
        w = str(w).lower()
        if seq.find(w) != -1:
            return True
    return False


def search_in_hubs(res_list, article_):
    hubs = article_.find_all(class_='tm-article-snippet__hubs-item')
    hubs = set(hub.text.strip() for hub in hubs)
    for hub in hubs:
        if hub in KEYWORDS or is_keyword_in(hub):
            published_date = get_article_date(article_)
            href = url + article_.find(class_='tm-article-snippet__title-link').attrs['href']

            title = article_.find('h2').find('span').text
            result = f'{published_date} - {title} - {href}'
            res_list.add(result)
    return res_list


def search_in_titles(res_list, article_):
    article_title = article_.find(class_='tm-article-snippet__title-link').find('span').text
    title_list = article_title.split()

    for title in title_list:
        if title in KEYWORDS or is_keyword_in(title):
            published_date = get_article_date(article_)

            href = url + article_.find(class_='tm-article-snippet__title-link').attrs['href']

            result = f'{published_date} - {article_title} - {href}'
            res_list.add(result)
    return res_list


def search_in_preview(res_list, article_):
    article_preview = article_.find_all(class_='article-formatted-body')
    ap = ''
    for ap_words in article_preview:
        ap = ap + ap_words.text.strip()
    words = set(ap.split())

    for elem in words:
        if elem in KEYWORDS or is_keyword_in(elem):
            published_date = get_article_date(article_)

            href = url + article_.find(class_='tm-article-snippet__title-link').attrs['href']

            article_title = article_.find(class_='tm-article-snippet__title-link').find('span').text
            result = f'{published_date} - {article_title} - {href}'
            res_list.add(result)
    return res_list


def show_list(list_):
    for elem in list_:
        print(elem)


if __name__ == '__main__':
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    articles = soup.find_all('article')

    result_list = set()

    for article in articles:
        # поиск в хабах
        result_list = search_in_hubs(result_list, article)
        # поиск в заголовках
        result_list = search_in_titles(result_list, article)
        # поиск в preview
        result_list = search_in_preview(result_list, article)

    show_list(result_list)
