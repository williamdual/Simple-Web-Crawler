import webdev
import os
import matmult
import math
sites = []
ranSites = [] #keeps a list of all sites that have been run
absolute = ""
ender = ""
pageIndex = 0 #is used to give a page an index
savedByTitle = {} #key will be N-0 (title) eliment will be its index (0)
savedByIndex = {} #key will be index (0) eliment will be its tittle (N-0)

totalSavedByFruit = {} #key is the word (apple) eliment is its frequency (2)
totalFruitsByName = [] #keeps track of all unique fruits

pagesFruitDicts = {} #dict of dicts that contaion ints key is N-0 then the next key is apple then the eliment is frequecy (2)
pagesFruitLists = {} #dict of lists, key is the title (n-0) eliment is a list of all unique fruits
pagesWordCounts = {} #dict of ints, key is the title, eliment is the word count
fruitFrquency = {} #key is the fruit (apple) eliment is the amount of pages it apears in 

pathway = {} #key is the page index, eliments are the outgoing links (N-0)
incoming = {} #key is the URL <- without the .html, eliments are the incoming links (N-0)
folder = "uniques"
def crawl(seed):
    #this is where we put all of the created files 
    if os.path.exists("sites.txt"): #deletes then creates the site.txt file
        os.remove("sites.txt")
    if os.path.exists("sitesOut.txt"):
        os.remove("sitesOut.txt")
    if os.path.isdir(folder):
        files = os.listdir(folder)
        for file in files:
            os.remove(os.path.join(folder, file))
        os.rmdir(folder)
    os.makedirs(folder)

    global sites 
    global absolute
    global savedByTitle
    global savedByIndex 
    sites = [seed]

    
    analize(seed, True) #now we have a list of seed sites, the absalute link and the all of the files
    ranSites.append(sites.pop(0))
    #for going to each linked site and then its linked site and then... until there is a list of all sites
    siteIndex = 0 #replaces the counter in a for loop
    while len(sites) > 0: #will run till all sites have been searched
        analize(sites[0], False)
        ranSites.append(sites.pop(0))
        siteIndex += 1
    numOfPages = len(ranSites)
    #now we have a 2d list with all indexes and titles, 
    ajayMatrix = []
    tempMatrix = []   
    for i in range(len(ranSites)):
        tempMatrix=[]
        for h in range(len(ranSites)):
            tempMatrix.append(0)
        for j in range(len(pathway[i])):
            tempMatrix[savedByTitle[pathway[i][j]]] = 0.5
        ajayMatrix.append(tempMatrix)
    #now we have our matrix, we need to change corisponding eliments that are both 0.5 to 1.0
    for k in range(len(ajayMatrix)):
        for l in range(len(ajayMatrix[k])):
            if ajayMatrix[k][l] == 0.5 and ajayMatrix[l][k] == 0.5:
                ajayMatrix[k][l] = 1
                ajayMatrix[l][k] = 1
    set_outgoing_linkss()
    set_incoming_linkss()
    set_page_ranks(ajayMatrix)
    set_idfs()
    set_tfs()    
    return numOfPages

def analize(seed, firstTime): #this will only be run once per unique page
    global pageIndex  
    global pathway 
    dictList = []
    global savedByTitle 
    global savedByIndex 
    global pagesFruitDicts
    global pagesFruitLists

    #txt files
    if firstTime: #if first run open files
        sitesF = open("sites.txt", "w")
    else: #if its not the first time simply append them
        sitesF = open("sites.txt", "a")

    savedByFruit = {} #key is the word (apple) eliment is its frequency (2)
    fruitsByName = [] #keeps track of all unique fruits
    stopFruit = 10000
    fruitLine = 0
    fruits = ""

    global sites
    global totalSavedByFruit
    global totalFruitsByName

    contents = webdev.read_url(seed)
    
    global absolute
    global ender
    if firstTime:   
        tempAbs = seed.split("/") #intermidiate value to split the link by / (must use / beacuse we cant asume link follows N-0 notation)     
        absolute = (seed.replace(tempAbs[-1], ""))[:-1] #this leaves us with the absolute url
        ender = "."+(tempAbs[-1].split("."))[-1]
    counter = 0
    for line in contents:
        #for the title and page stuff
        if "<title>" in line: #if its the title, save the title and asign it an index
            title = line.replace("<title>", "").replace("</title>","").replace("<html>","").replace("<head>","").replace("</head>","").replace("<body>","").replace("<p>","").replace(" ","")
            savedByTitle[title] = pageIndex
            savedByIndex[pageIndex] = title       
            sitesF.write(str(pageIndex)+"||"+title+"||"+seed+"\n") #saves the pages index, title, and url            
        #for the fruits stuff  
        if "<p>" in line: #if line contains the tag <p> then the next line will contain all of the fruits
            fruitLine = counter+1
        if fruitLine <= counter and counter < stopFruit: 
            fruits = fruits + " " + line
        if "</p>" in line: #means the fruit counting is done
            totalFruits = 0
            stopFruit = counter
            if " " in fruits: #if fruits are seperated by space charecters
                fruitList = fruits.split(" ") #then split it by the space charecter
            else: #if fruits are seperated by new line
                fruitList = fruits.split("\n")
            #removes both the leading null space and trailing end of paragraph charecter
            fruitList.pop(0)
            fruitList.pop(-1)
            pagesWordCounts[title] = len(fruitList)
            for fruit in fruitList: #runs through each word
                if fruit not in fruitsByName and fruit != "</p>":
                    savedByFruit[fruit] = 1
                    fruitsByName.append(fruit)
                    if fruit not in fruitFrquency:
                        fruitFrquency[fruit] = 1
                    else:
                        fruitFrquency[fruit] += 1
                    if fruit not in totalSavedByFruit: #keeps track of all words
                        totalSavedByFruit[fruit] = 1
                        totalFruitsByName.append(fruit)
                    else:
                        totalSavedByFruit[fruit] += 1
                else:
                    savedByFruit[fruit] += 1          
                    totalSavedByFruit[fruit] += 1        
            for i in range(len(fruitsByName)):
                totalFruits += savedByFruit[fruitsByName[i]]
        #for keeping track of the seed sites
        if "<a href=" in line:
            tempUrl = line.replace('<a href=".', '') #this removes everything before the link
            tempUrlElectricBogalo = tempUrl.split('"')
            tempUrl = tempUrlElectricBogalo[0] #this removes everything after the link\
            dictList.append(tempUrl.replace("/", "").replace(".html", "")) #adds the outgoing link to a list
            tempUrl = absolute+tempUrl #turns it into a compleate link
            if tempUrl not in incoming: #if the url is not already in the incoming links
                incoming[tempUrl] = [seed]
            else: #if its already in then add the curent site to its list
                incoming[tempUrl].append(seed)
            if tempUrl not in sites and tempUrl not in ranSites: #if the url is not already saved, add it to the list of sites
                sites.append(tempUrl)
        counter += 1
    pathway[pageIndex] = dictList
    pagesFruitDicts[title] = savedByFruit
    pagesFruitLists[title] = fruitsByName
    sitesF.close()
    pageIndex += 1


def set_outgoing_linkss():
    global savedByIndex
    global pathway
    global pageIndex
    curLink = ""#to keep track fo the current link
    for page in range(pageIndex):
        address = os.path.join(folder, savedByIndex[page]+".txt")
        if os.path.exists(address):
            os.remove(address)
        #the outgoing links will take up the first line
        f = open(address, "w")
        for link in pathway[page]:
            #simply write all of the outgoing links
            curLink = absolute+"/"+link+ender
            f.write(curLink+" ")
        f.write("\n")
        f.close()
        #now we repet for all outgoing links
        

def set_incoming_linkss():
    global savedByIndex
    global incoming
    global pageIndex
    curLink = ""
    for page in range(pageIndex):
        address = os.path.join(folder, savedByIndex[page]+".txt")
        #the imcoming links will tkae up the second line
        f = open(address, "a")
        for link in incoming[absolute+"/"+savedByIndex[page]+ender]:
            curLink = link
            f.write(curLink+" ")
        f.write("\n")
        f.close()



def set_page_ranks(baseMatrix):
    #saves each pages page rank value as the thired line in the corasponding txt file
    numOfPages = pageIndex
    numOfOnes = 0
    adMatrix = []
    alpha = 0.1 #a good const to have
    for vector in baseMatrix:
        holder = vector
        for i in range(len(holder)):
            if holder[i] > 0: #nessisary for allZero detection, as well as converting 0.5s into 1s, and sotreing the amount of 1s
                allZeros = False
                numOfOnes += 1
                holder[i] = 1
        #at this point we now have a row of 0s andor 1s      
        for j in range(len(holder)):
            if allZeros:
                holder[j] = 1/numOfPages
            elif holder[j] == 1:
                holder[j] = 1/numOfOnes
            holder[j] = holder[j]*(1-alpha)
            holder[j] = holder[j]+(alpha/numOfPages)
        numOfOnes = 0
        adMatrix.append(holder)
    #at this point all 0 rows have been divided by 1/N, and all 1 eliments have been divied by numOfOnes in row, multiplied by 1-alpha, and have been added to the matrix
    #we have our correct matrix at this point 
    piVect = []
    for i in range(len(adMatrix[0])):
        piVect.append(1/numOfPages)#this feels like the most time efiecent method
    #we now have our pi starting value
    tLast = piVect
    piVect = matmult.mult_matrix(adMatrix, piVect)
    while matmult.euclidean_dist(tLast,piVect) > 0.0001: #continualy multiplys the vector and matrix together until the euclidian distence is < or = to 0.0001
        tLast= piVect
        piVect = matmult.mult_matrix(adMatrix, piVect)
    #by this point we now have our final page vector so we save each page rank value to each txt file
    for page in range(pageIndex):
        address = os.path.join(folder, savedByIndex[page]+".txt")
        #the page rank value will take up the thired line
        f = open(address, "a")
        f.write(str(piVect[page])+"\n")
        f.close()

def set_idfs():
    for fruit in totalFruitsByName: #iterate through all fruits
        address = os.path.join(folder, fruit+".txt")
        if os.path.exists(address):
            os.remove(address)
        f = open(address, "w")
        f.write(str(math.log(pageIndex/(1+fruitFrquency[fruit]), 2)))
        f.close()
    

def set_tfs(): #will store these as individual txt files following format title-fruit (n-0-apple)
    for page in range(pageIndex): #iterate through all pages
        title = savedByIndex[page]
        wordCount = pagesWordCounts[title] #total amount of words in the page
        for fruit in pagesFruitLists[title]: #iterate through all unique fruits on that page
            fruitCount = pagesFruitDicts[title][fruit]#num of times a fruit apears in the page
            address = os.path.join(folder, title+"-"+fruit+".txt")
            f = open(address, "w")
            f.write(str(fruitCount/wordCount))
            f.close()

