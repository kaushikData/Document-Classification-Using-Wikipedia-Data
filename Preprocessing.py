import requests
import os
import random


class Preprocess:

    def __init__(self, origin_category = "Category:Main topic classifications", num_of_articles = 0, folder = "Preprocess"):


        self.origin_category = origin_category
        self.num_of_articles = num_of_articles

        self.URL = "https://en.wikipedia.org/w/api.php"
        self.index = {}


        self.basepath = "../"+ folder
        self.datapath = self.basepath +"/"+str(num_of_articles)
        self.rawpath = self.datapath + "/rawdata"
        self.plainpath = self.datapath + "/plaindata"

        
    def get_titles(self, category):
        

        PARAMS = {
            'action': "query",
            'list': "categorymembers",
            'cmtitle': category,
            'cmlimit': 200, # limits results to a maximum number
            'cmnamespace':0, 	#-> plain articles belonging to that category
            'format': "json"
        }
        S = requests.Session()
        R = S.get(url=self.URL, params=PARAMS)
        DATA = R.json()

        titles = []

        for article in DATA['query']['categorymembers']:
            titles.append(article['title'])

        return titles

    def get_subcategories(self, category):
        '''
        yields all subcategories inside that category
        '''
        PARAMS = {
            'action': "query",
            'list': "categorymembers",
            'cmtitle': category,
            'cmlimit': 200,
            'cmnamespace':14, #--> subcategories
            'format': "json"
        }
        S = requests.Session()
        R = S.get(url=self.URL, params=PARAMS)
        DATA = R.json()

        subcategories = []

        for article in DATA['query']['categorymembers']:
            subcategories.append(article['title'])

        return subcategories

    def get_dumptext(self, titles):
        '''
        gets text from article in titles, all titles in the same category
        '''

        PARAMS = {
            'action': 'query',
            'prop':'revisions',
            'rvprop':'content',
            'titles': "|".join(titles),
            'export':1,
            'exportnowrap':1,
            'format': "json"
            }
        S = requests.Session()
    return S.get(url=self.URL, params=PARAMS).text

    def write_rawdata(self, titles, category):
        '''
        writes all articles titles in a category into a single xml file
        '''
        category = category.split(":")[1]

        #check if Directory exists
        if not os.path.exists(self.basepath):
            os.mkdir(self.basepath)

        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)

        if not os.path.exists(self.rawpath):
            os.mkdir(self.rawpath)

        #write text to the file(s)
        print("writing files...")
        titles = [titles[x:x+50] for x in range(0, len(titles), 50)]
        for idx,t in enumerate(titles):

            filename = self.rawpath+"/"+category+"_"+str(self.num_of_articles)+"_"+str(idx)+".xml"
            with open(filename, 'w') as the_file:
                the_file.write(self.get_dumptext(t))

    def write_index(self, index,cat):
        '''
        index all articles titles in a category that were added to the baseline
        '''
        
        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)

        filename = self.datapath+"/"+cat+"_zz_index.json"
        with open(filename, 'w') as the_file:
            the_file.write(str(index))

    def get_rawdata(self):

        #get all 27 categories like arts, law, science and culture etc.
        main_categories = self.get_subcategories(self.origin_category)


        for cat in main_categories:
            print("looking for titles in category: {} ".format(cat))
            self.index[cat] = []

            for title in self.get_titles(cat):
                if not any(title in e for e in self.index.values()): #check for duplicates
                    self.index[cat].append(title)

            #get subcategories of one of 27 categories
            subcategories = self.get_subcategories(cat)

            for subcat in subcategories:
                for title2 in self.get_titles(subcat):
                    if not any(title2 in e for e in self.index.values()): #not allowing duplicates duplicates
                        self.index[cat].append(title2)

                if len(self.index[cat])<self.num_of_articles:
                    #get subsubcategories of one of the sub categories
                    subsubcategories = self.get_subcategories(subcat)
                    for subsubcat in subsubcategories:
                        for title3 in self.get_titles(subsubcat):
                            if not any(title3 in e for e in self.index.values()): #check for duplicates
                                self.index[cat].append(title3)

                        if len(self.index[cat])<self.num_of_articles:
                            # loop further to get more articles
                            subsubsubcategories = self.get_subcategories(subsubcat)
                            for subsubsubcat in subsubsubcategories:
                                for title4 in self.get_titles(subsubsubcat):
                                    if not any(title4 in e for e in self.index.values()): #check for duplicates
                                        self.index[cat].append(title4)

                            if len(self.index[cat])<self.num_of_articles:
                            # loop further to get more articles
                                subsubsubsubcategories = self.get_subcategories(subsubsubcat)
                                for subsubsubsubcat in subsubsubsubcategories:
                                    for title5 in self.get_titles(subsubsubsubcat):
                                        if not any(title5 in e for e in self.index.values()): #check for duplicates
                                            self.index[cat].append(title5)

            print("found {} titles in category: {} ".format(len(self.index[cat]), cat))

            #pick random articles, no title twice
            self.index[cat] = [self.index[cat][i] for i in random.sample(range(0, len(self.index[cat])-1), self.num_of_articles)]

            print(len(self.index[cat]))
            print("added {} unique titles to category: {} ".format(len(set(self.index[cat])), cat))

            #write articles in file
            self.write_rawdata((self.index[cat]),cat)
            #bookkeeping
            self.write_index(self.index[cat],cat)

    def convert_plain(self):
        '''
        Use WikiExtractor to get clear Text
        '''
        for file in os.listdir(self.rawpath):
            cat = file.split("_")[0]

            print("read document " + file)
            os.system("../wikiextractor/WikiExtractor.py "+self.rawpath+"/"+file+" -o "+self.plainpath+"/"+cat+"/"+file.split(".")[0]+" --json")

            
def main():

    # number of articles you want from each category - 11000
    num_of_articles = 11000
    
    #Data Folder to write files
    data_folder = "Data"
    
    # root category your are looking for - default:"Category:Main topic classifications"
    origin_category = "Category:Main topic classifications"

    BL = Preprocess(origin_category, num_of_articles, data_folder)
    BL.get_rawdata()
    BL.convert_plain()

if __name__== "__main__":
    main()