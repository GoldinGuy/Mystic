from . import cur, mc, youtube, YOUTUBE_CHANNELS
import requests
import lxml.html
import functools
import itertools


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
    mc_ongoing = mc.get("SCRYFALL_LATEST_PROMO_ONGOING")
    if mc_url is not None and mc_ongoing is not None:
        return {"url": mc_url, "ongoing": mc_ongoing}

    content = requests.get("https://scryfall.com/").text
    content = lxml.html.fromstring(content)

    nodes = content.xpath('//div[@class="homepage-examples"]/ul/li/a')
    target_node = None
    ongoing = None

    for node in nodes:
        text = str(node.text_content())
        if text.endswith("ongoing previews"):
            target_node = node
            ongoing = True
            break
        if text.endswith("full preview"):
            target_node = node
            ongoing = False
            break

    url = "https://scryfall.com" + target_node.attrib["href"]

    mc.add("SCRYFALL_LATEST_PROMO", url, time=60 * 60 * 24)
    mc.add("SCRYFALL_LATEST_PROMO_ONGOING", ongoing, time=60 * 60 * 24)

    return {"url": url, "ongoing": ongoing}


# TODO: can these globals be removed?
global_youtube_response = {}
global_counter = 0


def cb(c, request_id, response, exception):
    if global_youtube_response.get(c) is None:
        global_youtube_response[c] = []
    global_youtube_response[c].append(response)


def fetch_youtube_uploads(page_token=None):
    global global_counter

    this_counter = global_counter
    global_counter += 1

    batch = youtube.new_batch_http_request()
    for channel in YOUTUBE_CHANNELS:
        batch.add(
            youtube.playlistItems().list(
                part="snippet", playlistId=channel, maxResults=2, pageToken=page_token
            ),
            callback=functools.partial(cb, this_counter),
        )
    batch.execute()

    return {
        "kind": "youtube",
        "nextPageToken": global_youtube_response[this_counter][0]["nextPageToken"],
        "items": list(
            itertools.chain.from_iterable(
                map(lambda x: x["items"], global_youtube_response[this_counter])
            )
        ),
    }
