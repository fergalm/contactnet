
from ipdb import set_trace as idebug



import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
#import PyQt5.QtGui as QtGui

QtCore.Signal = QtCore.pyqtSignal

from frmbase.flogger import log 
from book import Person 


class SearchWidget(QtWidget.QWidget):
    
    """
    Signals:
    -----------
    
    searchByTagRequested
    back
    """
    nameSearchRequested = QtCore.Signal('QString')
    tagSearchRequested = QtCore.Signal('QString')

    def __init__(self, parent=None):
        QtWidget.QWidget.__init__(self, parent)
                
        label1 = QtWidget.QLabel("Name")
        self.nameEdit = QtWidget.QLineEdit()
        self.nameEdit.returnPressed.connect(self.handleNameSearchRequest)

        label2 = QtWidget.QLabel("Tags")
        self.tagEdit = QtWidget.QLineEdit()
        self.tagEdit.returnPressed.connect(self.handleTagSearchRequest)
        
        layout = QtWidget.QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.nameEdit)
        layout.addWidget(label2)
        layout.addWidget(self.tagEdit)
        self.setLayout(layout)

    def handleNameSearchRequest(self):
        name = self.nameEdit.text()
        log.info(f"Searching names for {name}")
        self.nameSearchRequested.emit(name)

    def handleTagSearchRequest(self):
        tag= self.tagEdit.text()
        log.info(f"Searching tags for {tag}")
        self.tagSearchRequested.emit(tag)

    #personSelectedEvent = QtCore.Signal('int')
    #tagSelectedEvent = QtCore.Signal("QString")
    
        #self.tagBox = QtWidget.QHBoxLayout()
        #self.createButtonsForTags(tags)

    #def createButtonsForTags(self, tagList):
        #layout = self.tagBox 
        
        #for tag in tagList:
            #button = QtWidget.QPushButton('#' + tag)
            #button.setFlat(True)
            #button.setStyleSheet("QPushButton {color:blue;}")

            #import functools 
            #f = functools.partial(self.handleSearchByTagRequest, tag)
            #button.clicked.connect(f)
            #layout.addWidget(button)
     

    #def handleSearchByTagRequest(self, tag:str):
        #log.info(f"Tag '{tag}' on '{self.name.text()}' was clicked")
        #self.tagSelectedEvent.emit(tag)
        
        


def main():
    return SearchWidget()
