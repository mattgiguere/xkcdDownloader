#!/usr/bin/env python

"""
Created on 2014-05-22T12:04:34
"""

from __future__ import division, print_function
import sys
import argparse
import Image
import cStringIO
from PIL import ImageFont
from PIL import ImageDraw
import os

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('You need BeautifulSoup installed')
    sys.exit(1)

try:
    import urllib2
except ImportError:
    print('You need urllib2 installed')
    sys.exit(1)


__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def xkcdDownloader(imgdir, imtype):
    """PURPOSE: To download all XKCD comics (with alt-text) to the specified
        directory and in the specified format."""

    if imgdir is None:
        imgdir = 'xkcd_images/'
    if imgdir[-1] != '/':
        imgdir += '/'

    if imtype is None:
        imtype = 'png'

    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    xkcdArchiveURL = 'http://xkcd.com/archive/'
    xkcdArchiveObj = urllib2.urlopen(xkcdArchiveURL)
    xkcdArchivePage = xkcdArchiveObj.read()

    soup = BeautifulSoup(xkcdArchivePage)

    nonComicLinksBefore = 7
    nonComicLinksAfter = 13
    links = soup.find_all('a')[nonComicLinksBefore:-nonComicLinksAfter]

    hrefs = []
    for link in links:
        hrefs.append(link.get('href'))

    for href in hrefs:
        print("now working on comic: " + href[1:-1])
        xkcdComicPageObj = urllib2.urlopen("http://xkcd.com"+href)
        xkcdComicPage = xkcdComicPageObj.read()
        soup = BeautifulSoup(xkcdComicPage)

        #extract just the div with the comic:
        comic = soup.find_all('div', attrs={"id": "comic"})

        #ONLY continue from this point on if the comic has an
        #image (and not some fancy javascript like comci 1350):
        if comic[0].find('img') is not None:
            #extract the comic image URL and load it as im.
            comicUrl = comic[0].find('img')['src']
            file = cStringIO.StringIO(urllib2.urlopen(comicUrl).read())
            im = Image.open(file)

            #get the size of the old image so we know how much padding to
            #add for the alt-text:
            oldImSize = im.size

            #break up the alt-text string:
            #each fixed-width character is 10 pixels. Figure out how
            #many characters can fit per line based on the width of the
            #comic image:
            imTextLength = int(oldImSize[0] / 10.)

            #save the comic alt-text to string:
            altText = comic[0].find('img')['title']

            #get the length of the alt-text string:
            altTextLen = len(altText)

            #now figure out how many lines you'll need below the image
            #to fit all the alt-text:
            numLines = int(altTextLen / imTextLength) + 1

            #create a new list to contain the broken up al-text into
            #each line at the bottom of the image:
            newAltText = []
            for i in range(numLines):
                newAltText.append(altText[i * imTextLength:
                                  (i + 1) * imTextLength])

            #the heigh for each line of text:
            textHeight = 25

            #create the new Image with the correct amount of padding
            #on the bottom
            newIm = Image.new("RGB", [oldImSize[0],
                              oldImSize[1] + textHeight * numLines], "white")

            #now paste the image in with no offset from the top-left corner:
            newIm.paste(im, (0, 0))
            draw = ImageDraw.Draw(newIm)

            #use a fixed-width (Mac-default) font to simplify things
            font = ImageFont.truetype("/Library/Fonts/Andale Mono.ttf", 16)
            for i in range(numLines):
                draw.text((0, oldImSize[1] + i * textHeight),
                          newAltText[i], (0, 0, 0), font=font)
            newIm.save(imgdir+href[1:-1]+'.'+imtype, imtype)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='argparse object.')
    parser.add_argument(
        'imgdir',
        help='This the directory to download all the images to. ' +
        'If not specified, all images will be downloaded into a directory ' +
        'called "xkcd_images".', nargs='?')
    parser.add_argument(
        'imtype',
        help='This argument specifies the image type to save everything as. ',
             nargs='?')

    args = parser.parse_args()

    xkcdDownloader(args.imgdir, args.imtype)
