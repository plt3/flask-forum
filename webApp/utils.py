from datetime import datetime


def getReplies(searchList, id, sort=False):
    # return comments replying to the specified ID (from comment list from database)
    replies = [comment for comment in searchList if comment["replyTo"] == id]

    if sort:
        replies.sort(key=lambda x: x["id"])

    return replies


def createListDict(wholeList, id=0, appendList=False):
    # recursively create JSON-like nested list of dictionaries representing comment
    # threads from flat list returned by database query
    # NOTE: never specify id or appendList parameters, they are only for recursion
    if id == 0:
        appendList = []

    # the datetime.now() is a patch. This needs to be replaced with the actual time

    for comment in getReplies(wholeList, id):
        commentDict = {
            "id": comment["id"],
            "author": comment["author"],
            "date": datetime.now(),
            "content": comment["content"],
            "replies": [],
        }
        appendList.append(commentDict)
        createListDict(wholeList, commentDict["id"], commentDict["replies"])

    if id == 0:
        return appendList
