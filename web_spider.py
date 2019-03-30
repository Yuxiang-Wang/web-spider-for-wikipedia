# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:33:19 2019

@author: yuxiang
"""

from bs4 import BeautifulSoup
import urllib.request
import wikipedia as wp
#wp.search(name,results=1)

def get_subs_and_parent(name):
    try:
        page = wp.page(name)
    except:
        return dict(zip(['parent','subsidiaries'],['','']))
    url = page.url
    response = urllib.request.urlopen(url)
    text = response.read()
    soup = BeautifulSoup(text, 'html.parser')
    
    try:
        info = soup.find("th",string="Parent")
        parent_link = info.find_next_sibling()
        parent = parent_link.get_text()
    except:
        parent=''
        pass
    
    try:
        info = soup.find("th",string="Subsidiaries")
        subsidiaries_link = info.find_next_sibling()
        subsidiaries = subsidiaries_link.get_text()
    except:
        subsidiaries=''
        pass

    return dict(zip(['parent','subsidiaries'],[parent,subsidiaries]))



def get_infobox(name):
    try:
        page = wp.page(name) # get wikipedia search result page
    except:
        return 
    url = page.url
    response = urllib.request.urlopen(url)
    text = response.read()
    soup = BeautifulSoup(text, 'html.parser')
    
    try:
        tr = soup.find("table","infobox vcard").find_all("tr")  # find all needed info in infobox card
        title=[]
        content=[]
        for i in tr[2:]: #i=tr[-4]
            t = i.find("th").get_text()
            c = i.find("td").get_text()
            
            #### string parser
            if c[0]=='\n':
                c=c[1:]
            if c[-1]=='\n':
                c=c[:-1]
            c=c.replace('\n',',')
            
            t=t.replace('\xa0',' ')
            c=c.replace('\xa0',' ')
            
            while(c.find('[')!=-1):
                c=c.replace(c[c.find('['):c.find(']')+1],'')
            ####
            
            title.append(t)
            content.append(c)
        d = dict(zip(title,content))
    except:
        return 

    return d

name='google'
name='Corus Entertainment Inc.'

d=get_subs_and_parent(name)
d=get_infobox(name)
name='IBM'

