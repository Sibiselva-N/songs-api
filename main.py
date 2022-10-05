import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

base_url = "https://masstamilan.dev/"
tamil_url = "tamil-songs"
hindi_url = "hindi-songs"
malayalam_url = "malayalam-songs"
telugu_url = "telugu-songs"


def movie_page(url):
    scrap_list = []
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scrap = soup.find_all('div', {'class': 'a-i'})
    next_page = soup.find_all('span', {'class': 'page next'})[0].find_next('a').get('href')
    for i in scrap:
        scrap_list.append({"title": i.find_next('a').get('title').replace(" Songs Download", ""),
                           "link": i.find_next('a').get('href'),
                           "image": i.find_next('img').get('src')})
    return {"next": next_page, "list": scrap_list}


# pass movie page url
def song_from_movie(url):
    scrap_list = []
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scrap = soup.find_all('a', {'class': 'dlink anim umami--click--dl320'})
    for i in scrap:
        scrap_list.append(
            {"name": i.get('title').replace("Download", "").replace("320kbps", ""), 'link': base_url + i.get('href')})
    return scrap_list


def song_trending_movie(url):
    scrap_main = []
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scrap = soup.find_all('section', {'class': 'wid ctr left'})
    for i in scrap:
        scrap_list = []
        for j in i.find_all('li'):
            scrap_list.append({"name": j.getText().replace("\n", ""), 'link': j.find_next('a').get('href')})
        scrap_main.append({"title": i.find_next("h4", {'class': 'wtitle cen'}).getText(), "list": scrap_list})
    return scrap_main


@app.route('/')
def all_lan():
    return {"language": [{'language': "Tamil", "url": tamil_url}, {'language': "Hindi", "url": hindi_url},
                         {'language': "Malayalam", "url": malayalam_url}, {'language': "Telugu", "url": telugu_url}]}


@app.route('/lan')
def lin():
    return movie_page(request.args.get('lan'))


@app.route('/mov')
def mov():
    return song_from_movie(request.args.get('mov'))


@app.route('/trend')
def trend():
    return song_trending_movie(request.args.get('lan'))[0]


@app.route('/music')
def music():
    return song_trending_movie(request.args.get('lan'))[1]


if __name__ == '__main__':
    app.run()
