from ipdb import set_trace as idebug

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
#import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt

QtCore.Signal = QtCore.pyqtSignal

from widgetlister import WidgetLister 
from frmbase.flogger import log 

from book import Person, Relationship

example = Relationship(1, "Rob ", "husband of", 2, "Neha")    


class RelationshipLister(WidgetLister):
    changeMadeEvent = QtCore.Signal() 
    lookupIdEvent = QtCore.Signal('int')
    
    def __init__(self, book):
        WidgetLister.__init__(self)
        self.hasBeenEdited = False 
        self.book = book 
        self.setupUi()

    def setupUi(self):
        Qt = QtWidget
        #self.itemClicked.connect(self.editRelationship)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        
        #TODO: Make the list area as small as possible
        self.setMinimumHeight(40)
        self.setMaximumHeight(200)
        self.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.setSizePolicy(QtWidget.QSizePolicy.Minimum, QtWidget.QSizePolicy.Minimum)

    def __repr__(self):
        return f"<RelationshipLister with {len(self.widgetList)} entries>"
    
    def add(self, selfid, relationship):
        widget = RelationshipView(self.book, selfid, relationship) 
        #widget.relationshipChangedEvent.connect(self.handleRelationshipChangedEvent)
        widget.lookupIdEvent.connect(self.lookupIdEvent)
        WidgetLister.add(self, widget)
        
    def handleRelationshipChangedEvent(self):
        self.hasBeenEdited = True 
        self.changeMadeEvent.emit()
    
    def editRelationship(self, item):
        row = self.currentRow()
        log.info(self.currentRow())
        rel = self.widgetList[row]
        log.info(rel)

        dialog = RelationshipEditor(self.book, self.selfid, rel)
        log.info("Creating dialog")
        if dialog.exec():
            self.hasBeenEdited = True 
            log.info(f"hasBeenEdited set to {self.hasBeenEdited}")
            self.changeMadeEvent.emit()
            
            rel = dialog.getRelationship()
            self.relationshipList[row] = rel 
            self.takeItem(row)
            self.insertItem(row, str(rel) )
    

class RelationshipView(QtWidget.QWidget):
    lookupIdEvent = QtCore.Signal(int)
    relationshipChangedEvent = QtCore.Signal()
    
    def __init__(self, book, selfid, relationship, parent=None):
        """selfid is the part of the relationship that can't be edited"""
        
        QtWidget.QWidget.__init__(self, parent)
        self.book = book 
        self.rel = relationship
        self.selfid = selfid
        #text = self.setText(selfid, relationship)
        #self.setupUi(selfid, text)
        self.setupUi(selfid)
        log.info("Creating a view widget")
        
    #def __str__(self):
        #return str(self.rel)
        
    def setupUi(self, selfid):
        rel = self.rel 

        layout = QtWidget.QHBoxLayout()
        
        if selfid == rel.idnum1:
            self.label = QtWidget.QLabel(f"{rel.name1} is {rel.connection}")
            self.button = QtWidget.QPushButton(f"{rel.name2}")
            self.idnum = int(rel.idnum2)
            layout.addWidget(self.label)
            layout.addWidget(self.button)
        else:
            self.button = QtWidget.QPushButton(f"{rel.name1}")
            self.label = QtWidget.QLabel(f"is {rel.connection} {rel.name2}")
            self.idnum = int(rel.idnum1)
            layout.addWidget(self.button)
            layout.addWidget(self.label)
        self.button.clicked.connect(self.handleIdRequest)
        
        edit = QtWidget.QPushButton("Edit")
        edit.setMaximumWidth(40)
        edit.clicked.connect(self.editRelationship)
        layout.addWidget(edit)
        self.setLayout(layout)

    def createText(self, selfid, relation):
        rel = relation
        layout = QtWidget.QHBoxLayout()
        
        if selfid == rel.idnum1:
            self.label = QtWidget.QLabel(f"{rel.name1} is {rel.connection}")
            self.button = QtWidget.QPushButton(f"{rel.name2}")
            self.idnum = int(rel.idnum2)
            layout.addWidget(self.label)
            layout.addWidget(self.button)
        else:
            self.button = QtWidget.QPushButton(f"{rel.name1}")
            self.label = QtWidget.QLabel(f"is {rel.connection} {rel.name2}")
            self.idnum = int(rel.idnum1)
            layout.addWidget(self.button)
            layout.addWidget(self.label)
        self.button.clicked.connect(self.handleIdRequest)
        
        edit = QtWidget.QPushButton("Edit")
        edit.setMaximumWidth(40)
        edit.clicked.connect(self.editRelationship)
        layout.addWidget(edit)
        self.setLayout(layout)

        
    def handleIdRequest(self):
        log.info(f"ID lookup request for {self.idnum}")
        self.lookupIdEvent.emit(self.idnum)
    
        
    def editRelationship(self):
        log.info("Editing relationship")
        dialog = RelationshipEditor(self.book, self.selfid, self.rel)
        if dialog.exec():
            self.rel = dialog.getRelationship()
            
            import utils 
            utils.clearLayout(self.layout())
            lo = self.layout()
            del lo
            self.createText(self.selfid, self.rel)
            #Tell the parent that we've changed
            self.relationshipChangedEvent.emit()
        
    #def setText(self, selfid, relationship):
        
        #name1 = relationship.name1 
        #name2 = relationship.name2
        #connection = relationship.connection
        
        #if relationship.idnum1 == selfid:
            #name2 = f"<FONT color='blue'>{name2}</FONT>"
        #else:
            #name1 = f"<FONT color='blue'>{name1}</FONT>"
        #text = f"{name1} is {connection} {name2}"
        #return text 
    
    
class RelationshipEditor(QtWidget.QDialog):
    def __init__(self, book, selfid, relationship):
        QtWidget.QDialog.__init__(self)
        log.info("Init RelationshipEditor")
        self.book = book 
        self.nameCompleter = Qt.QCompleter(book.getNameList(), self)

        self.setupUi(selfid, relationship)
        
    def setupUi(self, selfid, relationship):
        self.setWindowTitle("Edit Relationship")

        self.widget1 = QtWidget.QLineEdit(relationship.name1)
        self.widget2 = QtWidget.QLabel("is")
        self.widget3 = QtWidget.QLineEdit(relationship.connection)
        self.widget4 = QtWidget.QLineEdit(relationship.name2)
        
        self.widget1.setCompleter(self.nameCompleter)
        self.widget4.setCompleter(self.nameCompleter)
        
        if selfid == relationship.idnum1:
            self.widget1.setDisabled(True)
        else:
            self.widget4.setDisabled(True)
            
        innerlayout = QtWidget.QHBoxLayout()
        for w in [self.widget1, self.widget2, self.widget3, self.widget4]:
            innerlayout.addWidget(w)
            
              
        options = QtWidget.QDialogButtonBox
        QBtn = options.Save | options.Cancel            
        buttonBox = QtWidget.QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        outerlayout = QtWidget.QVBoxLayout()
        outerlayout.addLayout(innerlayout)
        outerlayout.addWidget(buttonBox)
        self.setLayout(outerlayout)

    def accept(self):
        QtWidget.QDialog.accept(self)
        
    def reject(self):
        QtWidget.QDialog.reject(self)

    def getRelationship(self):
        name1 = self.widget1.text()
        idnum1 = self.book.getIdForName(name1)
        name2 = self.widget4.text()
        idnum2 = self.book.getIdForName(name2)
        connection = self.widget3.text()

        rel = Relationship(idnum1, name1, connection, idnum2, name2)
        return rel 


def main():
    import loadbook 
    book = loadbook.load_book("../../names.csv")
    
    lister = RelationshipLister(book)
    
    #person= book.getPerson(193)
    person = book.getPerson(10)
    
    widget = RelationshipView(book, person.idnum, person.relationshipList[0])
    widget.show()
    return widget

    selfid = person.idnum
    for r in person.relationshipList:
        #widget = RelationshipView(book, selfid, r)
        lister.add(selfid, r)
    lister.show()
    return lister    
