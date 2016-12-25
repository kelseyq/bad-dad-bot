#!/usr/bin/env python

from twython import Twython
import random
import json

APP_KEY = ''
APP_SECRET = ''
TOKEN = ""
TOKEN_SECRET = ""
twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)

terms = ['tech worker', 'software engineer', 'computer programmer', 'software developer',
         'frontend dev', 'web developer', '10x developer', "linux developer", "web dev", 'backend dev', 'lead developer',
         'javascript dev', 'python dev', 'full stack dev', 'data scientist', 'coder', 'developer', 'programmer']

nope_words = [
    "african",
    "bitch",
    "black",
    "chinaman",
    "chinamen",
    "chink",
    "crip",
    "cunt",
    "dyke",
    "fag",
    "gimp",
    "homo",
    "hooker",
    "india",
    "jap",
    "kike",
    "lunatic",
    "negro",
    "nigga",
    "nigger",
    "nigguh",
    "paki",
    "pussy",
    "raghead",
    "retard",
    "shemale",
    "skank",
    "slut",
    "tard",
    "tits",
    "titt",
    "trannie",
    "tranny",
    'trans',
    "twat",
    "wetback",
    "whore",
    "estate",
    "game",
    "developer update",
]


def filter_tweets(results, search_term, seen_tweets):
    return [seen_tweets.add(result['retweeted_status']['text']) or result for result in results['statuses'] if
                  result.get('retweeted_status') and
                  result['retweeted_status']['text'] not in seen_tweets and
                  len(result['entities']['urls']) == 0 and
                  len(result['retweeted_status']['entities']['urls']) == 0 and
                  len(result['retweeted_status']['entities']['user_mentions']) == 0 and
                  result['retweeted_status']['favorite_count'] > 1 and
                  search_term in result['retweeted_status']['text'] and
                  not any(nope in result['retweeted_status']['text'].lower() for nope in nope_words)]


def get_tweets_for_term(search_term, seen_tweets):
    first_page = twitter.search(q=search_term, lang='en', result_type='recent', count=100)
    if first_page.get('statuses'):
        #result['retweeted_status']['text']
        #json.dumps(result, indent=4)
        tweets = filter_tweets(first_page, search_term, seen_tweets)
        # max_id = first_page['statuses'][-1]['id_str']
        # second_page = twitter.search(q=search_term, lang='en', result_type='recent', max_id=max_id)
        # tweets = filter_tweets(second_page, search_term, seen_tweets)
        # max_id = second_page['statuses'][-1]['id_str']
        # third_page = twitter.search(q=search_term, lang='en', result_type='recent', max_id=max_id)
        # tweets = tweets + filter_tweets(third_page, search_term, seen_tweets)
        print(str(len(tweets)) + " results for search term " + search_term)
        return tweets


def baddadize(text):
    simplified_terms = ['tech worker', 'software engineer', 'computer programmer', 'software developer',
                        'web developer', 'web dev', 'data scientist', 'coder', 'developer', 'programmer', 'dev']
    replaced_string = text
    for term in simplified_terms:
        replaced_string = replaced_string.replace(term, "bad dad")
    return replaced_string

def main():
    seen_tweets = set()
    tweets = [get_tweets_for_term(term, seen_tweets) +
              get_tweets_for_term(term + 's', seen_tweets) +
              get_tweets_for_term(term + "'s", seen_tweets) for term in terms]
    tweets = [item for sublist in tweets for item in sublist]
    my_latest_tweets = [tweet['text'] for tweet in twitter.get_user_timeline(count=5)]
    print(my_latest_tweets)
    tweeted = False
    tries = 0
    while not(tweeted) and (tries < 10):
        tries += 1
        tweet = random.choice(tweets)
        baddadized = baddadize(tweet['retweeted_status']['text'])
        print('trying: ' + baddadized)
        if baddadized not in my_latest_tweets:
            twitter.update_status(status=baddadized)
            tweeted = True

    if tweeted:
        print('tweeted: ' + baddadized + " after " + str(tries) + " tries")

if __name__ == "__main__":
    main()
