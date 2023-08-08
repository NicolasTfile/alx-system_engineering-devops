#!/usr/bin/python3
"""This module queries the Reddit API"""
import requests

def recurse_count(subreddit, hot_list=[], after=None):
    """This function queries the Reddit API recursively"""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    payload = {"after": after, "limit": 100}
    headers = {"User-Agent": "Python/requests"}

    try:
        req = requests.get(url, headers=headers, params=payload,
                           allow_redirects=False)
        if req.status_code == 200:
            data = req.json()
            after = data["data"]["after"]
            for post in data["data"]["children"]:
                hot_list.append(post["data"]["title"])
            if after:
                return recurse_count(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return None
    except requests.exceptions.JSONDecodeError:
        pass

def count_words(subreddit, word_list):
    """This function queries the Reddit API and
    sorts a list of words by occurrences"""
    word_dict = {}
    all_titles = recurse_count(subreddit)
    word_list = [w.lower() for w in word_list]

    # Only parse responses that are not None
    if all_titles:
        for word in word_list:
            count = 0
            for title in all_titles:
                # Convert words to lowercase for comparison
                title = [w.lower() for w in title.split()]

                # Only count for present words in response
                if word in title:
                    count += title.count(word)

            # Only add words that are present to dictionary
            if count:
                if word_dict.get(word):
                    count += word_dict[word]
                word_dict[word] = count

        sorted_dict = dict(sorted(word_dict.items(),
                           key=lambda item: (item[1], item[0]),
                           reverse=True))

        for word, count in sorted_dict.items():
            print(f"{word}: {count}")
