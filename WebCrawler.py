import os.path
from bs4 import BeautifulSoup
import requests
import urllib
from Graph import Graph
import re
import validators
import csv
import http.client
import random

def crawl (url, dic_id):
    '''
    crawl webpage from given url and update list
    '''
    if (crawled.__contains__(url)):
        needToCrawl.pop(url, None) 
        return

    print("Start crawling: "+ url)
    
    open_url = urllib.request.urlopen(url)
    soup = BeautifulSoup(open_url, features="html.parser",from_encoding="iso-8859-1")
    body = soup.body

    if body is None:
        print("error", url)
        needToCrawl.pop(url, None) 
        tempid = url_id.get(url)
        webGraph.remove_node(tempid)
    else:
        useless_tags = ['script', 'style'] # This will extract all the tags we do not need 
        [x.extract() for x in body.findAll(useless_tags)]
        text = body.getText() 
        with open(os.path.join(save_path, str(dic_id) +".txt"), "w+") as f:
            f.write(text)
        
        crawl_url_id.update({url:dic_id})
        crawl_id_url.update({dic_id:url})
        crawled.append(url)
        needToCrawl.pop(url, None) 

        addLinks(soup, dic_id)

def get_last_id ():
    '''
    access global variable last_id
    last_id is last id assigned for graph
    '''
    return last_id

def addLinks (source, dic_id):
    '''
    Add every valid hyperlink from dic_id url to potential crawling list
    Update global last_id after adding every hyperlink to url dictionaries
    @param source BeautifulSoup object 
    @param dic_id id of source url
    '''
    links = source.findAll('a', attrs={'href' : re.compile('.*')})
    newID = get_last_id () + 1
    print("Updated current last id: "+ str(get_last_id ()))
    if len(links) > 100:
        links = links[0:100]
    for i in links:
        link = i['href']
        if validators.url(link) and not str(link).endswith(".pdf") and not str(link).endswith(".jpg") and not str(link).startswith("https://web.archive.org/"):
            try: 
                if urllib.request.urlopen(link).getcode() == 200: # valid request
                    if url_id.get(link) and not url_id.get(link) == dic_id:
                        webGraph.insert_edge(dic_id, url_id.get(link))
                    else:
                        needToCrawl.update({link:newID})
                        url_id.update({link:newID})
                        id_url.update({newID:link})
                        print(str(newID))
                        newID += 1
                        webGraph.insert_edge(dic_id, newID)
            except urllib.error.URLError as e:
                pass
            except UnicodeError as e:
                pass
            except http.client.RemoteDisconnected as e:
                pass
            except Exception as e:
                pass
            except ValueError as e:
                pass
    print("we finished adding edges for "+ str(dic_id))
    global last_id
    last_id = newID

## Set up os.path
save_path = '/mnt/c/Users/stella/Documents/Github/Search-Engine/Contents'
start_url = 'https://en.wikipedia.org/wiki/Grinnell_College'

global last_id
last_id = 0

crawled = []
needToCrawl = {}
needToCrawl.update({start_url:last_id})
url_id = {}
url_id.update({start_url:last_id})
id_url = {}
id_url.update({last_id:start_url})
crawl_url_id = {}
crawl_id_url = {}
webGraph = Graph ()
        
for numCrawled in range(0, 130):
    if len(needToCrawl) >= 1:
        if (len(needToCrawl) > 20):
            tempRange = (int) (len(needToCrawl)/5)
        else:
            tempRange = len(needToCrawl)
        tempurl = list(needToCrawl)[random.randrange(0, tempRange, 1)]
        # Crawling random url from list of url so that web graph is not too much concentrated to seed url
        crawl(tempurl, url_id.get(tempurl))
    else:
        break

# Save url_to_id, id_to_url dictionary in the local directory
with open(os.path.join(save_path, "url_id.csv"), "w+") as f:
    w = csv.writer(f)
    for key, val in url_id.items():
	    w.writerow([key, val])

with open(os.path.join(save_path, "id_url.csv"), "w+") as f:
    w = csv.writer(f)
    for key, val in id_url.items():
	    w.writerow([key, val])

with open(os.path.join(save_path, "c_url_id.csv"), "w+") as f:
    w = csv.writer(f)
    for key, val in crawl_url_id.items():
	    w.writerow([key, val])

with open(os.path.join(save_path, "c_id_url.csv"), "w+") as f:
    w = csv.writer(f)
    for key, val in crawl_id_url.items():
	    w.writerow([key, val])
# Save web graph
webGraph.save_graph()



    
