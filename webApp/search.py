from flask import current_app

searchablePostFields = ["title", "content"]


def addPostToIndex(postObj):
    if not current_app.elasticsearch:
        return

    payload = {field: getattr(postObj, field) for field in searchablePostFields}

    current_app.elasticsearch.index(
        index=current_app.esPostIndexName, id=postObj.id, body=payload
    )


def queryPostIndex(query):
    if not current_app.elasticsearch:
        return []

    search = current_app.elasticsearch.search(
        index=current_app.esPostIndexName,
        body={
            "query": {"multi_match": {"query": query, "fields": ["*"]}},
            "size": 10000,
            "_source": False,
        },
    )

    return [int(res["_id"]) for res in search["hits"]["hits"]]
