------------------------------------Instructions to run Crawler.py--------------------------------

Author: Kunal Bohra
email:bohra.k@husky.neu.edu
License: MIT 


Requirements:

1. Python 2.x or more running on system
2. Uninterruted network connection to World Wide Web


1. The folder Web_Crawler has main file Crawler.py which contains the code to run the crawler. 

2. Copy the main folde Web_Crawler anywhere in your file system. 

3. Go to command line and change your current working directory to Web_Crawler

Example: /home/tony/Documents -> /home/tony/Documents/Web_Crawler

4. Run the following command:

/home/tony/Documents/Web_Crawler$ python<space><seed url><space><"keyphrase">

---Where seed url is root url to start crawl with.
---keyphrase is an optional parameter for focused crawling. Note that there are double quotes around keyphrase.


5. The program run for certain time, displayin some stats and progess on console. 

6. As the program terminates, we have a text output file named Crawled_Links.txt in the same current working directory folder. 
It has all the results of crawling. Basically contains each link crawled. 

