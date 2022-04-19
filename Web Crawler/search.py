import searchdata
import math
import matmult
def search(phrase, boost):
    phrase = phrase.lower() #just in case thee users hand slips
    terms = phrase.split()
    #now to celculate the cosine similarity and the vector space model
    #first lets get the qurrey vector beacuse that only needs to be computed once
    fList = [] #the list that will need to be sorted at the end to producde the ranked results
    qVect = [] #for ther qurry vector
    uTerms = [] #for keeping track of unique terms in case of duplicites
    for z in terms: #creates list of unique terms, perserving index order
        if z not in uTerms:
            uTerms.append(z)
    for term in uTerms:
        idf = searchdata.get_idf(term)
        tf = terms.count(term)/len(terms) #returns the tf for the word in the qurry
        qVect.append(math.log((1+tf), 2) * idf)
    #now we have have the query vector
    #now we get the vector for the pages and list, sort, and rank them
    sites = open("sites.txt","r")
    lines = sites.readlines()
    sites.close()
    for line in lines:
        dVect = []
        url = line.split("||")[2].replace("\n", "") #gives us the url
        for term in uTerms:
            dVect.append(searchdata.get_tf_idf(url,term))
        #we now have the vector for the page
        #now we celculate the cosine simularity for this page
        numerator = 0
        #could also use euclidain distence with a list of 0s but thats a waste of space
        for i in range(len(qVect)):
            numerator += (qVect[i]*dVect[i])
        left = (matmult.euclidean_norm(qVect))
        right = (matmult.euclidean_norm(dVect))
        if right != 0:
            contentScore = numerator/(left*right)
        else: #to prevent division by 0 errors
            contentScore = 0
        #we now have the cosine simularity for the document
        if boost: #if we are asked to incorperate pagerank then we do so
            contentScore *= searchdata.get_page_rank(url)
        dictToAdd = { "url" : url,
                        "title" : url.split("/")[5].replace(".html", ""),
                        "score" : contentScore                                                    }
        fList.append(dictToAdd)
    #at this point we now have our list of dicts of websites and their content scores

    fList = sorted(fList, key=lambda score: float(score["score"]), reverse = True) #returns the dicts in decending order of score
    return fList[:10] #returns the first 10 eliments of the list






