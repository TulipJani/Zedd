import urllib.parse
import webbrowser



def search_flipkart(query):
    url = f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Flipkart Search", url)]

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("YouTube Search", url)]

def search_amazon(query):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Amazon Search", url)]

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Google Search", url)]

def search_twitter(query):
    url = f"https://twitter.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Twitter Search", url)]

def search_instagram(query):
    url = f"https://www.instagram.com/{urllib.parse.quote(query)}/"
    webbrowser.open(url)
    return [("Instagram Search", url)]

def search_reddit(query):
    url = f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Reddit Search", url)]

def search_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("eBay Search", url)]

def search_wikipedia(query):
    url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Wikipedia Search", url)]

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Bing Search", url)]


def parse_input(user_input):
    parts = user_input.lower().strip().split(" on ")
    if len(parts) == 2 and parts[0].startswith("search for "):
        query = parts[0][11:].strip()
        platform = parts[1].strip()
        return query, platform
    elif len(parts) == 2:
        query = parts[0].strip()
        platform = parts[1].strip()
        return query, platform
    else:
        return None, None

def handle_search(user_input):
    query, platform = parse_input(user_input)
    if not query or not platform:
        return "Invalid input format. Please use 'search for [query] on [platform]'."

    search_functions = {
        "flipkart": search_flipkart,
        "amazon": search_amazon,
        "youtube": search_youtube,
        "google": search_google,
        "twitter": search_twitter,
        "instagram": search_instagram,
        "reddit": search_reddit,
        "ebay": search_ebay,
        "wikipedia": search_wikipedia,
        "bing": search_bing,
    }

    search_function = search_functions.get(platform)
    if search_function:
        search_function(query)
        return f"Here's what i've found."
    else:
        return f"Unsupported platform: {platform}."

