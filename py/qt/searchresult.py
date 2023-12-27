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
        

class SearchResultWidget(QtWidget.QWidget):
    """Displays a list of search results"""
    
    personSelectedEvent = QtCore.Signal('int')
    tagSelectedEvent = QtCore.Signal('QString')

    
    #def __init__(self, parent, results:list = None):
        #QtWidget.QWidget.__init__(self, parent)

        #layout = QtWidget.QVBoxLayout()
        
        #header = QtWidget.QLabel("Search Results")
        #layout.addWidget(header)

        #results = results or [] 
        #for result in results:
            #layout.addWidget(result)
        #self.setLayout(layout)

    def __init__(self, parent, results:list = None):
        QtWidget.QWidget.__init__(self, parent)

        groupbox = QtWidget.QGroupBox("Search Results Group Box")
        self.innerlayout = QtWidget.QVBoxLayout()
        self.innerlayout.addStretch()
        
        header = QtWidget.QLabel("Search Results")
        self.innerlayout.addWidget(header)

        results = results or [] 
        for result in results:
            self.innerlayout.addWidget(result)
            result.show()

        groupbox.setLayout(self.innerlayout )
        scroll = QtWidget.QScrollArea()
        #scroll.setLayout(self.innerlayout)
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        scroll.setFixedWidth(400)

        lo = QtWidget.QVBoxLayout(self)
        lo.addWidget(scroll)
        #lo.addWidget(groupbox)
        self.setLayout(lo)
        
    def addPerson(self, person:Person):
        log.info(f"{person}")
        #idebug()
        widget = IndividualSearchResultWidget(None, person.idnum, person.name, person.tagList, person.about)
        widget.tagSelectedEvent.connect(self.tagSelectedEvent)
        
        self.innerlayout.insertWidget(self.innerlayout.count(), widget)
        #log.info(self.innerlayout.count())
        widget.personSelectedEvent.connect(self.personSelectedEvent)
                
    def clear(self):
        log.info("Clearing search results widget")
        layout = self.innerlayout
        
        log.info(layout.count())
        while layout.count() > 1:
            widget = layout.takeAt(1)
            widget.widget().setParent(None)
            del widget
            
            
def main():
    df = pd.read_csv("../names.csv")
    df = df[:5]
    df = df.fillna("")
    
    results = []
    for i, row in df.iterrows():
        tags = [row.tag1, row.tag2, row.tag3, row.tag4]
        res = IndividualSearchResultWidget(None, row.idnum, row.Name, tags, row.about)
        results.append(res)
        
    coll = SearchResultWidget(None, results)
    #coll.clear()
    return coll
    
    
#class CategoricalFilter(AbstractColumnFilter):
    #def __init__(self, col, parent=None):
        #AbstractColumnFilter.__init__(self, parent)

        #self.label = QtWidget.QLabel(col.name)

        #self.col = col
        #self.idx = np.ones(len(col), dtype=bool)
        #self.items = set(col)
        #self.combo = CheckableComboBox()
        #self.combo.addItems(self.items)
        #self.combo.model().dataChanged.connect(self.onChange)

        #layout = QtWidget.QVBoxLayout()
        #layout.addWidget(self.label)
        #layout.addWidget(self.combo)
        #self.setLayout(layout)

    #def getFilteredIn(self) -> np.ndarray:
        ## print('Debug GFI', self.col.name, np.sum(self.idx))
        #return self.idx.copy()

    
