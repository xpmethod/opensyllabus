import csv
from datetime import datetime
import os
import sys
import tweepy
import urllib2

#log contains Twitter login creds and timestamp for most recent Tweet collected
logPath = '/home/jonahsmith/OSP-ARCHIVE/code/twitter/'
dumpPath = '/home/jonahsmith/OSP-ARCHIVE/document-dump/'

download(search())

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
    results = api.search(q='#syllabus', since_id=last)
    save(results)    
    #Extract all links and their destinations *after redirects*
    finalurls = []
    for result in results:
        tweet = result.entities
        for entry in tweet.get('urls'):
            url=entry.get('expanded_url')
            try:
                fullurl = urllib2.urlopen(url).geturl()
            except Exception:
                print "Woops, one of the links is broken."
                continue
            else:
                finalurls.append(fullurl)

    #Squash duplicates
    finalurls = list(set(finalurls))
    return finalurls

def download(finalurls):    #finalurls is a list of URLs to download
    for url in finalurls:
        try:
            site = urllib2.urlopen(url)
        except Exception:
            pass
        else:
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
            #Add .html if no extension is available. Better than nothing.
            if "." not in filename:
                filename = filename+".html"
            rawfilename = filename
            #Avoid ovewriting files named same thing.
            counter = 1
            while os.path.exists(dumpPath+date+'/'+filename):
                filename = str(counter) + '-' + rawfilename
                counter += 1
            with open(dumpPath+date+'/'+filename, 'w') as file:
                file.write(site.read())