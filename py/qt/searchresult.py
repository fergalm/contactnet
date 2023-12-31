from ipdb import set_trace as idebug

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
#import PyQt5.QtGui as QtGui

QtCore.Signal = QtCore.pyqtSignal

from frmbase.flogger import log 
from book import Person 
import pandas as pd 

class IndividualSearchResultWidget(QtWidget.QWidget):
    """Display an Individual search result for a single contact"""
    
    personSelectedEvent = QtCore.Signal('int')
    tagSelectedEvent = QtCore.Signal("QString")
    
    def __init__(self, parent, idnum, name:str, tags:list, notes:str):
        QtWidget.QWidget.__init__(self, parent)
        
        self.idnum = idnum
        self.name= QtWidget.QPushButton(name)
        self.name.setFlat(True)
        self.name.clicked.connect(self.handleNameClickEvent)
        font = self.name.font()
        font.setPointSize(24)
        self.name.setFont(font)
        self.name.setStyleSheet("QPushButton {text-align:left;}")

        tags = filter(lambda x: len(x) > 0, tags)
        self.tagBox = QtWidget.QHBoxLayout()
        self.createButtonsForTags(tags)
        self.notes = QtWidget.QLabel(notes)

        layout = QtWidget.QVBoxLayout()
        layout.addWidget(self.name)
        layout.addLayout(self.tagBox)
        layout.addWidget(self.notes)
        self.setLayout(layout)

    def createButtonsForTags(self, tagList):
        layout = self.tagBox 
        
        for tag in tagList:
            button = QtWidget.QPushButton('#' + tag)
            button.setFlat(True)
            button.setStyleSheet("QPushButton {color:blue;}")

            import functools 
            f = functools.partial(self.handleSearchByTagRequest, tag)
            button.clicked.connect(f)
            layout.addWidget(button)
     

    def handleNameClickEvent(self):
        """If the name is clicked, emit an event.
        
        TODO: Add a similar event for clicking on a tag
        """
        log.info(f"Idnum {self.idnum} was clicked")
        self.personSelectedEvent.emit(int(self.idnum))

    def handleSearchByTagRequest(self, tag:str):
        log.info(f"Tag '{tag}' on '{self.name.text()}' was clicked")
        self.tagSelectedEvent.emit(tag)
        

from widgetlister import WidgetLister
class SearchResultLister(WidgetLister):
    personSelectedEvent = QtCore.Signal('int')
    tagSelectedEvent = QtCore.Signal('QString')

    def __init__(self, parent=None):
        WidgetLister.__init__(self, parent)

    def add(self, person:Person):
        #log.info(f"{person}")
        widget = IndividualSearchResultWidget(self, person.idnum, person.name, person.tagList, person.about)
        widget.tagSelectedEvent.connect(self.tagSelectedEvent)
        widget.personSelectedEvent.connect(self.personSelectedEvent)

        WidgetLister.add(self, widget)
        
            
            
def main():
    import loadbook 
    book = loadbook.load_book("../../names.csv")
    
        
    personList = book.searchByName("Danny")
    print(personList)
    
    lister = SearchResultLister()
    for person in personList:
        lister.add(person)
    lister.show()
    return lister
