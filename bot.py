import csv
import random
import re
from os import environ
from collections import deque
from mastodon import Mastodon

POST_LENGTH = 500

def load_sayings():
    sayings = []
    with open("book_of_bokonon.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            sayings.append(row[0].strip())
    return sayings

def get_saying():
    return random.choice(load_sayings())

def split_to_posts(text):
    words = deque(*re.split("\b", text))
    posts = [[]]
    while len(words) > 0:
        word = words.popleft()
        if len(posts[-1]) + len(word) >= POST_LENGTH:
            posts.append([])
        posts[-1].append(word)
    return ["".join(post) for post in posts]

def post():
    mastodon = Mastodon(
        access_token = environ["ACCESS_TOKEN"],
        api_base_url = environ["API_BASE_URL"]
    )
    saying  = get_saying()
    posts = split_to_posts(saying)
    for post in posts:
        mastodon.status_post(post)

if __name__ == "__main__":
    post()

