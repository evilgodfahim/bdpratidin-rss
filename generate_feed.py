import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.bd-pratidin.com/open-air-theater"

resp = requests.get(URL)
resp.encoding = "utf-8"  # ensure Bangla text is handled properly
soup = BeautifulSoup(resp.text, "html.parser")

fg = FeedGenerator()
fg.title("BD Pratidin – Open Air Theater (Editorials Only)")
fg.link(href=URL, rel="alternate")
fg.description("Extracted editorials from bd-pratidin Open Air Theater")
fg.language("bn")

# Find the main editorial section
main_section = soup.find("div", class_="row categoryArea")

if main_section:
    # Main top article
    card_body = main_section.find("div", class_="card-body")
    if card_body:
        title = card_body.find("h1").get_text(strip=True)
        desc = card_body.find("p").get_text(strip=True)
        link = main_section.find("a", class_="stretched-link")["href"]
        img = main_section.find("img")["src"]

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description(f"<img src='{img}'><br>{desc}")
        fe.guid(link)

    # More articles
    more_items = main_section.find_all("div", class_="col-6")
    for item in more_items:
        title = item.find("h5").get_text(strip=True)
        link = item.find("a", class_="stretched-link")["href"]
        img = item.find("img")["src"]

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description(f"<img src='{img}'>")
        fe.guid(link)

# Save as RSS
fg.rss_file("feed.xml")
