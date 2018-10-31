#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

from __future__ import print_function
from selenium import webdriver
import time
import sys
import config
import json
import requests
import urllib
import sys


TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Parser
def parse_rzd(counter, url, train_number, text_to_find):
    page_url = url

    # browser = webdriver.Firefox()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x800')
    browser = webdriver.Chrome(options=options)

    browser.get(page_url)

    time.sleep(10)

    items = browser.find_elements_by_class_name('route-item')
    # print ("trains: %d" % len(items))
    for item in items:
        item_train_number = item.find_element_by_xpath('.//span[contains(@class, "route-trnum")]').text
        # print(item_train_number)
        if train_number not in item_train_number:
            continue

        element_to_find = ".//*[contains(text(), '{0}')]".format(text_to_find)
        seats = item.find_elements_by_xpath(element_to_find)

        if len(seats) > 0:
            eprint("There are tickets there")
            browser.close()
            return "There are tickets there"

    eprint("%d. No tickets yet" % counter)
    browser.close()


# Bot part
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def get_last_chat_id(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return chat_id


def send_message(text, chat_id):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    chat_id = None
    counter = 0
    url = ""
    text_to_find = ""
    if len(sys.argv) > 2:
        url = sys.argv[1]
        train_number = sys.argv[2]
        text_to_find = sys.argv[3]
    else:
        print("Please provide the url, train number and text to find")
        return
    while True:
        time.sleep(5)
        if chat_id is None:
            updates = get_updates(last_update_id)
            chat_id = get_last_chat_id(updates)
        text = ''
        counter += 1
        try:
            eprint("LOG: trying to open page")
            text = parse_rzd(counter, url, train_number, text_to_find)
            eprint("#%d %s" % (counter, text))
        except Exception as e:
            print(e)

        if text and chat_id:
            text = text + " " + url
            eprint("LOG: sending message '%s'" % text)
            send_message(text, chat_id)
        eprint("LOG: going to sleep")
        time.sleep(10*60)


if __name__ == '__main__':
    main()
