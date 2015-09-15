# The Rhyme Replacer
Command line Python program replacing words in a source text with rhyming ones taken from a database.

## You will need
* Python3
* [PostgreSQL](http://www.postgresql.org/download/) 
* [psycopg2](http://initd.org/psycopg/) -- make sure this is installed against Python3, too

## Setup
* Create the 'dictionary' table using the CreateDictionaryTable script against the Postgres database of your choice (I just put it in my default username one). You'll need to change the \<dbOwner\> to something appropriate for your setup.
* Alter main.py to use the database name and user as the values for DB_NAME and DB_USER you used in the above step.

## To run
The program can be run in a several ways Some examples (in a Unix-y style):

1. Out of one text file and into another

        cat poem | python3 main.py > newPoem
        
2. Sourced from a text file and output to the command line

        cat poem | python3 main.py
        
3. From the command line into a text file

        \echo "Those chubby, stubby beans" | python3 main.py > aGreatPoem
        
4. Just on the command line, one word at a time

        python3 main.py

Add an -s flag to enforce matching syllables between the input and ouput words. --input and --output flags can also be used instead of the pipe style given in the examples. There's some help written into the program (run with --help or -h) but as an example:

        python3 main.py -s --input poem --output newPoem


###### Credit: The database used in this project is a ported, reduced version of this [DillFog Muse MySQL database](http://muse.dillfrog.com/dump/).

