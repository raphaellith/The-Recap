import requests
from bs4 import BeautifulSoup


def get_titles_from_the_guardian(get_link=True):
    url = "https://www.theguardian.com/technology/all"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result = []

    for a_tag in soup.find_all("a"):
        data_link_name = a_tag.get('data-link-name')
        if data_link_name is not None:
            if data_link_name.startswith("news") or data_link_name.startswith("feature"):
                title = a_tag.get('aria-label')
                if get_link:
                    link = "https://www.theguardian.com" + a_tag.get('href')
                    result.append((title, link))
                else:
                    result.append(title)

    return result


def get_titles_from_bbc(get_link=True):
    url = "https://www.bbc.co.uk/news/technology"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result = []

    for a_tag in soup.find_all("a"):
        if a_tag.get('href') is not None:
            link = a_tag.get('href')
            if link.startswith('/news'):
                children = a_tag.find_all("span")
                for child in children:
                    if child.get('aria-hidden') == 'false':
                        title = child.text
                        if get_link:
                            link = 'https://www.bbc.co.uk' + link
                            result.append((title, link))
                        else:
                            result.append(title)

    return result


