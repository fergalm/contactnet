from ipdb import set_trace as idebug



import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
#import PyQt5.QtGui as QtGui

QtCore.Signal = QtCore.pyqtSignal

from book import Person 

QtCore.Signal = QtCore.pyqtSignal


class ViewForm(QtWidget.QWidget):
    
    """
    Signals:
    -----------
    
    searchByTagRequested
    back
    """
    
    searchByTagRequested = QtCore.Signal('QString')
    backButtonClicked = QtCore.Signal()
    
    #searchByTagRequested = QtCore.Signal()
    
    def __init__(self, person):
        QtWidget.QWidget.__init__(self, None)
        self.setupUi()
        self.person = person 
        self.displayPerson(person)
            
    def setupUi(self):
        layout = QtWidget.QVBoxLayout()

        #TODO: I need a labeled text edit widget
        QLabel = QtWidget.QLabel
        QEdit = QtWidget.QLineEdit
        
        self.nameEdit = QEdit()
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.nameEdit)

        self.tagsBox = QtWidget.QHBoxLayout()
        layout.addLayout(self.tagsBox)

        #Setup relations here 
        self.relationsBox = QtWidget.QVBoxLayout()
        layout.addLayout(self.relationsBox)
        #Setup phone numer and email here
        #TODO
        
        
        self.aboutEdit = QtWidget.QPlainTextEdit()
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.aboutEdit)

        self.back = QtWidget.QPushButton("Back")
        self.back.clicked.connect(self.backButtonClicked)
        layout.addWidget(self.back)
        
        self.setLayout(layout)

    def displayPerson(self, person:Person):
        self.nameEdit.setText(person.name)
        self.createButtonsForTags(person.tagList)
        #self.tagsEdit.setText(" ".join(person.tagList))
        self.aboutEdit = person.about 
        
        for relationship in person.relationshipList:
             widget = DisplayRelationshipWidget(self, relationship)
             self.relationsBox.addWidget(widget)

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
        print(f"Requesting a search of the tag {tag}")
        self.searchByTagRequested.emit(tag)

class DisplayRelationshipWidget(QtWidget.QWidget):
    def __init__(self, parent, relationship):
        QtWidget.QWidget.__init__(self, parent)
        
        layout = QtWidget.QHBoxLayout()
        layout.addWidget(QtWidget.QLabel(relationship))
        #layout.addWidget(QtWidget.QLabel(relationship.id1))
        #layout.addWidget(QtWidget.QLabel(relationship.connection))
        #layout.addWidget(QtWidget.QLabel(relationship.id2))
        self.setLayout(layout)


def main():
    #import pandas as pd 
    #df = pd.read_csv("../names.csv")
    #df = df.fillna("")
    #df['tags'] = df.apply(lambda x: ",".join([x.tag1, x.tag2, x.tag3, x.tag4]), axis=1)
    #df = df[:5]

    relations = [
        "Susan is mother of Pádraig",
        "Susan is mother of Róisín",
        "Linda Thompson is mother of Susan",
    ]
    susan = Person("Susan Mullally", "Herself", "Stsci Baltimore".split(), relations, idnum=1)
    
    form = ViewForm(susan)
    return form
    
    
    
