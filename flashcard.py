#! /usr/bin/env python
#
# Ben Osment
# Thu Jan 31 17:47:32 EST 2013

import sys
import argparse
import sqlite3


# configuration
DATABASE = 'flashcard.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DEBUG = True
verbose = False
db_conn = None


def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    db = connect_db()
    f = open('schema.sql')
    db.cursor().executescript(f.read())
    db.commit()

def add_card():
    """
    Add a card. User will prompted first for question, then answer. 

    Multiple card can be inserted at one time. User will press Ctrl-C 
    to exit (TODO: make sure the database connection is cleaned up)
    """
    # open a connection to our database
    # TODO: need something like...initial setup? something that creates the tables
    
    print "Add cards, one at a time"
    print "Type 'quit' or Ctrl-C to quit"

    try:
        db = connect_db()
        cursor = db.cursor()
    
        # loop for user input 
        # TODO: have a way for a user to input multiple lines
        #       like a batch option?
        while True:
            
            front = raw_input("Front: ")
            if front == 'quit':
                break
            back = raw_input("Back: ")
            # issue SQL
            db.execute('insert into flashcard (front, back) values (?, ?)', 
                       (front, back))
            # add/commit each question-answer pair
            db.commit()
            
            
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    # close connection
    finally:
        if db:
            db.close()


def batch_add(filename):
    """
    Batch add a card. Read a colon deliminated file, adding card one at time
    """
    num_cards = 0
    # open connection to DB
    try:
        db = connect_db()
        cursor = db.cursor()
    
        # open file
        # for each deliminated line, add a card
        for line in open(filename):
            line = line.strip()
            front, back = line.split(':')
            # issue SQL
            db.execute('insert into flashcard (front, back) values (?, ?)', 
                       (front, back))
            num_cards += 1

        # commit DB
        db.commit()
        # print statistics (num cards added)            
        print "added %d cards" % num_cards
            
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    # close connection
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    # build the command line parser
    # TODO: have a REVERSE option, where back is presented first
    parser = argparse.ArgumentParser(description='Quiz yourself on flashcards or add new cards')
    parser.add_argument('-a', '--add', help='add a new flashcard', action='store_true')
    parser.add_argument('-b', '--batch', help='batch add a file')
    parser.add_argument('--verbose', action='store_true')    

    args = parser.parse_args(sys.argv[1:])

    #global verbose
    #verbose = args.verbose

    if args.batch:
        batch_add(args.batch)
        sys.exit(0)
        
    if args.add:
        add_card()
        sys.exit(0)

