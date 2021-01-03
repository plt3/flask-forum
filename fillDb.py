import requests

from asyncGeneratePosts import ContentMaker
from secretKey import rapidApiKey


def fillPosts(numPosts):
    """Insert specified amount of random posts into the database

    :numPosts: amount of posts to create
    :returns: None

    """
    contentGenerator = ContentMaker(rapidApiKey)
    posts = contentGenerator.createPosts(numPosts)

    apiEndpoint = "http://localhost:5000/api/createPost"

    for post in posts:
        postRes = requests.post(apiEndpoint, json=post)
        postRes.raise_for_status()


def commentOnPost(postNum, numComments):
    """Post specified amount of comments on specified post

    :postNum: ID of forum post to post comments on
    :numComments: amount of comments to create
    :returns: None

    """
    pass


if __name__ == "__main__":
    fillPosts(3)
