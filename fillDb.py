import requests

from asyncGeneratePosts import PostMaker
from secretKey import rapidApiKey

POSTS_TO_MAKE = 100
postGenerator = PostMaker(rapidApiKey)
posts = postGenerator.createPosts(POSTS_TO_MAKE)

for post in posts:
    postRes = requests.post("http://localhost:5000/api/createPost", json=post)
    postRes.raise_for_status()
    print(postRes.json()["author"])
