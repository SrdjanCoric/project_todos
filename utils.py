def error_for_list_name(name, lists):
    if not 1 <= len(name) <= 100:
        return "The list name must be between 1 and 100 characters"
    elif any(lst['name'] == name for lst in lists):
        return "The list name must be unique."

    return None

def error_for_todo(name):
    if not 1 <= len(name) <= 100:
        return "Todo name must be between 1 and 100 characters"

    return None