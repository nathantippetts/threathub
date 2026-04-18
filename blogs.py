import requests
from bs4 import BeautifulSoup


def krebs():
    # Grabs the most recent post and returns a dictionary of the different components
    url = "https://krebsonsecurity.com"
    r1 = requests.get(url)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, features="html.parser")
    coverpage_news = soup1.find("h2", class_="entry-title")
    headline = coverpage_news.get_text()
    coverpage_desc = soup1.find("p")
    description = coverpage_desc.get_text()
    post_url = coverpage_news.findChild("a")["href"]
    author = "KrebsOnSecurity"
    date = soup1.find("span", class_="date updated").get_text()
    print(post_url)
    blog = {"headline": headline.strip(), "description": description, "url": url, "post_url": post_url, "author": author, "date": date}
    return blog


def hackernews():
    # Grabs the first four headlines, descriptions, urls, and dates then returns a list of dictionaries containing each post
    url = "https://thehackernews.com"
    r1 = requests.get(url)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, features="html.parser")
    coverpage_news = soup1.findAll("h2", class_="home-title")
    headlines = []
    for headline in coverpage_news[0:4]:
        headlines.append(headline.get_text())
    coverpage_desc = soup1.findAll("div", class_="home-desc")
    descriptions = []
    for desc in coverpage_desc[0:4]:
        descriptions.append(desc.get_text())
    post_urls = []
    links = soup1.findAll("a", class_="story-link")
    for item in links[0:4]:
        post_urls.append(item.get("href"))
    author = "The Hacker News"
    date = soup1.findAll("span", class_="h-datetime")
    dates = []
    for item in date[0:4]:
        dates.append(item.get_text())
    posts = []
    for i in range(0,4):
        posts.append({"headline": headlines[i], "description": descriptions[i], "url": url, "post_url": post_urls[i], "author": author, "date": dates[i]})
    return posts

