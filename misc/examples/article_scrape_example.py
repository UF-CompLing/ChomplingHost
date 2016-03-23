 GNU nano 2.4.2       File: article_scrape_example.py          Modified  

# Newspaper module usage example
# Newspaper pulls recent articles from news source urls

import newspaper

# Pull articles from CNN front page

cnn_paper = newspaper.build('http://cnn.com')

# Examine all cnn article urls
for article in cnn_paper.articles:
        print(article.url)

# Download and parse all articles
for article in cnn_paper.articles:
        article.download()
        article.parse()

# Title of an article
cnn_paper.articles[0].title

# Text of an article
cnn_paper.articles[0].text

# Authors
cnn_paper.articles[0].authors

# Etc

