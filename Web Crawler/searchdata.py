import math
import os
folder = "uniques"
def get_outgoing_links(URL): #return None if link isnt found
    title = (URL.split("/"))[-1].replace(".html", "") #retrives the title from the link
    address = os.path.join(folder,title+".txt")
    if os.path.isfile(address):
        f = open(address, "r")
        lines = f.readline().split() #read the first line and seperate the links
        return lines
    else:
        return None

def get_incoming_links(URL): #return None if link isnt found
    title = (URL.split("/"))[-1].replace(".html", "") #retrives the title from the link
    address = os.path.join(folder,title+".txt")
    if os.path.isfile(address):
        f = open(address, "r")
        lines = f.readlines()[1].split() #read the second line and seperate the links
        return lines
    else:
        return None

def get_page_rank(URL): #make sure to return -1 if the url was not found
    title = (URL.split("/"))[-1].replace(".html", "") #retrives the title from the link
    address = os.path.join(folder,title+".txt")
    if os.path.isfile(address):
        f = open(address, "r")
        line = float(f.readlines()[2]) #read the thired line 
        return line
    else:
        return -1
        
def get_idf(word): #if word is not present return 0
    fruit = word.lower()
    address = os.path.join(folder,fruit+".txt")
    if os.path.isfile(address):
        f = open(address, "r")
        line = float(f.readline())
        return line
    else:
        return 0

def get_tf(URL, word): #if either Url is not found or the word is not in the given url then return 0
    title = (URL.split("/"))[-1].replace(".html", "") #retrives the title from the link
    fruit = word.lower()
    address = os.path.join(folder,title+"-"+fruit+".txt")
    if os.path.isfile(address):
        f = open(address, "r")
        line = float(f.readline())
        return line
    else:
        return 0

def get_tf_idf(Url, word):
    tf = get_tf(Url, word) #get the term frequency for the word
    idf = get_idf(word) #get the inverse document frequency for the word
    #now we celculate the tf-idf weight for the passed word
    return math.log((1+tf), 2) * idf
