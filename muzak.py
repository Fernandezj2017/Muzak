`# muzak music tracker

import requests, re, time
import csv, pafy
import urllib
import urllib2
from bs4 import BeautifulSoup

urls = {
    'uptown' : 'http://muzakwpn.muzak.com/wpn/088.html',
    # 'metro' : 'http://muzakwpn.muzak.com/wpn/043.html',
    # 'stylus' : 'http://muzakwpn.muzak.com/wpn/076.html',
    # 'strobe' : 'http://muzakwpn.muzak.com/wpn/033.html',
    # 'nulounge' : 'http://muzakwpn.muzak.com/wpn/061.html',
    # 'perimiter' : 'http://muzakwpn.muzak.com/wpn/073.html'
}

utube = 'https://www.youtube.com'

path = 'C:\Users\jfern\Desktop'


ptrn = '(?<=\>)[\w /\'.,!+\^\-\*?()\[\]]+, by [\w /\'.,!+\^\-\*?()\[\]]+(?=<|$)'

def parse_song(line):
    match = re.findall(ptrn,line)[0]
    return match.replace(", by "," ")

def parse_playlist(url):
    page_content = requests.get(url).content
    return [line for line in page_content.split('\n') if ', by' in line]

def get_music():
    return [
        {'title' : parse_song(line), 'source' : key}
        for key in urls
        for line in parse_playlist(urls[key])
    ]


def get_url(songtitle):
    query = urllib.quote(songtitle)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        link = utube + vid['href']
        video = pafy.new(link)
        bestaudio = video.getbestaudio()
        bestaudio.download(quiet=False, filepath=path)  


    # song_url = [{utube + vid['href']} for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'})]
    return song_url

# def dicts_to_csv(list_of_urls, filename='music'):
    # """Saves list of urls to CSV"""
    # outfilename = filename + ".csv"
    # toCSV = list_of_urls
    # keys = list_of_urls[0].keys()
    # f = open(outfilename, 'wb')
    # dict_writer = csv.DictWriter(f, keys)
    # dict_writer.writer.writerow(keys)
    # dict_writer.writerows(toCSV)
    # f.close()
    # return outfilename 

# def get_songs():
    # music = get_music() 
    # return [
        # {'url' : get_url(song['title'])[0]} for song in music
    # ]
    # return[
        # {'song_title' : song['title'], 'url' : get_url(song['title'])[0]}
        # for song in music
    # ]

# def download_songs(songs):
    # for link in songs:
        # video = pafy.new(link)
        # bestaudio = video.getbestaudio()
        # bestaudio.download(quiet=False, filepath=path)

if __name__ == '__main__':
    music = get_music()
    for song in music:
        get_url(song['title'])
    print "Done!"
    # outfilename = dicts_to_csv(songs)
    # print "saved to", outfilename