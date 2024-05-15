import aiohttp
import asyncio
from bs4 import BeautifulSoup
import connection

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_anime_data(url):
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_url(session, url)
        soup = BeautifulSoup(response_text, 'html.parser')
        latest_anime = soup.find_all("div", class_="anime-tile lozad")
        for anime in latest_anime:
            name = anime.find("h2", class_="anime-tile-title").text
            rating = anime.find("strong", class_="anime-tile-rating-score").text
            description = anime.find("p", class_="anime-tile-description").text
            genres = anime.find_all("a", class_="anime-tile-genre")
            episodes = anime.find_all("div", class_="anime-tile-bottom-item")
            genre_texts = [genre.text for genre in genres]
            date = anime.find("time", class_= "anime-tile-bottom-item anime-tile-datetime").text
            duration = anime.find_all("div", class_ = "anime-tile-bottom-item anime-tile-bottom-item-length")
            new_url = "https://animeschedule.net" + anime.find("a")["href"]
            anime_response_text = await fetch_url(session, new_url)
            anime_soup = BeautifulSoup(anime_response_text, 'html.parser')
            anime_url = anime_soup.find("div", id = "page-content-wrapper")
            thumbnail = anime_url.find("img", id = "anime-poster")["src"]
            show_type = anime_url.find_all("a", class_ = "information-link")
            status = anime_url.find_all("div", class_ = "information-content-wrapper")
            alternative_name = anime_url.find("div", class_ = "alternative-name")
            anime_website_element = anime_url.find("a", class_="anime-link official-link")
            anime_website = anime_website_element["href"] if anime_website_element is not None else " "
            release_time_sub = anime_url.find("time", id = "release-time-subs")
            anime_link_container = anime_url.find("div", class_ = "links-container")
            streaming_sites = [link["href"] for link in anime_link_container.find_all("a", class_="anime-link")]


            print()
            print("Name:", name)
            print("Alt_name:", alternative_name.text if alternative_name is not None else " ")
            print("Description:", description)
            print("Thumbnail:", thumbnail)
            print("Genres:", genre_texts)
            print("Rating:", rating)
            print("Episodes:", episodes[1].text)
            print("Duration:", duration[1].text)
            print("Launch:", date.strip())
            print("Type:", show_type[0].text)
            print("Season:", show_type[1].text)
            print("Source:", show_type[2].text)
            print("Status:", status[3].find("div").text)
            print("Release_time_sub:", release_time_sub.text if release_time_sub is not None else " ")
            print("Streaming_sites:", streaming_sites)
            print("Official_website:", anime_website)

async def main():
    url = "https://animeschedule.net/seasons/winter-2024"
    await scrape_anime_data(url)

asyncio.run(main())
