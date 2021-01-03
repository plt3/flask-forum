import random

import requests

from asyncGeneratePosts import ContentMaker
from secretKey import rapidApiKey


def fillPosts(numPosts):
    """Insert specified amount of random posts into the database

    :numPosts: amount of posts to create
    :returns: None

    """
    postGenerator = ContentMaker(rapidApiKey)
    posts = postGenerator.createPosts(numPosts)

    apiEndpoint = "http://localhost:5000/api/createPost"

    for post in posts:
        postRes = requests.post(apiEndpoint, json=post)
        postRes.raise_for_status()


def getPostIds():
    """Return list of all post IDs in website

    :returns: list of IDs of all posts in the website

    """
    endpoint = 'http://localhost:5000/api/posts'
    params = {'page': 1, 'perPage': 20}
    response = requests.get(endpoint, params=params)
    postIds = [post['id'] for post in response.json()['response']]

    while response.json()['hasNext']:
        params['page'] += 1
        response = requests.get(endpoint, params=params)
        postIds.extend([post['id'] for post in response.json()['response']])

    return postIds


def getPostComments(postId, addZero=True):
    """Return list of all comment IDs on specified post

    :postId: ID of post to get comments from
    :addZero: whether to add 0 as one of the IDs in the list
    :returns: list of integers of all comment IDs on the post

    """
    endpoint = "http://localhost:5000/api/comments"
    params = {"post": postId, "page": 1, "perPage": 20}

    response = requests.get(endpoint, params=params)
    commentIds = [comment["id"] for comment in response.json()["response"]]

    while response.json()["hasNext"]:
        params["page"] += 1
        response = requests.get(endpoint, params=params)
        commentIds.extend([comment["id"] for comment in response.json()["response"]])

    if addZero:
        commentIds.append(0)

    return commentIds


def commentOnPost(postNum, numComments):
    """Post specified amount of comments on specified post

    :postNum: ID of forum post to post comments on
    :numComments: amount of comments to create
    :returns: None

    """
    commentGenerator = ContentMaker(rapidApiKey)
    comments = commentGenerator.createComments(numComments)

    commentIds = getPostComments(postNum)

    apiEndpoint = f"http://localhost:5000/api/{postNum}/addComment"

    for comment in comments:
        commentObj = {
            "name": comment["name"],
            "content": comment["content"],
            "replyTo": random.choice(commentIds),
        }
        response = requests.post(apiEndpoint, json=commentObj)
        response.raise_for_status()

        commentIds.append(response.json()["id"])


def fillComments(minPerPost, maxPerPost):
    """Generate random amount of comments on each post in the database

    :minPerPost: minimum amount of comments to have on each post
    :maxPerPost: maximum amount of comments to have on each post
    :returns: None

    """
    # NOTE: this generates A LOT of comments (up to maxPerPost * number of posts), and
    # is synchronous so that the website can handle it. It may take a while to run

    allPostIds = getPostIds()

    for id in allPostIds:
        commentsToMake = random.randint(minPerPost, maxPerPost)
        commentOnPost(id, commentsToMake)


if __name__ == "__main__":
    fillComments(0, 20)
