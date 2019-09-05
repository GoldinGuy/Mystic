from . import cur
import requests
import lxml.html


def retrieve_articles_from(site, count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url "
        "FROM articles WHERE LOWER(site_name) = %s ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (site.lower(), count, page * count),
    )

    return fetch_requested_articles()


def retrieve_articles_from_multiple(sites, count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url "
        "FROM articles WHERE LOWER(site_name) in %s ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (sites, count, page * count),
    )

    return fetch_requested_articles()


def retrieve_articles(count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url "
        "FROM articles ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (count, page * count),
    )
    return fetch_requested_articles()


def fetch_requested_articles():
    output = []
    for article in cur.fetchall():
        output.append(
            {
                "title": article[0],
                "url": article[1],
                "date": article[2],
                "image_url": article[3],
                "site_name": article[4],
                "site_url": article[5],
                "author_name": article[6],
                "author_url": article[7],
            }
        )
    return output


def fetch_scryfall_latest_promo():
    content = requests.get("https://scryfall.com/").text
    content = lxml.html.fromstring(content)

    return (
        "https://scryfall.com"
        + content.xpath('//div[@class="homepage-examples"]/ul/li/a')[0].attrib["href"]
    )
