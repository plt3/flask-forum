import asyncio
import random
import time
from json.decoder import JSONDecodeError

import aiohttp

"""ContentMaker class creates as many random forum posts/comments as needed to fill
website with test data. Favor using this module over generatePosts.py, as this one
queries APIs asynchronously and is therefore much faster.

"""


class ContentMaker:

    """Class to create any number of random posts and comments with which to populate
    website.
    createPosts method is only method a user must call to generate random posts
    createComments method is only method a user must call to generate random comments
    All others are helper methods

    """

    # max amount of sentences/paragraphs to have in a single post
    MAX_WIKI_LINES = 40
    MAX_SKATE_PARS = 3

    wikiType = "wikihow"
    skateType = "skate"

    def __init__(self, apiKey):
        """Initialize ContentMaker object with specified API key

        :apiKey: rapidapi.com API key to access wikihow, skate ipsum, random name,
        quote, and random messages APIs

        """
        self.apiKey = apiKey

    def createPosts(self, numPosts):
        """Main method to create random forum posts. A user only needs to call this
        method to create posts, and it uses most other methods in the class

        :numPosts: number of posts to create
        :returns: list of dictionaries of the form {'name': post author, 'title': post
        title, 'content': post content}

        """
        details, authors, titles, skatePars, wikiLines = asyncio.run(
            self.queryAllApis(numPosts)
        )

        madePosts = []
        wikiCounter = 0
        skateCounter = 0

        for index, post in enumerate(details):
            postDict = {"name": authors[index], "title": titles[index]}

            if post[0] == ContentMaker.wikiType:
                body = " ".join(wikiLines[wikiCounter : wikiCounter + post[1]])
                wikiCounter += post[1]
            else:
                body = "".join(skatePars[skateCounter : skateCounter + post[1]]).strip()
                skateCounter += post[1]

            postDict["content"] = body
            madePosts.append(postDict)

        return madePosts

    def createComments(self, numComments):
        """Main method to create random forum comments. A user only needs to call this
        method to create comments

        :numComments: number of comments to create
        :returns: list of dictionaries of the form {'name': comment author, 'content':
        comment content}

        """
        authors, comments = asyncio.run(self.queryCommentApis(numComments))

        return [{"name": auth, "content": com} for auth, com in zip(authors, comments)]

    async def queryCommentApis(self, numComments):
        """Main async method to query all APIs needed to create comments. Called by
        createComments method.

        :numComments: number of comments to create
        :returns: tuple of all generated names and all generated comment contents

        """
        async with aiohttp.ClientSession() as mainSession:
            tasksList = [
                self.makeNames(numComments, mainSession),
                self.makeCommentContents(numComments, mainSession),
            ]
            allNames, allContents = await asyncio.gather(*tasksList)

        return allNames, allContents

    async def queryAllApis(self, numPosts):
        """Main async method to query all APIs and return all data needed to create
        posts. Called by createPosts method.

        :numPosts: amount of posts to create
        :returns: 5-tuple consisting of lengths and types of posts to create, specified
        number of authors, specified number of titles, all skate ipsum paragraphs
        needed, and all wkihow sentences needed

        """
        postDetails, totalsDict = ContentMaker.makePostLengths(numPosts)

        async with aiohttp.ClientSession() as mainSession:
            tasksList = [
                self.makeNames(numPosts, mainSession),
                self.makeTitles(numPosts, mainSession),
                self.getSkateParagraphs(
                    totalsDict[ContentMaker.skateType], mainSession
                ),
                self.getWikihowLines(totalsDict[ContentMaker.wikiType], mainSession),
            ]

            (
                allAuthors,
                allTitles,
                allSkateParagraphs,
                allWikihowLines,
            ) = await asyncio.gather(*tasksList)

        return postDetails, allAuthors, allTitles, allSkateParagraphs, allWikihowLines

    async def getJson(self, session, url, host, params=None):
        """General method to make asynchronous HTTP GET request to an API and return
        JSON response

        :session: aiohttp ClientSession object
        :url: URL to make HTTP GET request to
        :host: rapidapi.com host header
        :params: any parameters to send with the HTTP request
        :returns: json response from API endpoint

        """
        headers = {
            "x-rapidapi-key": self.apiKey,
            "x-rapidapi-host": host,
        }

        async with session.get(url, headers=headers, params=params) as response:
            try:
                jsonResp = await response.json(content_type=None)
            except JSONDecodeError:
                # messages API sometimes returns unescaped double quotes in its JSON,
                # so this was the only way to get the message from it
                message = await response.text()
                realMessage = message[32:-2]

                jsonResp = {"Category": "Random", "Message": realMessage}

        return jsonResp

    async def makeCommentContents(self, number, session):
        """Create specified amount of comments from messages API

        :numComments: amount of comments to generate
        :session: aiohttp ClientSession object
        :returns: list of generated comments

        """
        commentUrl = "https://ajith-messages.p.rapidapi.com/getMsgs"
        commentHost = "ajith-messages.p.rapidapi.com"
        params = {"category": "random"}

        commentRequests = [
            self.getJson(session, commentUrl, commentHost, params=params)
            for _ in range(number)
        ]
        commentResponses = await asyncio.gather(*commentRequests)

        comments = [resp["Message"] for resp in commentResponses]

        return comments

    async def makeNames(self, number, session):
        """Create specified amount of random (German) names from random name API

        :number: amount of names to generate
        :session: aiohttp ClientSession object
        :returns: list of generated names

        """
        nameUrl = (
            "https://dawn2k-random-german-profiles-and-names-generator-v1."
            "p.rapidapi.com/"
        )
        nameHost = "dawn2k-random-german-profiles-and-names-generator-v1.p.rapidapi.com"
        params = {"format": "json", "count": number}

        jsonNames = await self.getJson(session, nameUrl, nameHost, params=params)

        return [elem["firstname"] + " " + elem["lastname"] for elem in jsonNames]

    async def makeTitles(self, number, session):
        """Create specified amount of post titles from random quote API

        :number: number of titles to create
        :session: aiohttp ClientSession object
        :returns: list of titles

        """
        quoteUrl = "https://fireflyquotes.p.rapidapi.com/quotes/random"
        quoteHost = "fireflyquotes.p.rapidapi.com"

        quoteRequests = [
            self.getJson(session, quoteUrl, quoteHost) for _ in range(number)
        ]
        quoteResponses = await asyncio.gather(*quoteRequests)

        titles = [resp["body"]["Quote"] for resp in quoteResponses]

        return titles

    @classmethod
    def makePostLengths(cls, numPosts):
        """Create list of tuples to represent forum posts

        :numPosts: amount of posts to create tuples for
        :returns: list of tuples of form (post type, amount of lines/paragraphs in post)
        and dictionary of how many lines/paragraphs of each type are needed

        """
        posts = []
        lengths = {cls.wikiType: 0, cls.skateType: 0}

        for _ in range(numPosts):
            postType = random.choice([cls.wikiType, cls.skateType])
            if postType == cls.wikiType:
                length = random.randint(1, cls.MAX_WIKI_LINES)
                posts.append((cls.wikiType, length))
            else:
                length = random.randint(1, cls.MAX_SKATE_PARS)
                posts.append((cls.skateType, length))

            lengths[postType] += length

        return posts, lengths

    async def getSkateParagraphs(self, numParagraphs, session):
        """Create list of specified amount of paragraphs using skate ipsum API

        :numParagraphs: amount of paragraphs to generate
        :session: aiohttp ClientSession object
        :returns: list of random skate ipsum pararaphs

        """
        url = (
            f"https://mashape-community-skate-ipsum.p.rapidapi.com/{numParagraphs}/"
            "0/JSON"
        )
        skateHost = "mashape-community-skate-ipsum.p.rapidapi.com"

        return await self.getJson(session, url, skateHost)

    async def getWikihowLines(self, numLines, session):
        """Create list of specified amount of random wikihow sentences from wikihow API

        :numLines: amount of sentences to generate
        :session: aiohttp ClientSession object
        :returns: list of random wikihow sentences

        """
        url = "https://hargrimm-wikihow-v1.p.rapidapi.com/steps"
        wikiHost = "hargrimm-wikihow-v1.p.rapidapi.com"
        wikiLines = []
        MAX_REQUEST = 1000
        requestAmounts = [MAX_REQUEST for _ in range(numLines // MAX_REQUEST)] + [
            numLines % MAX_REQUEST
        ]
        wikiRequests = [
            self.getJson(session, url, wikiHost, params={"count": amount})
            for amount in requestAmounts
        ]
        wikiResponses = await asyncio.gather(*wikiRequests)

        for resp in wikiResponses:
            lines = resp.values()
            wikiLines.extend(list(lines))

        return wikiLines


if __name__ == "__main__":
    from secretKey import rapidApiKey

    a = ContentMaker(rapidApiKey)
    start = time.time()
    # posts = a.createPosts(10)
    comments = a.createComments(10)
    end = time.time()
    print(f"Took {round(end - start, 2)} seconds.")
