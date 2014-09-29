#########  CS600 HW1: A Focused Web Crawler  ###########

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

#Set recursion limit on the crawler.
sys.setrecursionlimit(2500)

#unseen_list is a List of URLs that are to be visited
unseen_list = []
#seen_list is a list of URLs that are visited
seen_list = []
#craw_depth is the halting measure of the crawling algorithm
craw_depth = 3
#is_keyphrase_present is a boolean to swtich between focused and unfocused crawling
is_keyphrase_present = False
#Sanity Check
is_input_url_present = False

#Final Crawled_List
result_list = []
#Base depth to start crawling
start_depth = 1

#Constant fot crawling depth 
halt_limit = 4

#Constant for Main Wiki Page
main_page = 'http://en.wikipedia.org/wiki/Main_Page'

#Constant for base englisht wiki page
base_page = 'http://en.wikipedia.org/wiki/'

#Input Seed URL. Taken as command line argument
baseURL = sys.argv[1]
if sys.argv[1] != None:
    #This boolean helps in switching mode later on
    is_input_url_present = True
    

#Check if optional second argument is present or not.
if len(sys.argv) < 2:
    #This boolean helps in switching mode later on
    is_keyphrase_present = False
else:
    is_keyphrase_present = False
    
if is_keyphrase_present:
    keyphrase = sys.argv[2]
else:
    keyphrase = ""
    
    
#Function to check for Canonical URLS
def check_canonical(url):
    #Request page
    print "In canonical function|n"
    print url
    request = urllib2.urlopen(url)
    
    #Read the page contents and store them
    response = request.read()
    
    #Parse the contents of web page
    soup = BeautifulSoup(response)
    
    #Final all link tages with canonical attribute
    #links = soup.findAll('link', attrs={"rel":"canonical"})
    links = soup.findAll('link')
    
    #Check if we are inputted with a canonical URL
    for link in links:
        if "canonical"  in str(link.get('rel')):
            #print link
            print "Canonical is....."
            print link.get('href')
            return link.get('href')
    return url
    

#Main crawler function. Implements a Breadth First Search but with limited depth over the 
#search space.
def crawl(result_list,unseen_list,seen_list,crawl_depth,seed_url,increaseDepth, depthCountdown):
    
    #Halt at given depth
    if crawl_depth == halt_limit:
        
        #Get final statistics 
        result_list = seen_list+unseen_list
        #Total number of crawled links
        links_crawled = len(result_list)
        #print result_list
        #print links_crawled
        
        #Create an output file
        result_file = open("Crawled_Links.txt","w")
        result_file.write("----------------Summary of Crawled "+str(links_crawled)+" Links"+"----------------"+"\n")
        for link in range(len(result_list)):
            #print result_list[link]
            result_file.write(str(link+1)+"  "+result_list[link]+"\n")
            
        return 
    
    
    
    #Condition variable to control depth movement
    if increaseDepth == True:
        depthCountdown = len(unseen_list)
        increaseDepth = False

    #Respect robots.txt Delay for 1 second
    #time.sleep(1)
    
    #Request the page to explore
    response = urllib2.urlopen(seed_url)
    #print "Fetching URL...."+final_url
    page = response.read()
    response.close()
    soup = BeautifulSoup(page)
   
    #Scrap text from web page for focus crawling mode
    base = soup.find_all(text = re.compile("\\b"+keyphrase+"\\b",re.IGNORECASE))        

    #Flag to see if we have a match in base text in focused crawling mode
    flag = False
    for i in range(len(base)):
        if re.search(keyphrase, base[i], re.IGNORECASE) is not None:
            flag = True
            break
        else:
            flag = False
                        
    #If true, we have a match during focused crawling.
    if flag:
        #Add URL to seen list to avoid cycles.
        seen_list.append(seed_url)    
        
        #Explore the children of current URL
        for link in soup.find_all('a'):
            new_link = link.get('href')
            fullurl = urlparse.urljoin(seed_url, new_link)
            
            
                   
            #Condition check as given in the problem statement:
            
            if '#' not in fullurl:
                
                #URL should not be same as Main wiki page
                constraintOne = fullurl != main_page
                
                #URL should not start with English wiki articles
                constraintTwo = fullurl.startswith(base_page)
                
                #URL should not already be visited. Else we have cycles
                constraintThree = fullurl not in seen_list
                
                #URL should be in unseen_list
                constraintFour = fullurl not in unseen_list
                
                if constraintOne and constraintTwo and constraintThree and constraintFour and ':' not in new_link:
                    sec_url =  check_canonical(fullurl)            
		    if str(fullurl) != str(sec_url):
		    #final_url = sec_url
		    #else:
		        print sec_url
		        print fullurl
		        fullurl = sec_url
			
		if fullurl not in seen_list and fullurl not in unseen_list:
		    unseen_list.append(fullurl)
		
            
            else:
                main_Url = fullurl.partition('#')[0]
                #print main_Url
                #URL should not be same as Main wiki page    
                constraintOneHashLink = main_Url != main_page
                
                #URL should not start with English wiki artices
                constraintTwoHashLink = main_Url.startswith(base_page)
                
                #URL should not already be visited. Else we have cycles
                constraintThreeHashLink = main_Url not in seen_list
                
                #URL should be in unseen_list
                constraintFourHashLink = main_Url not in unseen_list
                   
                if constraintOneHashLink and constraintTwoHashLink and constraintThreeHashLink and constraintFourHashLink and ':' not in new_link: 
		    sec_url =  check_canonical(main_Url)            
		    if str(main_Url) != str(sec_url):
		        #final_url = sec_url
		        #else:
			print sec_url
			print main_Url
			main_Url = sec_url
			
		    if main_Url not in seen_list and main_Url not in unseen_list:
		        unseen_list.append(main_Url)
		
    
    #Pop the next URL from queue to process.    
    absolute_link = unseen_list.pop(0)
    
    #Check and control the depth variables
    depthCountdown = depthCountdown -1
    if depthCountdown == 0:
        crawl_depth = crawl_depth + 1
        increaseDepth = True
    
    #Debug print messages.
    curren_seen_list_length = str(len(seen_list))
    curren_unseen_list_length = str(len(list(unseen_list)))
    
    print "Seen List length is: "+curren_seen_list_length
    print "Unseen List length is: " + curren_unseen_list_length
    print depthCountdown
    
    #Recursive call to the function.
    crawl(result_list,unseen_list, seen_list, crawl_depth, absolute_link, increaseDepth, depthCountdown)
                    

if __name__ == "__main__":
    #Sanity Checks
    if not(is_input_url_present):
        print "Enter Seed URL to proceed"
        print "Input Seed URL is: "+baseURL
    #Call crawling algorithm
    crawl(result_list,unseen_list,seen_list,start_depth,baseURL,False,1)
    
        
        
