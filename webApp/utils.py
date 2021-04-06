def getReplies(searchList, id, sort=False):
    # return comments replying to the specified ID (from comment list from database)

    if id == 0:
        id = None

    replies = [comment for comment in searchList if comment.replyId == id]

    if sort:
        replies.sort(key=lambda x: x.id)

    return replies


def createListDict(wholeList, id=0, appendList=False):
    # recursively create JSON-like nested list of dictionaries representing comment
    # threads from flat list returned by database query
    # NOTE: never specify id or appendList parameters, they are only for recursion

    if id == 0:
        appendList = []

    for comment in getReplies(wholeList, id):
        commentDict = {
            "id": comment.id,
            "author": comment.author,
            "content": comment.content,
            "created": comment.created,
            "replies": [],
        }
        appendList.insert(0, commentDict)
        createListDict(wholeList, commentDict["id"], commentDict["replies"])

    if id == 0:
        return appendList
