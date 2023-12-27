import pandas as pd 
import book 


def init():
    people = pd.DataFrame()
    people['idnum'] = [1,2,3]
    people['Name'] = "John Pat Mary".split()
    people['about'] = ['', '', '']
    people['tags'] = [ "tag1,tag2", "tag2,tag3", "tag4"]
    
    cols = "id1 connection id2".split()
    rel = pd.DataFrame(columns=cols)
    rel.loc[0] = [1, "brother of", 2]
    rel.loc[1] = [3, "sister of", 2]

    return book.Book(people, rel)


def test_smoke():
    bk = init()
    assert bk is not None 
    
    
def test_add():
    bk = init()
    tags = ["t1", "t2"]
    bk.add("Joe", tags, [])
    plist = bk.searchById(4)
    assert isinstance(plist, list), plist
    assert isinstance(plist[0], book.Person), plist
    assert plist[0].name == "Joe"


def test_editName():
    bk = init()
    bk.editName(1, "Joe")

    plist = bk.searchById(1)
    assert isinstance(plist, list), plist
    assert isinstance(plist[0], book.Person), plist
    assert plist[0].name == "Joe"

    
def test_setTags():
    bk = init()
    bk.setTags(1, ["new1", "new2"])
    plist = bk.searchById(1)
    person = plist[0]
    tags = person.tagList 
    assert len(tags) == 2
    assert tags[0] == "new1"
    assert tags[1] == "new2" 



def test_updateTags():
    bk = init()
    num = len(bk.searchById(1)[0].tagList)
    assert num == 2 
    
    bk.updateTags(1, ["new1", "new2"])
    tagList = bk.searchById(1)[0].tagList 
    assert len(tagList) == 4
    
    

def test_addRelationship():
    bk = init()
    bk.addRelationship(1, "friend of", 2)
    person = bk.searchById(1)[0]
    assert len(person.relationshipList) == 2
    
        
def test_searchByName():
    bk = init()
    plist = bk.searchByName("Mary")
    assert len(plist) == 1 
    assert plist[0].name == "Mary"
    
def test_searchByTag():
    bk = init()
    plist = bk.searchByTag("tag2")
    assert len(plist) == 2

    assert plist[0].name == "John"
    assert plist[1].name == "Pat"
    
"""
class Book:
 

    def setTags(self, idnum:int, tags:List):
        rownum = self.getRowNumForId(idnum)
        self.name_df.loc[rownum, 'tags'] = ",".join(tags)
        
    def editTags(self, idnum:int, new_tags:List):
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
        self.relation_df.iloc[num+1] = [idnum, relationship, companion]
        
    def searchByName(self, name):
        numchar = len(name)
        idx = self.name_df.Name.str[:numchar] == name
        wh = np.where(idx)[0]
        # idebug()
        personList = self.makePersonList(wh)
        return personList

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

"""
