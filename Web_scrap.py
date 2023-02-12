#!/usr/bin/env python
# coding: utf-8

# In[38]:


#pip install bs4
#pip install requests


# In[16]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk import *
from nltk.tokenize import sent_tokenize, word_tokenize
import string


# In[14]:


df= pd.read_excel("Input.xlsx")
print(df)
rm=df['URL']
rd=df['URL_ID']


# In[4]:


#df['Titles']= rm
for index, url in enumerate(rm,rd[0]): #since our url_id starts with 37, we started enumerate at 37
    text1=[]  #declare variable
    name1=[]
    #After long try, i found out that server expects theUser-Agent header. 
    #Interestingly, it is happy with any User-Agent, even any fictional:
    #also you can try using fake-useragent package  
    reqs1 = requests.get(url, headers = {'User-Agent': 'My User Agent 1.0'})#using request module
    reqs2 = requests.get(url, headers = {'User-Agent': 'My User Agent 1.0'}) #refered from stackoverflow
    reqs3 = requests.get(url, headers = {'User-Agent': 'My User Agent 1.0'})
    
    soup1 = BeautifulSoup(reqs1.text, 'html.parser') #using the BeautifulSoup module
    soup2 = BeautifulSoup(reqs2.text, 'html.parser')
    soup3 = BeautifulSoup(reqs3.text, 'html.parser')
    for a in soup1.findAll('div',attrs={"class":"td-parallax-header"}): #inspecting the website to get the required output(title)
        for b in soup2.findAll('div',attrs={"class":"td-post-content"}): #Article on website
            for c in soup3.findAll('p'): #required article on website
                text = c.get_text()  #article
                text1.append(text)  # (''.join(map(str,text))) can be used directly to convert list to string
                
        name = a.find('h1',attrs={"class":"entry-title"}) #title 
        name=name.get_text()
        name1.append(name)
   #save name and its article in different files (as requirement)    
    with open(f"folfol/{index}.txt", "w" , encoding='utf-8') as file: #mandatory to give encoding otherwise error
        file.write(str(name1))
        file.write('\n') 
        file.write(str(text1))
    text1.clear()  #to start with new iteration, the previous elements in list must be remove
    name1.clear()


# In[24]:


URL=list(rm)
URL_ID=list(rd)
positive=[]
negative=[]
polarity=[]
subjectivity=[]
AvgWordPerSent=[]
word_count=[]

for index in range(37,151):             
    with open(f"folfol/{index}.txt", "r" , encoding='utf-8') as file:
        f_content = file.read().lower()   #read and convert text to lower
        f_content=f_content.replace("[","") 
        f_content=f_content.replace("]","")
        f_content=f_content.replace('“',"")
        
        tokens = nltk.word_tokenize(f_content) #tokenize words
        #print(tokens)
        #print("total words before cleaning",len(tokens))
        
        with open('folfol/StopWords/StopWords_GenericLong.txt','r') as f2, open('folfol/StopWords/StopWords_Currencies.txt','r') as f3, open('folfol/StopWords/StopWords_DatesandNumbers.txt','r') as f4, open('folfol/StopWords/StopWords_Generic.txt','r') as f5 , open('folfol/StopWords/StopWords_Geographic.txt','r') as f6 , open('folfol/StopWords/StopWords_Names.txt','r') as f7:
        #opening all Stopwords files
            f2content = f2.read().lower()
            f2content= f2content.split()
            #print(f2content)
            
            f3content = f3.read().lower()
            f3content= f3content.split()
            #print(f3content)
            
            f4content = f4.read().lower()
            f4content= f4content.split()
            #print(f4content)
            
            f5content = f5.read().lower()
            f5content= f5content.split()
            #print(f5content)
            
            f6content = f6.read().lower()
            f6content= f6content.split()
            #print(f6content)
            
            f7content = f7.read().lower()
            f7content=f7content.replace("Surnames from 1990 census > .002%.  www.census.gov.genealogy/names/dist.all.last","")
            f7content= f7content.split()
            #print(f7content)
            
            #checking stopwords whether present in file
            clean_words = [x for x in tokens if x not in f2content ]
            #print(len(clean_words))

            clean_words = [x for x in clean_words if x not in f3content ]
            #print(clean_words)
            #print(len(clean_words))
            
            clean_words = [x for x in clean_words if x not in f3content ]
            #print(len(clean_words))
            
            clean_words = [x for x in clean_words if x not in f4content ]
            #print(len(clean_words))
            
            clean_words = [x for x in clean_words if x not in f5content ]
            #print(clean_words)
            #print(len(clean_words))
            
            clean_words = [x for x in clean_words if x not in f6content ]
            #print(len(clean_words))
            
            clean_words = [x for x in clean_words if x not in f7content ]
            clean_len= len(clean_words)
            ##print("words after clearning",clean_len)
            #print(clean_words)            #AFTER REMOVING STOPWORDS FROM TEXT
            
            #converting to string to calculate number of sentences
            sent=' '.join(clean_words)
            #print(sent)
            clean_sent = re.compile('[.!?]').split(sent)
            clean_sen_len=len(clean_sent)
            #print(clean_sen_len)
            
            
            #calculate word count
            send1=sent.translate(str.maketrans('', '', string.punctuation))
            word_cnt=len(send1.split())
            #print(send1)
            #print(word_cnt)
            word_count.append(word_cnt)

            
            
            #removed_text = [y for y in tokens if y in f7content] #just to check what is removed
            #print(removed_text)
            
            #opening file with positive and negativw words
            with open('folfol/MasterDictionary/negative-words.txt','r') as n1 , open('folfol/MasterDictionary/positive-words.txt','r') as p1:
                neg_words=n1.read()
                neg_words=neg_words.split()
                #print(neg_words)

                
                pos_words=p1.read()
                #pos_words=pos_words.split()
                #print(pos_words)

                #negative score
                neg_dict=[z for z in clean_words if z in neg_words]
                #print(neg_dict))
                neg_len=len(neg_dict)
                #print(neg_len)
                negative.append(neg_len)
                
                #positive score
                pos_dict=[z for z in clean_words if z in pos_words]
                #print(pos_dict)
                pos_len=len(pos_dict)
                #print(pos_len)
                positive.append(pos_len)
                
                #polarity score
                pol_score = (pos_len - neg_len)/ ((pos_len + neg_len) + 0.000001)
                polarity.append(pol_score)
                
                #subjectivity score
                sub_score=(pos_len + neg_len)/ ((clean_len) + 0.000001)
                subjectivity.append(sub_score)
                
                #average word per sentence
                AvgWPerSent = (clean_len / clean_sen_len)
                AvgWordPerSent.append(AvgWPerSent)
                
#SAVING OUTPUT TO EXCEL FILE:
df = pd.DataFrame({'URL':URL,'URL_ID':URL_ID,'POSITIVE SCORE':positive,'NEGATIVE SCORE':negative,'POLARITY SCORE':polarity,'SUBJECTIVITY SCORE':subjectivity,'AVG WORD PER SENT':AvgWordPerSent,'WORD COUNT':word_count})
df.to_excel('Output.xlsx', index=False, encoding='utf-8')


# In[ ]:




