from ipdb import set_trace as idebug
from typing import List, Tuple
import pandas as pd 
import numpy as np 
from book import Book  


import argparse 
import sys 


def setup_argparse():
    """
    
    Search interface
    contactnet [-n name] [-t tags]

    TODO: 
    x Search by ID
    x edit a record 
    ~ Add a relationship 
    o --add --about
    o Add multiple relations in a single pass 
    o When adding tags, avoid duplication
    o Add a new person
    """
    
    parser = argparse.ArgumentParser(
        prog="contactnet",
        description="Map connections between your contacts",
        add_help=True,
 )
    
    parser.add_argument("--name", type=str)
    parser.add_argument("--tags", type=str)
    parser.add_argument("--id", type=int)
    parser.add_argument("--add", action='store_true')
    parser.add_argument("--edit", type=int, default=False, help="Id num of contact to edit")
    parser.add_argument("--relation", type=str, default=False, help="e.g 'aunt of 175'. Last token must be a valid id number")

    return parser

def getRelationshipTuple(strr) -> Tuple[str, int]:
    """Convert a string like "mother of 175" to ("mother of", 175)"""
    
    tokens = strr.split()
    rtype = " ".join(tokens[:-1])
    rid = int(tokens[-1])
    return rtype, rid 


def main():
    fn = "names.csv"

    parser = setup_argparse()
    args = parser.parse_args() 
    
    book = load_book(fn)
    
    #TODO Pretty this up some
    if args.add:
        if not args.name:
            raise ValueError("Must supply a name to add")
        
        tags = args.tags or "" 
        tags = tags.split(',')
        
        relation = args.relation or []
        relation = lmap(getRelationshipTuple, relation)
        idnum = book.add(args.name, tags, relation)
        people = book.searchById(idnum)
        print(printPersonList(people))

    elif args.edit:
        idnum = int(args.edit)
        
        if args.name:
            book.editName(idnum, args.name)
        if args.tags:
            tags = args.tags.split(',')
            book.editTags(idnum, args.tags)
        if args.relation:
            relations = args.relation.split(',')
            relations = lmap(getRelationshipTuple, relation)
            for r in relations:
                book.addRelationship(idnum, r[0], r[1])
            
        #book.save()
        people = book.searchById(idnum) 
        print(printPersonList(people))
        #book.save(fn)

    else:
        if args.name:
            people = book.searchByName(args.name)
        elif args.tags:
            people = book.searchByTag(args.tags)
        elif args.id:
            people = book.searchById(args.id)
        else:
            parser.print_help()
            sys.exit(0)
        
        print(printPersonList(people))
        print("Finished")
    
    
def load_book(fn):
 
    df = pd.read_csv(fn)
    df['idnum'] = df['idnum'].replace(np.nan, -1).astype(int)
    df['id1'] = df['id1'].replace(np.nan, -1).astype(int)
    tags = df[['tag1', 'tag2', 'tag3', 'tag4']].replace(np.nan, "")
    df['tags'] = tags.agg(','.join, axis=1)    
    df = df.replace(np.nan, "")
    
    namedf = df[['idnum', 'Name', 'about', 'tags']]
    reldf = df[['idnum', 'R1', 'id1']]
    reldf = reldf[ reldf.id1 > 0]
    reldf = reldf.rename( {'idnum': 'id1', 'R1':'connection', 'id1':'id2'}, axis=1)
    book = Book(namedf, reldf)
    #print(namedf)
    return book
    
    #df2 = df.copy()
    #df2.drop(['R1', 'id1']
        
        
        
def printPersonList(personList):
    for person in personList:
        printPerson(person)
        
        
def printPerson(person):
    person.print()



def lmap(func, args):
    return list(map(func, args))

if __name__ == "__main__":
    main()
