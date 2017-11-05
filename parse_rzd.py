#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import sys
import config
import json
import requests
import urllib

TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Parser
def parse_rzd(counter, url, text_to_find):
    page_url = url

    browser = webdriver.Firefox()
    browser.get(page_url)

    time.sleep(10)
    element_to_find = "//*[contains(text(), {0})]".format(text_to_find)
    seats = browser.find_elements_by_xpath(element_to_find)

    if len(seats) > 0:
        print "There is tickets there"
        return "There is tickets there"

    print "%d. No tickets yet" % counter
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
        text_to_find = sys.argv[2]
    else:
        print "Please provide the url and text to find"
        return
    while True:
        time.sleep(5)
        if chat_id is None:
            updates = get_updates(last_update_id)
            chat_id = get_last_chat_id(updates)
        text = ''
        counter += 1
        try:
            text = parse_rzd(counter, url, text_to_find)
        except Exception, e:
            print e

        if text and chat_id:
            send_message(text, chat_id)
        time.sleep(10*60)


if __name__ == '__main__':
    main()
