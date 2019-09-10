from . import cur, mc
import requests
import lxml.html


def retrieve_articles_from(site, count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url, description "
        "FROM articles WHERE LOWER(site_name) = %s ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (site.lower(), count, page * count),
    )

    return fetch_requested_articles()


def retrieve_articles_from_multiple(sites, count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url, description "
        "FROM articles WHERE LOWER(site_name) in %s ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (sites, count, page * count),
    )

    return fetch_requested_articles()


def retrieve_articles(count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url, description "
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
                "description": article[8],
            }
        )
    return output


def fetch_scryfall_latest_promo():
    mc_url = mc.get("SCRYFALL_LATEST_PROMO")
    if mc_url is not None:
        return mc_url

    content = requests.get("https://scryfall.com/").text
    content = lxml.html.fromstring(content)

    nodes = content.xpath('//div[@class="homepage-examples"]/ul/li/a')
    target_node = None

    for node in nodes:
        text = str(node.text_content())
        if text.endswith("ongoing previews") or text.endswith("full preview"):
            target_node = node
            break

    url = "https://scryfall.com" + target_node.attrib["href"]

    mc.add("SCRYFALL_LATEST_PROMO", url, time=60 * 60 * 24)

    return url
