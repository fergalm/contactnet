#from ipdb import set_trace as idebug
from typing import List
#import pandas as pd 
import numpy as np 

"""
TODO

o Search by name should be by regex 
o Clean up input 
x Person request should return back links to that person 
o Add person and edit person endpoints


add 
--> INSERT INTO people ({idnum}, {name}, {about})
self.setTags()
for r in relations:
    self.setRElationship()
"""

#Predeclare
class Person:
    pass 

class SqlBook:
    def __init__(self, dbpath):
        self.dbpath = dbpath 
        self.sep = "|"
        
    def __repr__(self):
        return f"<Book with {len(self.name_df)} entries>"
    
    def add(self, name:str, about:str, tags:List, relationships:List = None):
        """TODO: Should this be addPerson(p:Person) ?"""
        
        tags = self.sep.join(tags)        #Send this cmd to sql 
        cmd = f"INSERT INTO people ({idnum}, {name}, {about}, {tags})"
        
        self.setTags(tags)
        for r in relationshipList:
            self.addRelationship(r)

    def editName(self, idnum, name):
        rownum = self.getRowNumForId(idnum)
        #FIXME
        cmd = f"INSERT name = {name} INTO people WHERE {rownum} = idnum"

    def setTags(self, idnum:int, tags:List):
        tags = self.sep.join(tags)
        rownum = self.getRowNumForId(idnum)
        cmd = f"INSERT tags = {tags} INTO people WHERE {rownum} = idnum"
        self._updateTagDict(tags)
        
    def updateTags(self, idnum:int, new_tags:List):
        rownum = self.getRowNumForId(idnum)
        old_tags = f"SELECT tags FROM people WHERE idnum = {rownum}"
        new_tags = tags.split(',')
        
        new_tags = list(set(new_tags) | set(tags))
        new_tags = self.sep.join(new_)
        self.setTags(idnum, tags)
        
    def _updateTagDict(self, new_tags):
        for t in new_tags:
            if t not in self.tagDict:
                self.tagDict[t] = []
            self.tagDict[t].append(rownum)
        
    def addRelationship(self, idnum, relationship, companion):
        #TODO Check both idnums exist 
        cmd = f"INSERT INTO relationships ({idnum1}, {relationship}, {idnum2})"
        
    def searchByName(self, name):
        size = len(name)
        cmd = f"SELECT * FROM people where substr(name, size) = {name}"
        
        cmd2 = f"SELECT * FROM relationships WHERE idnum1 in {rownums}"
        cmd3 = f"SELECT * FROM relationships WHERE idnum2 in {rownums}"
        
        #TODO Make a list of persons 

    def searchByTag(self, tag):
        try:
            matches = self.tagDict[tag]
        except KeyError:
            return [] 
        
        wh = np.where(self.name_df.idnum.isin(matches))[0]
        return self.makePersonList(wh)
        
    def searchById(self, idnum) -> List[Person]:
        rownum = self.getRowNumForId(idnum)
        result = Person.from_row(rownum, self.name_df, self.relation_df) 
        return [result]

    def makePersonList(self, wh):
        out = []
        for i in wh:
            out.append(Person.from_row(i, self.name_df, self.relation_df))
        return out 
        
    def getRowNumForId(self, idnum):
        try:
            rownum = np.where(self.name_df.idnum == idnum)[0][0]
        except IndexError:
            raise ValueError(f"Idnum {idnum} not found")
        return rownum

    def save(self, fn):
        self.name_df.to_csv(fn)
        
        
def createTagDict(df) -> dict:
    out = dict()
    for i, row in df.iterrows():
        idnum = row.idnum 
        tags = row.tags.split(',')
        for t in tags:
            if t not in out:
                out[t] = []
            out[t].append(idnum)
    return out 

        
class Person:
    def __init__(self, name, about, tags, relationships, idnum=None):
        self.idnum = idnum
        self.name = name 
        self.about = about 
        self.tagList = tags 
        self.relationshipList = relationships 

    @classmethod
    def from_row(cls, row, names, relations):
        row = names.iloc[row]
        
        #@TODO: Why is this necessary. I should alwys be passing type(row)==int
        try:
            idnum = row.idnum.iloc[0]
            name = row.Name.iloc[0] 
            about = row.about.iloc[0]
            tags = row.tags.iloc[0].split(',')
        except AttributeError:
            idnum = row.idnum
            name = row.Name
            about = row.about 
            tags = row.tags.split(',')
            
            
        wh = np.where(relations.id1 == idnum)[0]
        tmp = []
        for w in wh:
            rrow = relations.iloc[w]
            name1 = names[ names.idnum == rrow.id1].Name.iloc[0]
            name2 = names[ names.idnum == rrow.id2].Name.iloc[0] 
            tmp.append(f"{name1} is {rrow.connection} {name2}")

        wh = np.where(relations.id2 == idnum)[0]
        for w in wh:
            rrow = relations.iloc[w]
            name1 = names[ names.idnum == rrow.id1].Name.iloc[0]
            name2 = names[ names.idnum == rrow.id2].Name.iloc[0] 
            tmp.append(f"{name1} is {rrow.connection} {name2}")
        
        return Person(name, about, tags, tmp, idnum)

    def print(self):
        print(f"Name: {self.name}  ({self.idnum})" )
        print(f"Notes: {self.about}")
        print(f"Tags: {','.join(self.tagList)}")
        
        #idebug()
        if len(self.relationshipList) > 0:
            print("")
            print("\n".join(self.relationshipList))
        print("---")        
    

class Relationship:
    def __str__(self):
        print("Printing relationships not implemented")
     
