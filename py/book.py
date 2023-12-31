#from ipdb import set_trace as idebug
from typing import List
#import pandas as pd 
import numpy as np 

from frmbase.flogger import log 

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

class Book:
    def __init__(self, name_df, relation_df):
        self.name_df = name_df 
        self.relation_df = relation_df
        self.tagDict = createTagDict(self.name_df)

    def __repr__(self):
        return f"<Book with {len(self.name_df)} entries>"
    
    def add(self, name:str, about:str, tags:List, relationships:List = None):
        """TODO: Should this be addPerson(p:Person) ?"""
        idnum = self.name_df.idnum.max() + 1
        self.name_df.loc[idnum] = (idnum, name, about, '') 
        self.editTags(idnum, tags)

        relationships = relationships or []
        for relation in relationships:
            self.addRelationship(idnum, relation[0], relation[1])
        return idnum
 
    def editName(self, idnum, name):
        rownum = self.getRowNumForId(idnum)
        self.name_df.loc[rownum, 'Name'] = name

    def setTags(self, idnum:int, tags:List):
        rownum = self.getRowNumForId(idnum)
        self.name_df.loc[rownum, 'tags'] = ",".join(tags)
 
    def getNameList(self):
        """Return a list of all tags. Used for autocomplete"""
        return self.name_df.Name.values
 
    def getTagList(self):
        """Return a list of all tags. Used for autocomplete"""
        return self.tagDict.keys()
    
    def updateTags(self, idnum:int, new_tags:List):
        rownum = self.getRowNumForId(idnum)
        tags = self.name_df.iloc[rownum].tags
        tags = tags.split(',')
        
        new_tags = list(set(new_tags) - set(tags))
        tags.extend(new_tags)
        print(f"The tags are {tags}")
        self.name_df.loc[rownum, 'tags'] = ",".join(tags)
        
        for t in new_tags:
            if t not in self.tagDict:
                self.tagDict[t] = []
            self.tagDict[t].append(rownum)
        
    def addRelationship(self, idnum, relationship, companion):
        num = self.relation_df.index.max()
        self.relation_df.loc[num+1] = [idnum, relationship, companion]
        
    def searchByName(self, name):
        numchar = len(name)
        idx = self.name_df.Name.str[:numchar] == name
        wh = np.where(idx)[0]
        # idebug()
        personList = self.makePersonList(wh)
        return personList

    def getIdForName(self, name):
        wh = np.where(self.name_df.Name == name)[0]
        
        if len(wh) == 0:
            raise ValueError(f"No entry matches {name}")
        if len(wh) > 1:
            raise ValueError(f"Ambiguous name: {name}")
        return self.name_df.idnum.iloc[wh[0]]
    
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

    def getPerson(self, idnum):
        wh = np.where(self.name_df.idnum == idnum)[0]
        return Person.from_row(wh, self.name_df, self.relation_df)
    
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

    def __repr__(self):
        return f"<book.Person ({self.idnum}: {self.name})>"
    
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
            idnum1 = rrow.id1
            idnum2 = rrow.id2
            name1 = names[ names.idnum == idnum1].Name.iloc[0]
            name2 = names[ names.idnum == idnum2].Name.iloc[0] 
            relation = Relationship(idnum1, name1, rrow.connection, idnum2, name2)
            tmp.append(relation)
            log.info(relation)

        wh = np.where(relations.id2 == idnum)[0]
        for w in wh:
            rrow = relations.iloc[w]
            idnum1 = rrow.id1
            idnum2 = rrow.id2
            name1 = names[ names.idnum == idnum1].Name.iloc[0]
            name2 = names[ names.idnum == idnum2].Name.iloc[0] 
            relation = Relationship(idnum1, name1, rrow.connection, idnum2, name2)
            tmp.append(relation)
            log.info(relation)
            
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
    def __init__(self, idnum1, name1, connection, idnum2, name2):
        self.name1 = name1
        self.name2 = name2
        self.idnum1 = idnum1
        self.idnum2 = idnum2
        self.connection = connection

    def __str__(self):
        return f"{self.name1} is {self.connection} {self.name2}"

    def __repr__(self):
        return f"<Relationship between {self.name1} & {self.name2}>"
