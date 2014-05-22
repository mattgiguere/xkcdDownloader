xkcdDownloader
==============

Downloads each XKCD comic and its respective title-text (the hidden text that appears when you mouse over the comic), 
combines them into a single image and saves the combined images for all comics to a user-specified directory. 
Dependencies include:

* [argparse](https://docs.python.org/dev/library/argparse.html)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
* [urllib2](https://docs.python.org/2/library/urllib2.html)

###Example 1

To download all comics in PNG form into a subdirectory within the current directory called xkcd_images, type the following at the command line:

`python xkcdDownloader.py`

###Example 2
To specify the directory and change the image type:

`python xkcdDownloder.py /my/xkcd/image/directory/ jpg`

In this second example, "/my/xkcd/image/directory/" is the directory xkcdDownloader will save all comics into, and "jpg" is the file format. For a full list of all available image formats see the [Python Image Library Documentation](http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html).
