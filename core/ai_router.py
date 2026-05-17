def route_query(query):

    query = query.lower()

    simple_keywords = [
        "list",
        "create",
        "delete",
        "remove",
        "folder",
        "file",
        "disk",
        "scan",
        "cd",
        "dir"
    ]

    for word in simple_keywords:
        if word in query.lower():
            try:
                return cloud_ai(query)
            except:
                return local_reasoning(query)

