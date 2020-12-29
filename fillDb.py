import random
import time

import requests


class PostMaker:

    """Class to create any number of random posts with which to populate website.
    createPosts method is only method needed to call."""

    # max amount of sentences/paragraphs to have in a single post
    MAX_WIKI_LINES = 40
    MAX_SKATE_PARS = 3

    wikiType = "wikihow"
    skateType = "skate"

    def __init__(self, apiKey):
        """Initialize PostMaker object with specified API key

        :apiKey: rapidapi.com API key to access wikihow, skate ipsum, random name,
        quote, and random messages APIs

        """

        self.apiKey = apiKey

    def createPosts(self, numPosts):
        """Create list of tuples representing specified number of posts to make

        :numPosts: amount of posts to create
        :returns: list of tuples representing posts, in the form
        (author, title, content)

        """
        start = time.time()
        allAuthors = self.makeNames(numPosts)
        print("got all authors")
        t1 = time.time()
        print(t1 - start)
        allTitles = self.makeTitles(numPosts)
        print("got all titles")
        t2 = time.time()
        print(t2 - t1)
        postDetails, totalsDict = PostMaker.makePostLengths(numPosts)
        print("made all post lengths")
        t3 = time.time()
        print(t3 - t2)
        allSkateParagraphs = self.getSkateParagraphs(totalsDict[PostMaker.skateType])
        print("got all paragraphs")
        t4 = time.time()
        print(t4 - t3)
        allWikihowLines = self.getWikihowLines(totalsDict[PostMaker.wikiType])
        print("got all lines")
        t5 = time.time()
        print(t5 - t4)
        print("took", t5 - start)

        madePosts = []
        wikiCounter = 0
        skateCounter = 0

        for index, post in enumerate(postDetails):
            if post[0] == PostMaker.wikiType:
                body = " ".join(allWikihowLines[wikiCounter : wikiCounter + post[1]])
                madePosts.append((allAuthors[index], allTitles[index], body))
                wikiCounter += post[1]
            else:
                body = "".join(
                    allSkateParagraphs[skateCounter : skateCounter + post[1]]
                ).strip()
                madePosts.append((allAuthors[index], allTitles[index], body))
                skateCounter += post[1]

        return madePosts

    def makeNames(self, number):
        """Create specified amount of random (German) names from random name API

        :number: amount of names to generate
        :returns: list of generated names

        """
        nameUrl = (
            "https://dawn2k-random-german-profiles-and-names-generator-v1."
            "p.rapidapi.com/"
        )
        headers = {
            "x-rapidapi-key": self.apiKey,
            "x-rapidapi-host": (
                "dawn2k-random-german-profiles-and-names-generator-v1.p.rapidapi.com"
            ),
        }
        params = {"format": "json", "count": number}

        response = requests.get(nameUrl, headers=headers, params=params)
        response.raise_for_status()

        return [elem["firstname"] + " " + elem["lastname"] for elem in response.json()]

    def makeTitles(self, number):
        """Create specified amount of post titles from random quote API

        :number: number of titles to create
        :returns: list of titles

        """
        quoteUrl = "https://fireflyquotes.p.rapidapi.com/quotes/random"
        headers = {
            "x-rapidapi-key": self.apiKey,
            "x-rapidapi-host": "fireflyquotes.p.rapidapi.com",
        }

        titles = []

        for _ in range(number):
            response = requests.get(quoteUrl, headers=headers)
            response.raise_for_status()
            title = response.json()["body"]["Quote"]
            titles.append(title)

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

    def getSkateParagraphs(self, numParagraphs):
        """Create list of specified amount of paragraphs using skate ipsum API

        :numParagraphs: amount of paragraphs to generate
        :returns: list of random skate ipsum pararaphs

        """
        url = (
            f"https://mashape-community-skate-ipsum.p.rapidapi.com/{numParagraphs}/"
            "0/JSON"
        )
        headers = {
            "x-rapidapi-key": self.apiKey,
            "x-rapidapi-host": "mashape-community-skate-ipsum.p.rapidapi.com",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def getWikihowLines(self, numLines):
        """Create list of specified amount of random wikihow sentences from wikihow API

        :numLines: amount of sentences to generate
        :returns: list of random wikihow sentences

        """
        url = "https://hargrimm-wikihow-v1.p.rapidapi.com/steps"
        headers = {
            "x-rapidapi-key": self.apiKey,
            "x-rapidapi-host": "hargrimm-wikihow-v1.p.rapidapi.com",
        }
        wikiLines = []
        MAX_REQUEST = 1000
        requestAmounts = [MAX_REQUEST for _ in range(numLines // MAX_REQUEST)] + [
            numLines % MAX_REQUEST
        ]
        for amount in requestAmounts:
            params = {"count": amount}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            wikiLines.extend(list(response.json().values()))

        return wikiLines
