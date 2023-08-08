#!/usr/bin/python3
"""This module queries the reddit API"""
import requests

def count_words(subreddit, word_list, after=None, counts={}):
    """This function queries the reddit API recursively
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {"User-Agent": "Python/requests"}
    params = {
        "after": after,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    
    if response.status_code != 200:
        return
    
    results = response.json().get("data")
    after = results.get("after")
    
    for c in results.get("children"):
        title = c.get("data").get("title").lower()
        for word in word_list:
            word = word.lower()
            if word in title and " " + word + " " not in title:
                counts[word] = counts.get(word, 0) + 1

    if after is not None:
        return count_words(subreddit, word_list, after, counts)
    
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")
