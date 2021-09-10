# flask api to scrape data from the web
from flask import Flask, request, jsonify

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


# scrape data from the web
# Tunisienumerique
@app.route('/scrape')
def scrape():
    # beautiful soup scraping
    tech_url = 'https://www.tunisienumerique.com/actualite-tunisie/tech-net/'
    eco_url = 'https://www.tunisienumerique.com/actualite-tunisie/economie/'
    tun_url = 'https://www.tunisienumerique.com/actualite-tunisie/tunisie/'
    world_url = 'https://www.tunisienumerique.com/actualite-tunisie/monde/'
    sport_url = 'https://sport.tunisienumerique.com/actus/'
    html = requests.get(sport_url)
    soup = BeautifulSoup(html.text, 'lxml')

    # print(soup.prettify())

    # get the title
    postes = soup.find(class_='archive-col-list')
    titles = postes.find_all('h2')
    descriptions = postes.find_all('p')
    images = postes.find_all('img')[0::2]
    links = postes.find_all('a')

    # for post in postes:
    #     print(['src'])
    # images.append(post.find('img').get('src'))

    data = []
    for title, description, image, link in zip(titles, descriptions, images,
                                               links):
        print(image)
        data.append({
            'title': title.text,
            'description': description.text,
            'image': image.get('src'),
            'link': link.get('href')
        })

    return jsonify(data)


@app.route('/details', methods=['POST'])
def details():
    url = request.get_json()['url']

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    details = soup.find(id='content-main').find_all('p')

    texts = []
    for detail in details[1:(len(details) - 1)]:
        texts.append(detail.text)

    return jsonify(texts)


# Babnet
@app.route('/scrap/babnet', methods=['POST'])
def scrapbabnet():
    url = request.get_json()['url']
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    category = soup.find(class_='block-title').find('span').text

    posts = soup.find(class_='block category-listing')
    titles = posts.find_all('a')[0::2]
    images = posts.find_all('img')
    dates = posts.find_all('span')[1:]
    descriptions = posts.find_all('p')

    data = []

    for title, image, date, description in zip(titles, images, dates,
                                               descriptions):
        data.append({
            'title': title.text,
            'image': image.get('src'),
            'date': date.text,
            'description': description.text,
            'link': 'https://www.babnet.net/' + title.get('href')
        })

    # print(titles)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
