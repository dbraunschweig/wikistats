import json
import operator
import re
import string
import time
import urllib.parse
import urllib.request
import requests

titles = dict()


def get_pagestats(wiki, title, start, end):
    global titles

    title = title.replace(" ", "_")
    title = urllib.parse.quote(title)
    title = title.replace("/", "%2f")
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"\
        + wiki + "/all-access/user/"\
        + title + "/daily/" + start + "/" + end
    try:
        page = urllib.request.urlopen(url).read()
    except:
        print("Error reading " + url)
        return
    page = page.decode("UTF-8")

    items = json.loads(page)
    for item in items["items"]:
        title = item["article"]
        views = int(item["views"])

        if title in titles:
            titles[title] += views
        else:
            titles[title] = views


def get_wikistats(wiki, date):
    global titles

    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/" + wiki + "/all-access/" + date
    try:
        page = urllib.request.urlopen(url).read()
    except:
        print("Error reading " + url)
        return
    page = page.decode("UTF-8")

    items = json.loads(page)
    items = items["items"][0]
    for item in items["articles"]:
        title = item["article"]
        views = int(item["views"])

        if title in titles:
            titles[title] += views
        else:
            titles[title] = views


def get_month(wiki, month):
    for day in range(1, 32):
        date = month + "/" + '{num:02d}'.format(num=day)
        if time.strftime("%Y/%m/%d") <= date:
            break
        print(date)
        try:
            get_wikistats(wiki, date)
        except:
            break


def monthly_stats(wiki, month):
    global titles

    get_month(wiki, month)
    list = sorted(titles.items())
    list = sorted(list, key=lambda x: -x[1])

    count = 0
    for record in list:
        text = "# {} - [[{}]]".format(record[1], record[0])
        text = text.replace("[[File:", "[[:File:")
        text = text.replace("[[Category:", "[[:Category:")
        text = text.replace("_", " ")
        print(text)
        count += 1
        if count >= 1000:
            break


def yearly_stats(year):
    global titles

    regex = re.compile('<li>([^ ]*)[^>]*>([^<]*)')
    for month in range(1, 13):
        url = "https://en.wikiversity.org/wiki/Wikiversity:Statistics/" + str(year) + "/" + str(month).rjust(2, "0")
        print(url)
        page = urllib.request.urlopen(url).read()
        page = page.decode("utf-8")
        index = str.find(page, '<ol>')
        page = page[index + 5:]
        index = str.find(page, '</ol>')
        page = page[0:index]

        lines = page.split("\n")
        for line in lines:
            match = regex.search(line)
            if match != None:
                views = int(match.groups()[0])
                title = match.groups()[1]

                if title in titles:
                    titles[title] += views
                else:
                    titles[title] = views

    list = sorted(titles.items())
    list = sorted(list, key=lambda x: -x[1])

    count = 0
    for record in list:
        text = "# {} - [[{}]]".format(record[1], record[0])
        text = text.replace("[[File:", "[[:File:")
        text = text.replace("[[Category:", "[[:Category:")
        text = text.replace("_", " ")
        print(text)
        count += 1
        if count >= 1000:
            break


def page_stats(wiki, pages, start, end):
    global titles

    for page in pages:
        print(page)
        get_pagestats("en.wikiversity", page, start, end)

    list = sorted(titles.items())
    list = sorted(list, key=lambda x: -x[1])

    count = 0
    for record in list:
        text = "# {} - [[{}]]".format(record[1], record[0])
        text = text.replace("[[File:", "[[:File:")
        text = text.replace("[[Category:", "[[:Category:")
        text = text.replace("_", " ")
        print(text)


monthly_stats("en.wikiversity", "2016/03")
#yearly_stats("2015")
exit()

pages = [
    "IT Fundamentals"
    # ...
]

page_stats("en.wikiversity", pages, "20151101", "20160229")
