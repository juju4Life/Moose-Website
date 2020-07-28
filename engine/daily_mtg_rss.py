from engine.models import DailyMtgNews
import requests
import xmltodict


def daily_mtg_update():
    current_articles = DailyMtgNews.objects.all()
    r = requests.get(url="https://magic.wizards.com/en/rss/rss.xml?tags=Daily%20MTG&lang=en")
    xml = xmltodict.parse(r.text)
    articles = xml.get("rss").get("channel").get("item")[0:5]
    new_articles = list()

    for article in articles:
        title = article["title"]
        link = article["link"]
        description = article["description"]
        published = article["pubDateString"]
        if "Juli" in published:
            published = published.replace("Juli", "July")
        creator = article["dc:creator"]

        if not current_articles.filter(title=title).filter(published_date=published).exists():
            new_articles.append(
                DailyMtgNews(
                    title=title,
                    link=link,
                    description=description,
                    published_date=published,
                    creator=creator,
                )
            )

    DailyMtgNews.objects.bulk_create(new_articles)


daily_mtg_update()


