#! /usr/bin/env python
#
# Ben Osment
# Thu Jan 31 17:47:32 EST 2013

import sys
import argparse
import sqlite3

verbose = False
db_conn = None

def add_card():
    """
    Add a card. User will prompted first for question, then answer. 

    Multiple card can be inserted at one time. User will press Ctrl-C 
    to exit (TODO: make sure the database connection is cleaned up)
    """
    # open a connection to our database
    # TODO: need something like...initial setup? something that creates the tables
    try:
        db_conn = sqlite3.connect('flashcard.db')
        cursor = db_conn.cursor()
    
    # loop for user input 

    # add each question-answer pair

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    # close connection
    finally:
        if db_conn:
            db_conn.close()

if __name__ == '__main__':
    # build the command line parser
    parser = argparse.ArgumentParser(description='Quiz yourself on flashcards or add new cards')
    parser.add_argument('-a', '--add', help='add a new flashcard', action='store_true')
    parser.add_argument('--verbose', action='store_true')    

    args = parser.parse_args(sys.argv[1:])

    global verbose
    verbose = args.verbose

    if args.add:
        add_card()

