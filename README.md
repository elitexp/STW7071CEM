### Task 1: Search Engine
Create a vertical search engine comparable to Google Scholar, but specialized in retrieving just papers/books published by a member of Coventry University's Research Centre for health and life sciences (RCHL): https://pureportal.coventry.ac.uk/en/organisations/centre-for-health-and-life-sciences

Your system crawls the relevant web pages and retrieves information about all available
publications. For each publication, it extracts available data (such as authors, publication year,
and title) and the links to both the publication page and the author's profile (also called "pureportal"
profile) page.
Make sure you that your crawler is polite, i.e. it preserves the robots.txt rules and does not hit the
servers unnecessarily or too fast.
Because of low rate of changes to this information, your crawler may be scheduled to look for new
information, say, once per week, but it should ideally be able to do so automatically, as a scheduled
task. Every time it runs, it should update the index with the new data. Make sure you apply the
required pre-processing tasks to both the crawled data and the users' queries.
From the user's perspective, your system provides an interface similar to Google Scholar's main
page, where the user may enter in queries/keywords concerning the resources they wish to locate.
The results will then be shown by your system, arranged by relevancy, in a manner similar to
Google Scholar. However, the search results are limited to RCHL members' publications. Unless
you aim to earn a score of 70 or above, the user interface does not need to be web-based (like
Google Scholar), and the usual Python interface in your IDE would do. However, for more usability,
it would be preferable to be able to click on the printed links rather than copying and pasting them
into a browser.

### Task 2: Document Clustering
Develop a document clustering system.
First, collect a number of documents that belong to different categories, namely Sport, Health
and Business. Each document should be at least one sentence (the longer is usually the better).
The total number of documents is up to you but should be at least 100 (the more is usually the
better). You may collect these document from publicly available web sites such as BBC news
websites, but make sure you preserve their copyrights and terms of use and clearly cite them in
your work. You may simply copy-paste such texts manually, and writing an RSS feed
reader/crawler to do it automatically is NOT mandatory.
Once you have collected sufficient documents, cluster them using a standard clustering method
(e.g. K-means).
Finally, use the created model to assign a new document to one of the existing clusters. That is,
the user enters a document (e.g. a sentence) and your system outputs the right cluster.
NOTE: You must show in your report and viva that your system suggests the right cluster for variety
of inputs, e.g. short and long inputs, those with and without stop worlds, inputs of different topics,
as well as more challenging inputs to show the system is robust enough.