#########  A Focused Web Crawler  ###########


'''
Author: Kunal Bohra
CS 6200
email:bohra.k@husky.neu.edu
NUID:001971024
'''


import urlparse
from bs4 import BeautifulSoup
from collections import deque
import urllib2
import time
import sys
import re

#Constant Declaration

#unseen_list is a List of URLs that are to be visited
unseen_list = []

#seen_list is a list of URLs that are visited
seen_list = []

#List of all crawled urls
result_list = []

#This list contains urls with keyword
new_list = []

#It should be noted that in case of empty keyphrase, new_list and seen_list
#has same entries.

#Base depth to start crawling
start_depth = 1

#Constant is the halting measure of the crawling algorithm
halt_limit = 4

#Constant for Main Wiki Page
main_page = 'http://en.wikipedia.org/wiki/Main_Page'

#Constant for base englisht wiki page
base_page = 'http://en.wikipedia.org/wiki/'

#keyphrase = "information retrieval"
    
#baseURL = "http://en.wikipedia.org/wiki/Gerard_Salton"

#Set recursion limit on the crawler.
sys.setrecursionlimit(2500)

#Sanity Checks

if len(sys.argv) < 2:
#This boolean helps in switching mode later on
    print "Cannot start without Seed URL !!!!"
else:
    baseURL = sys.argv[1]

if len(sys.argv) > 2:
#There is a keyphrase as an optional keyword
    keyphrase = sys.argv[2]
    print "Keyphrase is:  "+str(keyphrase)
else:
    keyphrase=""


    
#Function to check for Canonical URL
def check_canonical(url):
    #Request page
    
    #Respect robots.txt Delay for 1 second
    time.sleep(1)	
    request = urllib2.urlopen(url)
    
    #Read the page contents and store them
    response = request.read()
    request.close()
    #Parse the contents of web page
    soup = BeautifulSoup(response)
    
    #Final all link tages with canonical attribute
    links = soup.findAll('link')
    
    #Check if we are inputted with a canonical URL
    for link in links:
        if "canonical"  in str(link.get('rel')):
	    #print "In cannonical"
            return link.get('href')
    return url

#Function to validate a URL according to problem statement    
def validate_url(url,seen_list,unseen_list):
    if '#' in url:
        updated_url = url.partition('#')[0]
    else:
        updated_url = url
                
    #URL should not be same as Main wiki page
    constraintOne = updated_url != main_page
            
    #URL should not start with English wiki articles
    constraintTwo = updated_url.startswith(base_page)
                
    #URL should not already be visited. Else we have cycles
    constraintThree = updated_url not in seen_list
                
    #URL should be in unseen_list
    constraintFour = updated_url not in unseen_list
                
    if constraintOne and constraintTwo and constraintThree and constraintFour:
        return True
    else:
        return False

#Function to scrap all text from a page.
def scrap_page(soup):
    #Scrap text from web page for focus crawling mode

    #Remove all style and javascript elements
    for script in soup(["style","script"]):
        script.extract()
        
    #Fetch all text from page
    text = soup.get_text()
    
    #Format the data 
    text_line = (line.strip() for line in text.splitlines())
    
    #Create text chunks
    blocks = (para.strip() for line in text_line for para in line.split("  "))
    
    #Final formatting
    text = '\n'.join(block for block in blocks if block)

    #Encode data to readable form
    base_scrap = (text.encode('utf-8'))
    return base_scrap

    
#Main crawler function. Implements a Breadth First Search but with limited depth over the 
#search space.
def crawl(result_list,unseen_list,seen_list,crawl_depth,seed_url,increaseDepth, depthCountdown, new_list):
    
    #Halt at given depth
    if crawl_depth == halt_limit:
        print "Halting condition reached....."
        print "Halting at depth :"+str(halt_limit)
        
        #Get final statistics 
        result_list = list(set(seen_list+unseen_list))
        
        #Total number of crawled links
        links_crawled = len(result_list)
        matched_links = len(list(new_list))

        #Create an output file
        result_file = open("Crawled_Links.txt","w")
        result_file.write("-----------   Summary of All Crawled "+str(links_crawled)+" Links"+"-----------"+"\n")
        for link in range(len(result_list)):
            result_file.write(str(link+1)+"  "+result_list[link]+"\n")

        #Create an output file
        result_file = open("Focus_Crawl.txt","w")
        result_file.write("----------    Summary of Links with Keyphrase "+str(links_crawled)+" Links"+"----------"+"\n")
        for link in range(len(new_list)):
            result_file.write(str(link+1)+"  "+new_list[link]+"\n")
            
        return 
    
    
    #Condition variable to control depth movement
    if increaseDepth == True:
        depthCountdown = len(unseen_list)
        increaseDepth = False

    #Respect robots.txt Delay for 1 second
    time.sleep(1)
    
    #Request the page to explore
    response = urllib2.urlopen(seed_url)
    print "Processing URL....   "+seed_url

    page = response.read()
    response.close()
    soup = BeautifulSoup(page)
    #Page has been explored, add it to seen list
    seen_list.append(seed_url)
    

    #Function to scrap text off the web page
    base_scrap = scrap_page(soup)
    
    #Flag to see if we have a match in base text in focused crawling mode
    flag = False

    #Generate the keyphrase to be matched
    text_to_search = re.compile("\\b"+keyphrase+"\\b",re.IGNORECASE)


    #Search for the keyword only if keyphrase is not an empty string
    #Thus below check is skipped for unfocussed crawl.

    
    if re.search(text_to_search, base_scrap) != None:   
        #If true, we have a match during focused crawling.
        #print "Keyword Found"
        
        #This list has all urls that has keyword
        new_list.append(seed_url)
        flag = True
    else:
        #print"\n"
        #print "The current "+seed_url+" doesn't have a keyword !!"
        flag = False                        

    if flag:
    #We are in focus crawling    
    #Explore the children of current URL  
        for link in soup.find_all('a'):
            #print "childs are"
            #print len(soup.find_all('a'))
            new_link = link.get('href')
            #Construct child URL
            fullurl = urlparse.urljoin(seed_url, new_link)
                   
            #Condition check as given in the problem statement:
            is_url_valid = validate_url(fullurl, seen_list, unseen_list)
                                    
            if is_url_valid and ':' not in new_link:
                #Check for canonicals 
		#print fullurl
                final_url = check_canonical(fullurl)
		            
                if str(fullurl) != str(final_url):
                    fullurl = final_url
                    if fullurl not in seen_list and fullurl not in unseen_list:
                        unseen_list.append(fullurl)
                else:
                    #No canonicals for this url
                    unseen_list.append(fullurl)


    #Pop the next URL from queue to process.    
    next_url_to_process = unseen_list.pop(0)
    print "Next URL to process is :" + next_url_to_process
    
    #Check and adjust the depth variables
    depthCountdown = depthCountdown -1
    if depthCountdown == 0:
        crawl_depth = crawl_depth + 1
        increaseDepth = True
    
    #Debug print messages.
    current_seen_list_length = str(len(seen_list))
    current_unseen_list_length = str(len(list(unseen_list)))
    current_new_list_length = str(len(list(new_list)))

    print "Number of URL seen are: "+current_seen_list_length
    print "Number of URL yet to be explored are: " + current_unseen_list_length

    if keyphrase != "":
        print "Number of links with keyphrase is: " + current_new_list_length

    #This variable helps us to know how much time left for program to halt
    if depthCountdown > 1:    
        print "Count down to complete traversing current level is :  "+str(depthCountdown)
    
    #Recursive call to the function.
    crawl(result_list,unseen_list, seen_list, crawl_depth, next_url_to_process, increaseDepth, depthCountdown, new_list)
                    

#Call main crawling function only if seed url is there
if len(sys.argv) >= 2:   
    crawl(result_list,unseen_list,seen_list,start_depth,baseURL,False,1,new_list)
        
