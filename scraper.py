import json
import requests
import csv

api_url_base = 'https://api.viafoura.co/v2/'
headers = {
    'Content-Type': 'application/json'
}


def print_comments():
    with open('cbc_comments_with_replies.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "comment"])
        last_obj = {}
        not_complete = True
        i = 1
        results = retrieve_comments()
        for obj in results:
            last_obj = obj
            writer.writerow([last_obj['id'], last_obj['user']['name'], last_obj['content']])
            if obj['thread']:
                thread_results = obj['thread']['results']
                for subcomment in thread_results:
                    writer.writerow([subcomment['id'], subcomment['user']['name'], subcomment['content']])
                    print([subcomment['id'], subcomment['user']['name'], subcomment['content']])
            i += 1
        print(last_obj['id'])

        while not_complete:
            if i >= 100:
                i = 0
                results = retrieve_next_comments(last_obj['id'])
                for obj in results:
                    last_obj = obj
                    writer.writerow([last_obj['id'], last_obj['user']['name'], last_obj['content']])
                    if obj['thread']:
                        thread_results = obj['thread']['results']
                        for subcomment in thread_results:
                            writer.writerow([subcomment['id'], subcomment['user']['name'], subcomment['content']])
                            print([subcomment['id'], subcomment['user']['name'], subcomment['content']])
                    i += 1
            else:
                not_complete = False


def retrieve_comments():
    json_params = {'site': 'www.cbc.ca', 'requests': {
        '1': {'limit': '100', 'child_limit': 100, 'sort': 'newest', 'section': '2.636',
              'verb': 'get', 'route': '/pages/5349300019786/threads'}}}
    response = requests.get(api_url_base + "?json=" + json.dumps(json_params))
    results = response.json()['responses']['1']['result']['results']
    return results


def retrieve_next_comments(after_id):
    json_params = {'site': 'www.cbc.ca', 'requests': {
        '1': {'limit': '100', 'child_limit': 100, 'sort': 'newest', 'after_id': after_id, 'section': '2.636',
              'verb': 'get', 'route': '/pages/5349300019786/threads'}}}
    response = requests.get(api_url_base + "?json=" + json.dumps(json_params))
    results = response.json()['responses']['1']['result']['results']
    return results


print_comments()
