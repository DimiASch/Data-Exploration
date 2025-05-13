'''
in the folder where the program is stored there are two text files one with methods and one with applications written in it 
there exist different function in the programm to chosse from, one functions collects the words that often appear in correspondence with the words in the first list 
another one the words that appear in correspondence with the second list and the third one alls words that appear with the different combinations of the first and the second list
it is important to keep the .txt tidy and to write every word into a new line for now the processing of sentences is not possible the only possibility is for two word combinations like banana apple 
There are some preliminary functions that are not of importence but keep the code a lot more readable
When the programm is run for the first time it is important to uncomment the three nltk.download in the import section so that the required packages are installed these may be commented out in 
later use to speed up the process
There is txt file called unwantedwords where the user can put in words they dont want to have in the sorting this is mainly used for fillerwords that  are not cought by the nltk stopwords'''

import json
import os
import nltk
from nltk.tokenize import word_tokenize
import re
import csv
import sys
import matplotlib
import pymupdf
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import sys
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')



def main():
    currentpath = os.path.dirname(os.path.abspath(__file__)) #this is the path to the current python file
    relativepath = r'../../data/cleaned'    #this is the relative path from this python 
    folderpath = os.path.normpath(os.path.join(currentpath,relativepath)+ os.path.sep) 
    dictlist,namelist = loadjson(folderpath)
    stop_words = set(stopwords.words('english'))
    stop_wordsgerman = set(stopwords.words('german'))
    unwantedwords = txt2list('ignoredwords.txt')
    totaldict = {}
    journalsplit() # used to create json
    mainhandling() # used to clean json
    ## section for simplewordcount
    if wordcountswingle.get():
        for i in range(len(namelist)):
            returndict = simplewordcount(dictlist[i],stop_words,stop_wordsgerman,unwantedwords)
            sortplot(returndict,namelist[i][:-5],50)
    
    ### section for counting appearances
    if Methodssingle.get():
        for dictionary in dictlist:
            totaldict.update(dictionary)
        resultdict = appearancecount(totaldict,'methods.txt',stop_words,stop_wordsgerman,unwantedwords)
        for namekey,dictvalue in resultdict.items():
            sortplot(dictvalue,namekey,50)
    
    if Applicationssingele.get():
        for dictionary in dictlist:
            totaldict.update(dictionary)
        resultdict = appearancecount(totaldict,'applications.txt',stop_words,stop_wordsgerman,unwantedwords)
        for namekey,dictvalue in resultdict.items():
            sortplot(dictvalue,namekey,50)

    ### section for combinations
    if methodsandappl.get():
        for dictionary in dictlist:
            totaldict.update(dictionary)
        resultdict = combinationcount(totaldict,'methods.txt','applications.txt',stop_words,stop_wordsgerman,unwantedwords)
        for namekey,dictvalue in resultdict.items():
            sortplot(dictvalue,namekey,50)

def getfilepaths(directory):# this functions returns the absolute paths to each file in a specified directory the directory has to be given as an absolute path 
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def txt2list(name): #this function converts the content of a txt file to  alist the name of the file has to be entered as a string like 'example.txt' and this only works for txt files
    file_path = getfilepath(name)
    with open(file_path, 'r') as file:
        listcontent = [line.strip() for line in file]
    return listcontent

def getfilepath(name): #this function returns the path to a specified file within the journal scraping folde the name has to be given as a string like 'example.txt' this works for every file type
    currentpath = os.path.dirname(os.path.abspath(__file__))
    relativepath = fr'../../'
    directory_path = os.path.abspath(os.path.join(currentpath,relativepath))
    for root, dirs, files in os.walk(directory_path):
        if name in files:
            file_path = os.path.join(root, name)
            return file_path

def checkforfile(name): # this function checks if a file is existing in the journal scraping folder
    currentpath = os.path.dirname(os.path.abspath(__file__))
    relativepath = fr'../../../JournalScraping/data' 
    directory_path = os.path.normpath(os.path.join(currentpath,relativepath)+ os.path.sep) 
    for root, dirs, files in os.walk(directory_path):
        if name in files:
            return True
    return False
        
def sortplot(givendict,diagramname,number): #this makes a histogramm plot out of  a given dictionary on the x axis the keys are plotted and on the y axis the values the the diagramm name has to be text and is displayes as name of the diagram the number specifies how many entries are plotted
    sorted_data = sorted(givendict.items(), key=lambda item: item[1], reverse=True)
    topdict = {k: v for k, v in sorted_data[:number]}
    currentpath = os.path.dirname(os.path.abspath(__file__))
    relativepath = fr'../../data/plots'
    directory_path = os.path.abspath(os.path.join(currentpath,relativepath))
    fullpath = os.path.abspath(os.path.join(directory_path,f'{diagramname}.png'))
    plt.figure(figsize=(19.2, 10.8))
    plt.bar(topdict.keys(),topdict.values()) 
    plt.xlabel('Keys')
    plt.ylabel('Number of appearances')
    plt.title(diagramname)
    plt.xticks(rotation=45)
    plt.savefig(fullpath, dpi=100)       

def loadjson(folderpath): # this function loads all json files in a specified folder and returns a list of dictionaries and also a list of the file names the folderpath is the path to the folder where the json are stored; no other files than .json should be stored in that folder
    filepaths = getfilepaths(folderpath)
    dictlist = []
    namelist = []
    for filepath in filepaths:
        namelist.append(os.path.basename(filepath))
        with open(filepath,'r') as file:
            dictlist.append(json.load(file))
    return dictlist,namelist

def simplewordcount(data_dict,stop_words,stop_wordsgerman,unwantedwords): #this function simply counts the number of words that appear in a specified json file and plots a histogramm of the most often appearing words
    countdict = {}
    counter = 0
    for text in data_dict.values():
        numberoflines = len(data_dict)
        maxnum = numberoflines
        if counter % 20 == 0:
            print(f'{counter}/{maxnum}')
        wordlist = word_tokenize(text.lower())
        for word in wordlist:
            if word not in stop_words and word not in stop_wordsgerman and word not in unwantedwords:
                if word in countdict:
                    countdict[word] += 1
                else:
                    countdict[word] = 1
        counter += 1
    return countdict

def appearancecount(datadict,nameoffile,stop_words,stop_wordsgerman,unwantedwords): # this function collects the often appearing words for each word in a given text file.
    complist = txt2list(nameoffile)
    counter = 0
    maxnum = len(datadict)
    resultdict = {}
    for text in datadict.values():
        wordlist = word_tokenize(text.lower())
        if counter % 20 == 0:
            print(f'{counter}/{maxnum}')
        counter += 1
        for checkword in complist:
            if checkword not in resultdict:
                resultdict[checkword] = {}

            sub_list = checkword.split()
            if any(wordlist[i:i + len(sub_list)] == sub_list for i in range(len(wordlist) - len(sub_list) + 1)):
                for singleword in wordlist:
                    if singleword not in stop_words and singleword not in stop_wordsgerman and singleword not in unwantedwords:
                        if singleword in resultdict[checkword]:
                            resultdict[checkword][singleword] += 1
                        else:
                            resultdict[checkword][singleword] = 1
    return resultdict

def combinationcount(datadict,nameoffile1,nameoffile2,stop_words,stop_wordsgerman,unwantedwords): # this function check for each combination of words in two given texfiles if they appear together in a single article and if this is the case the often appearing words are counted.
    list1 = txt2list(nameoffile1)
    list2 = txt2list(nameoffile2)
    counter = 0
    maxnum = len(datadict)
    resultdict = {}
    for text in datadict.values():
        wordlist = word_tokenize(text.lower())
        if counter % 20 == 0:
            print(f'{counter}/{maxnum}')
        counter += 1
        for firstword in list1:
            for secondword in list2:
                combword = firstword + ' ' + secondword
                if combword not in resultdict:
                    resultdict[combword] = {}
                
                if ' ' not in firstword and ' ' not in secondword:
                    if firstword in wordlist and secondword in wordlist:
                        for singleword in wordlist:
                            if singleword not in stop_words and singleword not in stop_wordsgerman and singleword not in unwantedwords:
                                if singleword in resultdict[combword]:
                                    resultdict[combword][singleword] += 1
                                else:
                                    resultdict[combword][singleword] = 1
                
                if ' ' in firstword and ' ' not in secondword:
                    first_sub_list = firstword.split()
                    if any(wordlist[i:i + len(first_sub_list)] == first_sub_list for i in range(len(wordlist) - len(first_sub_list) + 1)) and secondword in wordlist:
                        for singleword in wordlist:
                            if singleword not in stop_words and singleword not in stop_wordsgerman and singleword not in unwantedwords:
                                if singleword in resultdict[combword]:
                                    resultdict[combword][singleword] += 1
                                else:
                                    resultdict[combword][singleword] = 1
                
                if ' ' in secondword and ' ' not in firstword:
                    second_sub_list = secondword.split()
                    if any(wordlist[i:i + len(second_sub_list)] == second_sub_list for i in range(len(wordlist) - len(second_sub_list) + 1)) and firstword in wordlist:
                        for singleword in wordlist:
                            if singleword not in stop_words and singleword not in stop_wordsgerman and singleword not in unwantedwords:
                                if singleword in resultdict[combword]:
                                    resultdict[combword][singleword] += 1
                                else:
                                    resultdict[combword][singleword] = 1

                if ' ' in firstword and ' ' in secondword:
                    first_sub_list = firstword.split()
                    second_sub_list = secondword.split()
                    if any(wordlist[i:i + len(first_sub_list)] == first_sub_list for i in range(len(wordlist) - len(first_sub_list) + 1)) and any(wordlist[i:i + len(second_sub_list)] == second_sub_list for i in range(len(wordlist) - len(second_sub_list) + 1)):
                        for singleword in wordlist:
                            if singleword not in stop_words and singleword not in stop_wordsgerman and singleword not in unwantedwords:
                                if singleword in resultdict[combword]:
                                    resultdict[combword][singleword] += 1
                                else:
                                    resultdict[combword][singleword] = 1
    return resultdict

def filterhandling(s): # this defines the filter to standardise the json files and remove all unwanted characters and whitespaces
    replacements = {
    r'\u00c4': 'AE',  # Ä
    r'\u00e4': 'ae',  # ä
    r'\u00d6': 'OE',  # Ö
    r'\u00f6': 'oe',  # ö
    r'\u00dc': 'UE',  # Ü
    r'\u00fc': 'ue',  # ü
    r'\u00df': 'ss'   # ß
    }
    for pattern, replacement in replacements.items():
        s = re.sub(pattern, replacement, s)
    s = re.sub(r'\d+',' ',s)
    s = re.sub(r'\b\w\b', ' ', s)
    s = re.sub(r'\W+',' ',s)
    s = re.sub(r'\\\S*\s', ' ', s)    
    unwanted_word_list = []
    currentpath = os.path.dirname(os.path.abspath(__file__))
    filename = 'unwantedwords.txt'
    file_path = os.path.join(currentpath,filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        unwanted_word_list = [line.strip() for line in file]
    for word in unwanted_word_list:
        s = re.sub(fr'{word}','',s).strip()
    s = re.sub(r'\s+',' ',s)
    return s

def mainhandling(): # this is the main function for the text filtering
    dirnames = getdirshandling()
    currentpath = os.path.dirname(os.path.abspath(__file__))
    for name in dirnames:
        if not checkforfile(f'{name}cleaned.json'):
            relativepath = fr'../../data/{name}.json'
            filepath = getfilepathhandling(name)
            with open(filepath,'r', encoding='utf-8') as file:
                data = json.load(file)
            numberofarticles = len(data)
            counter = 0
            newdict = {}
            for key in data:
                newdict[key] = filterhandling(data[key])
                if counter % 100 == 0:
                    print(f'cleaned {counter}/{numberofarticles}')
                counter += 1
            relativepath = fr'../../data/cleaned/{name}cleaned.json'
            filepath = os.path.realpath(os.path.join(currentpath,relativepath))
            directorypath = os.path.dirname(filepath)
        
        # Create the directories if they do not exist
            if not os.path.exists(directorypath):
                os.makedirs(directorypath)
            with open(filepath,'w') as newfile:
                json.dump(newdict,newfile,indent = 4)

def getdirshandling(): # this function is modified to get all names of the directories in the articles folder
    currentpath = os.path.dirname(os.path.abspath(__file__)) #the folder where the articles should be stored
    relativepath = r'../../data/articles'
    folderpath = os.path.realpath(os.path.join(currentpath,relativepath)) + os.path.sep
    dir_paths = []
    dir_names = []
    if not os.path.exists(folderpath):
        sys.exit("An error occurred: The specified folder does not exist.")
    for root, dirs, files in os.walk(folderpath):
        for directory in dirs:
            if directory.lower() != 'cleaned':
                dir_paths.append(os.path.join(root, directory))
    for dirpath in dir_paths:
        dir_names.append(os.path.basename(os.path.normpath(dirpath)))
    return dir_names

def getfilepathhandling(name):# this function collects all json files in a specified folder
    currentpath = os.path.dirname(os.path.abspath(__file__))
    relativepath = fr'../../'
    directory_path = os.path.abspath(os.path.join(currentpath,relativepath))
    for root, dirs, files in os.walk(directory_path):
        if f'{name}.json' in files:
            file_path = os.path.join(root, f'{name}.json')
            return file_path

def getdirsgeneration(): # This function gets the name and path of every subfolder in the articles folder
    currentpath = os.path.dirname(os.path.abspath(__file__)) #the folder where the articles should be stored
    relativepath = r'../../data/articles'
    folderpath = os.path.realpath(os.path.join(currentpath,relativepath)) + os.path.sep
    dir_paths = []
    dir_names = []
    if not os.path.exists(folderpath):
        sys.exit("An error occurred: The specified folder does not exist.")
    for root, dirs, files in os.walk(folderpath):
        for directory in dirs:
            dir_paths.append(os.path.join(root, directory))
    for dirpath in dir_paths:
        dir_names.append(os.path.basename(os.path.normpath(dirpath)))
    return dir_names,dir_paths

def extractxml(path,datadict,counter,maxnum): # this function extracts the text of an xml file
    with open(path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
    article = soup.find('article')
    if article is not None:
        for tail in article.find_all('tail'):
            tail.decompose()
        article_text = article.get_text(separator=' ')
        datadict[os.path.basename(path)] = article_text 
    print(f'alivexml{counter}/{maxnum}')
    return datadict

def extractpdf(path,datadict,counter,maxnum): # this function extracts the text of an xml file
    pdf_document = pymupdf.open(path)
    totaltext = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        totaltext += text
    datadict[os.path.basename(path)] = totaltext   
    print(f'alivepdf{counter}/{maxnum}')
    return datadict

def journalsplit(): # this function generates a json out of every journal it also checks if this json already exist
    dir_names,dir_paths = getdirsgeneration() #if file does not exist create
    for name,path in zip(dir_names,dir_paths):
        counter = 0
        if not checkforfile(f'{name}.json'):
            datadict = {}
            file_path = getfilepaths(path)
            maxnum = len(file_path)
            for path in file_path:
                if path[-3:] == 'xml':
                    extractxml(path,datadict,counter,maxnum)
                    counter += 1
                elif path[-3:] == 'pdf': 
                    extractpdf(path,datadict,counter,maxnum)
                    counter += 1
                else:
                    sys.exit("An error occurred: The type of file has to be .xml or .pdf.")
            currentpath = os.path.dirname(os.path.abspath(__file__))
            relativepath = r'../../data/'
            filename = f'{name}.json'
            file_path_json = os.path.join(currentpath,relativepath,filename)
            with open(file_path_json, "w") as json_file:
                json.dump(datadict, json_file, indent=4)


#### UI section
#region
#Create the main window
root = tk.Tk()
root.title("Textanalysis")
root.geometry('800x600')
# Create a label
label = ttk.Label(root, text="Select your preferences:")
label.pack(pady=10)

# Create variables to store checkbox states
Methodssingle = tk.BooleanVar()
Applicationssingele = tk.BooleanVar()
methodsandappl = tk.BooleanVar()
wordcountswingle = tk.BooleanVar()
# Add checkboxes
checkbox1 = ttk.Checkbutton(root, text="Methods", variable=Methodssingle)
checkbox1.pack()

checkbox2 = ttk.Checkbutton(root, text="Applications", variable=Applicationssingele)
checkbox2.pack()

checkbox3 = ttk.Checkbutton(root, text="Methods & Applications", variable=methodsandappl)
checkbox3.pack()

checkbox4 = ttk.Checkbutton(root, text="Simple Wordcount", variable=wordcountswingle)
checkbox4.pack()
# Add a button to show selection
button = ttk.Button(root, text="Run analysis", command=main)
button.pack(pady=10)


# Label to display selected options
result_label = ttk.Label(root, text="")
result_label.pack()
# button to exit the program
exit_button = tk.Button(root, text="Exit Program", command=sys.exit)
exit_button.pack(pady=20)
# Run the application
root.mainloop()
#endregion