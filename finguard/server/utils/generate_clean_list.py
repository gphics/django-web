
def get_clean_list(arr:list) -> list:
    """
    This function loops through a given list and remove any 'False' item in it
    """

    result = []

    for item in arr:

        if not isinstance(item, bool):

            result.append(item)

    return result