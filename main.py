from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import json

term = input("Search term: ")
URL = f"https://www.amazon.com/s?k={term}"
session = HTMLSession()

response = session.get(URL)
response.html.render()

webhook = "" # Add discord webhook link here

soup = BeautifulSoup(response.html.html, "lxml")

results = soup.find_all(class_="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True)

price = int(input("Max Price: "))
max_price = price
for result in results:
    link = f"amazon.com{result['href']}"
    price = float(result.find(class_="a-offscreen").get_text().split("$")[-1].replace(",", ""))

    if price < max_price:
        data = {"content": f'Price: {price} \nLink: {link}'}
        response = requests.post(webhook, json=data)
        print(response.status_code)
session.close()
