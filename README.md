# Sentiment Analysis (updated 23 February 2016)

This is the repository for all the work done by the UF Computational Linguistics Club Sentiment Analysis Group

*New members should make sure to glance over the "quickstart" notes at the bottom of this page.*

## Members: (Feel free to add your name)

* Dax Gerts
* ...
* ...
* ...

## Projects & Files

### Sentiment mining from journalistic sources

* **news_updater/ version 1.0 is complete!** -Dax: I currently have it running every 15 minutes on my machine, see **papers_master.csv** for hourly updated master file of all articles
* **papers/** small examples of articles from each source, good for testing models with
* **examples/** misc. article extraction and analsyis examples

#### Analysis Tasks

1. Objectivity v. Subjectivity

2. Specific sentiment

#### Data Tasks

1. Compile "training" corpora

2. Test different sources

* Full articles from web
* RSS feeds titles + summaries
* Twitter news (might be same as RSS)

## Quickstart:

(Dax) We'll definitely be using the python-NLTK toolkit in the projects

### NLTK install instructions

#### Linux

Open up the terminal and enter the following command...

```bash
sudo apt-get install python-nltk
```

This installed the basics of the nltk toolkit, but before it can be used you have to make sure to download all of the corpora and libraries. This can be done from command line as well.

```bash
python
```

This opens up python in the terminal. From here enter the following...

```python
import nltk
nltk.download('all')
```

Alternatively ```nltk.download()``` opens the downloader GUI.

This stage often causes errors and requires a stable internet connection. Even if it appears that the download doesn't finish, make sure to test the packages on existing code to see if they work. Also, the download will likely seem to stall on "panlex lite", but it most likely hasn't, the download just takes a really long time.

#### Windows

#### Mac

### Python "Newspaper" Module

The "newspaper" module allows for news articles to be parsed in bulk and transformed directly into plain text with a minimum of effort.

Installation instructions are here: http://newspaper.readthedocs.org/en/latest/user_guide/install.html#install

*Be warned: there are a lot of dependencies and things can get pretty finicky, if you need help just ask me -Dax*

## References & Readings

Python NLTK - www.nltk.org

NLTK Cheatsheet (this is your friend) - https://blogs.princeton.edu/etc/files/2014/03/Text-Analysis-with-NLTK-Cheatsheet.pdf

Sentiment Analysis with Twitter - www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
