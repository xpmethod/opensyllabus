#!/usr/bin/env python

# 0 * * * * /mnt/osp-archive-mount/code/twitter/twitter.py

import csv
from datetime import datetime
import os
import sys
import tweepy
import urllib2
import httplib
import urlparse

#log contains Twitter login creds and timestamp for most recent Tweet collected
logPath = '/mnt/osp-archive-mount/code/twitter/'
dumpPath = '/mnt/osp-archive-mount/document-dump/twitter/'

def login():
    try:
        with open(logPath+'twitter-log.csv', 'r') as f:
            log = csv.DictReader(f, delimiter=',')
            row = log.next()
            keys = [row['cons_key'], row['cons_secret'], row['a_key'], row['a_secret']]
            #'last' is the timestampt of the most recent Tweet pulled from server
            last = row['last']
    except Exception:
        print "Log file not accessible or corrupted"
        sys.exit(0)
    auth = tweepy.auth.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    api = tweepy.API(auth)
    return api, last

def save(results):
    #save the ID of the most recent Tweet in 'results'
    try:
        thisTime = results[0].id
    except Exception:
        print "Sorry, no new Tweets."
        sys.exit(0)
    with open(logPath+'twitter-log.csv', 'rb') as r:
        with open(logPath+'newlog.csv', 'wb') as w:
            read = csv.reader(r, delimiter=',')
            write = csv.writer(w,delimiter=',')
            row = read.next()
            write.writerow(row)
            row = read.next()
            row[4] = str(thisTime)
            write.writerow(row)
            r.close()
            w.close()
    os.rename(logPath+'newlog.csv', logPath+'twitter-log.csv')

def search():
    api, last = login()
    results = api.search(q='#ospsubmit', since_id=last)
    save(results)    
    finalurls = []
    users = []
    ids = []
    for result in results:
        for entry in result.entities.get('urls'):    
            fullurl=entry.get('expanded_url')
            finalurls.append(fullurl)
            users.append(result.user.screen_name)
            ids.append(result.id)
    
    return finalurls, users, api, ids

def download(finalurls):    #finalurls is a list of URLs to download
    for index in range(len(finalurls[0])):
        url = finalurls[0][index]
        user = finalurls[1][index]
        api = finalurls[2]
        tweetid = finalurls[3][index]
        
        #construct string of date to use as folder for these downloads
        date = (str(datetime.now().year) + '-' + str(datetime.now().month) + 
            '-' + str(datetime.now().day))
        if not os.path.exists(dumpPath+date):
            os.mkdir(dumpPath+date)
        
        #chop off the tracking junk from URL string
        if '?' in url:
            url=url.split('?')[0]
        
        #take last string of URL and make it into filename
        filename = url.split('/')[len(url.split('/'))-1]
        if filename=='':
            filename = url.split('/')[len(url.split('/'))-2]
    
        write = 0 #innocent until proven guilty
        
        #check filetype
        if len(filename.split('.')) == 2:
            extension = filename.split('.')[1].lower()
            if extension not in ["doc", "docx", "pdf", "txt", "rtf", "md", "html"]:
                write = 1
        else:
            write = 1
                            
        #check size
        try:
            if int(getsize(url)) > int(5242880):  
                write = 2
        except Exception:
            print "Unable to get file size."

        #Avoid overwriting files named same thing.
        counter = 1
        rawfilename = filename
        while os.path.exists(dumpPath+date+'/'+filename):
            filename = str(counter) + '-' + rawfilename
            counter += 1
    
        #download or not, depending on status
        if write == 0:
            try:
                site = urllib2.urlopen(url)
                with open(dumpPath+date+'/'+filename, 'w') as file:
                    file.write(site.read())
            except Exception:
                print "A file failed to download."
                write = 3
        tweet(write, user, filename, tweetid, api)
                
def getsize(site):
    scheme, host, path, params, query, fragment = urlparse.urlparse(site)
    if scheme != "http":
        raise ValueError("only supports HTTP requests")
    if not path:
        path = "/"
    if params:
        path = path + ";" + params
    if query:
        path = path + "?" + query
    # make a http HEAD request
    h = httplib.HTTP(host)
    h.putrequest("HEAD", path)
    h.putheader("Host", host)
    h.endheaders()
    status, reason, headers = h.getreply()
    h.close()
    size = headers.get("content-length")
    #if server doesn't send header, resort to downloading + checking (possible security issue)
    if size is None:
        page = urllib.urlopen(site)
        return len(page.read())
    return size
                
def tweet(status, user, filename, tweetid, api):
    if len(filename) > 40:
        filename = "..." + filename[-30:]
    if status == 0:
        message = "@" + user + " Thanks for submitting to the Open Syllabus Project. \'" + filename + "\' is now in the database!"
    if status == 1:
        message = "@" + user + " Sorry, \'" + filename + "\' is not in a supported format (doc/docx, pdf, htm/html, txt, rtf, or md)!"
    if status == 2:
        message = "@" + user + " Sorry, \'" + filename + "\' is too large. Please tweet a smaller copy!"
    if status == 3:
        message = "@" + user + " Woops! \'" + filename + "\' was not accessible. Please check the link and tweet again."
    print message
    try:
        api.update_status(message, tweetid)
    except Exception:
        print "Tweet failed."

download(search())
