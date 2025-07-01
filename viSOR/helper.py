def grab_name(data, name):

    for item in data:
        if item["name"] == name:
            return item

    return None