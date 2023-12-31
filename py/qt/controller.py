from ipdb import set_trace as idebug

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt

from searchwidget import SearchWidget
import searchresult as sr
from viewform import ViewForm
from book import Book
from frmbase.flogger import log 

"""
#This is the master controller

TODO:

Homepage
    * Seach Box
        Search 
            * Name
                * Exact name match 
                * Name boundary match
                * String contains 
                * soundex 
            * Tags 
        * v1 should show two text boxes, eventually we can merge 
    * Searchbox showing search for all 
    * Button to create New user.
        * Opens the edit tab on a new idnum 
    
x SearchForm
    o Autocomplete
o SearchResults:
    x Search by tag 
    - Back Button
    x Scrollbar
    o Sort results alphabethically
o ViewForm
    - Back Button
    x Don't pop up, but appear in main dialog
    x Show relationships
    x Add links to relationships
    o Scrollbar for relationships
o Edit form 
    Needs to be written 
o Controller:
    x Needs a super-window that stays visible
o View Form
    o Scroll bar for relationships
    
"""

class EmptyWidget(QtWidget.QWidget):
    """Placeholder will I create some of the other forms"""
    def __init__(self, parent=None):
        QtWidget.QWidget.__init__(self, parent)
        

class MasterController(QtWidget.QDialog):
    def __init__(self, book:Book):
        QtWidget.QDialog.__init__(self, None)
        self.book = book
        
        #TODO, creating these needs to be a separated method 
        #than the new-contact form can signal
        nameCompleter = Qt.QCompleter(book.getNameList(), self)
        nameCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        tagCompleter = Qt.QCompleter(book.getTagList(), self)
        tagCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.searchForm = SearchWidget(nameCompleter, tagCompleter, self)
        self.searchForm.nameSearchRequested.connect(self.searchByName)
        self.searchForm.tagSearchRequested.connect(self.searchByTag)
        
        self.searchResultForm = sr.SearchResultLister(self)
        self.searchResultForm.personSelectedEvent.connect(self.viewPerson)
        self.searchResultForm.tagSelectedEvent.connect(self.searchByTag)

        self.viewContactForm = ViewForm(book)
        self.viewContactForm.lookupIdRequested.connect(self.viewPerson)
        self.viewContactForm.searchByTagRequested.connect(self.searchByTag)
        self.viewContactForm.back.clicked.connect(self.viewContactForm.hide)
        self.viewContactForm.hide()
        
        layout = QtWidget.QVBoxLayout()
        layout.addWidget(self.searchForm)
        layout.addWidget(self.searchResultForm )
        #layout.addWidget(self.editContactForm)
        layout.addWidget(self.viewContactForm)
        
        self.setLayout(layout)
        #self.hideAll()
    
    def hideAll(self):
        pass
        #self.searchResultForm.setVisible(False)
        #self.searchForm.setVisible(False)
        #self.viewContactForm.setVisible(False)
        #self.editContactForm.setVisible(False)
        
        
    def showViewContactForm(self):
        self.hideAll()
        self.viewContactForm.setVisible(True)
        
    def showSearchForm(self):
        self.hideAll()
        self.searchForm.setVisible(True)
        
    def showSearchResultsForm(self):
        self.hideAll()
        #idebug()
        self.searchResultForm.setVisible(True)
       
    def searchByTag(self, tag:str):
        personList = self.book.searchByTag(tag)
        log.info(f"{len(personList)} results found")
        self.searchResultForm.clear()
        for person in personList:
            self.searchResultForm.add(person)
        self.showSearchResultsForm()
        self.searchForm.tagEdit.setText(tag)
        
    def searchByName(self, name:str):
        personList = self.book.searchByName(name)
        log.info(f"{len(personList)} results found")
        self.searchResultForm.clear()
        for person in personList:
            self.searchResultForm.add(person)
        self.showSearchResultsForm()

    def viewPerson(self, idnum):
        #idebug()
        log.info(f"idnum is {idnum}")
        person = self.book.getPerson(idnum)
        log.info(str(person) +  str(person.idnum))
        self.viewContactForm.displayPerson(person)
        self.showViewContactForm()
        


import pandas as pd
import numpy as np 
def load_book(fn):
 
    df = pd.read_csv(fn)
    df['idnum'] = df['idnum'].replace(np.nan, -1).astype(int)
    df['id1'] = df['id1'].replace(np.nan, -1).astype(int)
    tags = df[['tag1', 'tag2', 'tag3', 'tag4']].replace(np.nan, "")
    df['tags'] = tags.agg(','.join, axis=1)    
    df = df.replace(np.nan, "")
    
    namedf = df[['idnum', 'Name', 'about', 'tags']]
    reldf = df[['idnum', 'R1', 'id1']]
    reldf = reldf[ reldf.id1 > 0]
    reldf = reldf.rename( {'idnum': 'id1', 'R1':'connection', 'id1':'id2'}, axis=1)
    book = Book(namedf, reldf)
    #print(namedf)
    return book



def main():
    #import pandas as pd 
    #df = pd.read_csv("../names.csv")
    #df = df.fillna("")
    #df['tags'] = df.apply(lambda x: ",".join([x.tag1, x.tag2, x.tag3, x.tag4]), axis=1)
    ##df = df[:5]
    
    #relations = pd.DataFrame(columns = "id1 connection id2".split())
    #book = Book(df, relations)
    book = load_book("../../names.csv")

    controller = MasterController(book)
    controller.searchByName(name="")
    return controller
