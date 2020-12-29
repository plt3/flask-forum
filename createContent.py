import random

import requests

from secretKey import rapidApiKey

apis = {
    "wikihow": {
        "endpoint": "https://hargrimm-wikihow-v1.p.rapidapi.com/steps",
        "apiHost": "hargrimm-wikihow-v1.p.rapidapi.com",
        "queryParams": {
            "count": (1, 40),
        },
    },
    "skate": {
        "endpoint": "https://mashape-community-skate-ipsum.p.rapidapi.com/5000/0/JSON",
        "apiHost": "mashape-community-skate-ipsum.p.rapidapi.com",
        "queryParams": {
            "start": (0, 0),
            "paragraphs": (1, 3),
        },
    },
}


def makeNames(number, apiKey):
    """Create specified amount of random (German) names"""
    nameUrl = (
        "https://dawn2k-random-german-profiles-and-names-generator-v1.p.rapidapi.com/"
    )
    headers = {
        "x-rapidapi-key": apiKey,
        "x-rapidapi-host": (
            "dawn2k-random-german-profiles-and-names-generator-v1.p.rapidapi.com"
        ),
    }
    params = {"format": "json", "count": number}

    response = requests.get(nameUrl, headers=headers, params=params)
    response.raise_for_status()

    return [elem["firstname"] + " " + elem["lastname"] for elem in response.json()]


def makeTitles(number, apiKey):
    """Create specified amount of post titles"""
    quoteUrl = "https://fireflyquotes.p.rapidapi.com/quotes/random"
    headers = {
        "x-rapidapi-key": apiKey,
        "x-rapidapi-host": "fireflyquotes.p.rapidapi.com",
    }

    titles = []

    for _ in range(number):
        response = requests.get(quoteUrl, headers=headers)
        title = response.json()["body"]["Quote"]
        titles.append(title)

    return titles


# def responseToString(listOrDict):
#     """Return string of text from parsed JSON returned by skate ipsum or wikihow APIs"""
#     try:
#         return " ".join(listOrDict.values())
#     except AttributeError:
#         return "".join(listOrDict)


def makePostLengths(numPosts):
    posts = []
    lengths = {"wikihow": 0, "skate": 0}

    for _ in range(numPosts):
        postType = random.choice(["wikihow", "skate"])
        if postType == "wikihow":
            length = random.randint(1, 40)
            posts.append(("wikihow", length))
        else:
            length = random.randint(1, 3)
            posts.append(("skate", length))

        lengths[postType] += length

    return posts, lengths


def getSkateParagraphs(numParagraphs, apiKey):
    url = f"https://mashape-community-skate-ipsum.p.rapidapi.com/{numParagraphs}/0/JSON"
    headers = {
        "x-rapidapi-key": apiKey,
        "x-rapidapi-host": "mashape-community-skate-ipsum.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def getWikihowLines(numLines, apiKey):
    url = "https://hargrimm-wikihow-v1.p.rapidapi.com/steps"
    headers = {
        "x-rapidapi-key": apiKey,
        "x-rapidapi-host": "hargrimm-wikihow-v1.p.rapidapi.com",
    }
    wikiLines = []
    MAX = 1000
    requestAmounts = [MAX for _ in range(numLines // MAX)] + [numLines % MAX]
    for amount in requestAmounts:
        params = {"count": amount}
        response = requests.get(url, headers=headers, params=params)
        wikiLines.extend(list(response.json().values()))

    return wikiLines


# def makeAllPosts(numPosts, apiKey):
numPosts = 100
apiKey = rapidApiKey
authors = makeNames(numPosts, apiKey)
titles = makeTitles(numPosts, apiKey)
postDetails, totalsDict = makePostLengths(numPosts)
allSkateParagraphs = getSkateParagraphs(totalsDict["skate"], apiKey)
allWikihowLines = getWikihowLines(totalsDict["wikihow"], apiKey)

madePosts = []
wikiCounter = 0
skateCounter = 0

# turn all this and what's above into a function (and maybe make a class? idk)

for index, post in enumerate(postDetails):
    if post[0] == "wikihow":
        body = " ".join(allWikihowLines[wikiCounter : wikiCounter + post[1]])
        madePosts.append((authors[index], titles[index], body))
        wikiCounter += post[1]
    else:
        body = "".join(
            allSkateParagraphs[skateCounter : skateCounter + post[1]]
        ).strip()
        madePosts.append((authors[index], titles[index], body))
        skateCounter += post[1]


# for use to generate comments
# messageHost = "https://ajith-messages.p.rapidapi.com/getMsgs"

# now i need to generate random titles

# f = open("../apiTest.json", "w")

# headers = {"x-rapidapi-key": rapidApiKey, "x-rapidapi-host": apis[1]["apiHost"]}
# res = requests.get(
#     apis[1]["endpoint"], params={"start": "0", "paragraphs": "10"}, headers=headers
# )
# import json

# json.dump(res.json(), f, indent=2)

# for _ in range(10):
#     api = random.choice(apis)
# headers = {
#     "x-rapidapi-key": rapidApiKey,
#     "x-rapidapi-host": api['apiHost']
# }
#     params = {key: random.randint(*value) for key, value in api["queryParams"].items()}
#     response = requests.get(api["endpoint"], headers=headers, params=params)

#     f.write(responseToString(response.json()))
#     f.write("\n-----------\n")

# f.close()
# res = requests.get(
# , headers=headers, params=params
# )

# print(res.status_code)
# print(res.json())
