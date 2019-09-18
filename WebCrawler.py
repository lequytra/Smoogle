import os.path
from bs4 import BeautifulSoup
import requests
import urllib
from Graph import Graph
import re
import validators
import csv

def crawl (url, dic_id):
    '''
    crawl webpage from given url and update list
    '''
    if (crawled.__contains__(url)):
        needToCrawl.remove(url)
        return

    print(url)
    ## Write content in function
    try: open_url = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        needToCrawl.remove(url)
        tempid = url_id.get(url)
        webGraph.remove_node(tempid)
        print(e.reason, url)
        return
    
    soup = BeautifulSoup(open_url, features="html.parser",from_encoding="iso-8859-1")
    body = soup.body

    if body is None:
        print("error", url)
        needToCrawl.remove(url)
        tempid = url_id.get(url)
        webGraph.remove_node(tempid)
    else:
        #useless_tags = ['script', 'style']
        # This will extract all the tags we do not need 
        # #[x.extract() for x in body.findAll(useless_tags)]
        text = body.getText() 
        with open(os.path.join(save_path, "content " + str(dic_id) +".txt"), "w+") as f:
            f.write(text)
        
        url_id.update({url:dic_id})
        id_url.update({dic_id:url})
        crawled.append(url)
        needToCrawl.remove(url)

        return addLinks(soup, dic_id)

def addLinks (source, dic_id):
    links = source.findAll('a', attrs={'href' : re.compile('.*')})
    newID = dic_id
    for i in links:
        link = i['href']
        if validators.url(link) and not re.match(r'^https://web.archive.org/', link):
            needToCrawl.append(link)
            if url_id.get(link):
                webGraph.insert_edge(dic_id, url_id.get(link))
            else:
                newID += 1
                webGraph.insert_edge(dic_id, newID)
    print("we added edges for "+ str(dic_id))
    return newID

## Set up os.path
save_path = '/mnt/c/Users/stella/Documents/Github/Search-Engine/Contents'
start_url = 'https://en.wikipedia.org/wiki/Grinnell_College'

dic_id = 0
crawled = []
needToCrawl = [start_url]
url_id = {}
id_url = {}
webGraph = Graph ()
        
for counter in range(0, 10):
    print (needToCrawl[0], dic_id)
    dic_id = crawl(needToCrawl[0], dic_id)

w = csv.writer(open("/mnt/c/Users/stella/Documents/Github/Search-Engine/url_id.csv"), "w")
for key, val in url_id.items():
	w.writerow([key, val])

w2 = csv.writer(open("/mnt/c/Users/stella/Documents/Github/Search-Engine/id_url.csv"), "w")
for key, val in id_url.items():
	w.writerow([key, val])




    
