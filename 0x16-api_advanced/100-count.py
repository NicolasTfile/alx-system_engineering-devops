#!/usr/bin/python3
"""This module queries the reddit API"""
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """This function queries the reddit API recursively
    """
    if counts is None:
        counts = {}

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot/.json?after={after}"
    
    headers = {"User-Agent": "Python/requests"}
    params = {"limit": 100}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code == 200:
        data = response.json().get("data")
        after = data.get("after")

        for child in data.get("children"):
            title = child.get("data").get("title").lower()
            for word in word_list:
                word = word.lower()
                if word in title and f" {word} " not in title:
                    counts[word] = counts.get(word, 0) + 1

        if after is not None:
            return count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
