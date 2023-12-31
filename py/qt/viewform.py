from ipdb import set_trace as idebug



import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
#import PyQt5.QtGui as QtGui

QtCore.Signal = QtCore.pyqtSignal

from frmbase.flogger import log 
from book import Person 


class ViewForm(QtWidget.QWidget):
    
    """
    Signals:
    -----------
    
    searchByTagRequested
    back
    """
    
    searchByTagRequested = QtCore.Signal('QString')
    backButtonClicked = QtCore.Signal()
    lookupIdRequested = QtCore.Signal('int')
    
    def __init__(self, book):
        QtWidget.QWidget.__init__(self, None)
        self.book = book 
        self.isModified = False 
        self.setupUi()
    
    def handleModificationEvent(self):
        self.isModified = True 
        log.info(f"{self.sender()}")
        self.save.setDisabled(False)
            
    def setupUi(self):
        layout = QtWidget.QVBoxLayout()

        #TODO: I need a labeled text edit widget
        QLabel = QtWidget.QLabel
        QEdit = QtWidget.QLineEdit
        
        self.nameEdit = QEdit()
        self.nameEdit.textChanged.connect(self.handleModificationEvent)
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.nameEdit)

        self.tagsBox = QtWidget.QHBoxLayout()
        layout.addLayout(self.tagsBox)

        #Setup relations here 
        from relationshipview import RelationshipLister
        self.relationsBox = RelationshipLister(self.book)
        self.relationsBox.changeMadeEvent.connect(self.handleModificationEvent)
        self.relationsBox.lookupIdEvent.connect(self.handleSearchByIdEvent)
        layout.addWidget(self.relationsBox)
        #Setup phone numer and email here
        #TODO
        
        
        self.aboutEdit = QtWidget.QPlainTextEdit()
        self.aboutEdit.textChanged.connect(self.handleModificationEvent)
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.aboutEdit)

        self.save = QtWidget.QPushButton("Save")
        self.save.setDisabled(True)
        self.back = QtWidget.QPushButton("Back")
        self.back.clicked.connect(self.backButtonClicked)
        
        layout.addWidget(self.save)
        layout.addWidget(self.back)
        
        self.setLayout(layout)
        
    def displayPerson(self, person:Person):
        self.clearForm()
        self.nameEdit.setText(person.name)
        self.createButtonsForTags(person.tagList)
        self.aboutEdit.setPlainText(person.about)
        
        log.info(f"Filling relationships for {person}")
        log.info(f"{person.relationshipList}")
        selfid = person.idnum
        for relationship in person.relationshipList:
            self.relationsBox.add(selfid, relationship)
        
        self.isModified = False
        self.save.setDisabled(True)
    
    def clearForm(self):
        self.nameEdit.setText("")
        self.aboutEdit.setPlainText("")
        self.relationsBox.reset()

        self.relationsBox.clear()
        clearLayout(self.tagsBox)

    def createButtonsForTags(self, tagList):
        layout = self.tagsBox 
        
        for tag in tagList:
            button = QtWidget.QPushButton(tag)
            button.setFlat(True)
            button.setStyleSheet("QPushButton {color:blue;}")
            f = lambda: self.handleSearchByTagRequest(tag)
            button.clicked.connect(f)
            layout.addWidget(button)
     
    #@QtCore.pyqtSlot()
    def handleSearchByTagRequest(self, tag):
        sender = self.sender()
        tag = sender.text()
        log.info(f"Requesting a search of the tag {tag}")
        self.searchByTagRequested.emit(tag)

    def handleSearchByIdEvent(self, idnum):
        log.info(f"Request received to search for {idnum}")
        self.lookupIdRequested.emit(idnum)

def clearLayout(layout, nhead=0):
    """Clears all widgets from a layout

    TODO: Do this recursively with sublayouts too
    """
    import utils 
    utils.clearLayout(layout, nhead)


import loadbook 
def main():

    book = loadbook.load_book("../../names.csv")

    person= book.getPerson(193)
    #person = book.getPerson(10)
    
    form = ViewForm(book)
    #form.displayPerson(susan)
    form.displayPerson(person)
    form.show()
    return form
    
    
    
