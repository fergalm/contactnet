import PyQt5.QtWidgets as QtWidget


"""
Based on a suggestion in 
https://stackoverflow.com/questions/948444/qlistview-qlistwidget-with-custom-items-and-custom-item-widgets

"""


class WidgetLister(QtWidget.QListWidget):
    """A wrapper around QT's QListWidget that makes adding widgets easier"""
    def __init__(self, parent=None):
        QtWidget.QListWidget.__init__(self, parent)
        self.widgetList = []
        
    def add(self, widget):
        self.widgetList.append(widget)
        item = QtWidget.QListWidgetItem(self)
        self.addItem(item)
        self.setItemWidget(item, widget)
        item.setSizeHint(widget.minimumSizeHint())
        
    def insert(self, widget, i):
        self.widgetList.insert(i, widget)
        item = QtWidget.QListWidgetItem(self)
        self.insertItem(i, item)
        self.setItemWidget(item, widget)
        item.setSizeHint(widget.minimumSizeHint())
                
        
    def delete(self, i):
        self.takeItem(i)

    def replace(self, widget, i):
        self.takeItem(i)
        self.insert(widget, i)
        
    def clear(self):
        for i in range(self.count()):
            self.takeItem(0)

    def getWidget(self, i):
        return self.widgetList[i]
