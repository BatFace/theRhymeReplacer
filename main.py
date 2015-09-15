import argparse
import psycopg2
import re
import sys

DB_NAME = "dbName" # Insert DB Name in which dictonary table exists
DB_USER = "dbOwner"

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs='?', help='Original file')
parser.add_argument('--output', nargs='?', help='Output file')
parser.add_argument('-s', action='store_true', help='Match on syllables')
args = vars(parser.parse_args())

conn = psycopg2.connect("dbname='{name}' user='{user}'".format(name=DB_NAME,user=DB_USER))

input = open(args['input'], 'r') if args['input'] else sys.stdin 
output = open(args['output'], 'w') if args['output'] else sys.stdout

# Zips the rhyming words back together with any spaces/punctuation/newlines
def reconstruct_line(list_a, list_b, word_start):
    (a,b) = (list_a, list_b) if word_start else (list_b, list_a)
    if len(a) > len(b): b.append('')
    line = [a2 + b2 for (a2, b2) in zip(a,b)]
    return "".join(line)

syllableSelector = 'AND dict.syllable_count = input.syllable_count' if args['s'] else ''

query ="""SELECT dict.word 
          FROM dictionary AS dict,
	       (SELECT word, syllable_count, rhyme_group 
	       FROM dictionary 
	       WHERE word = %s) AS input 
	  WHERE dict.rhyme_group = input.rhyme_group {0}
	       ORDER BY RANDOM()
   	  LIMIT 1;""".format(syllableSelector)

with conn.cursor() as cur:
    for line in input:
        new_words = []
        words = re.findall(r"[\w']+", line)
        non_words = re.findall(r"[^\w']+", line)
        word_start = re.match("[\w]", line[0]) != None
        for word in words:
            word = word.upper()
            cur.execute(query, (word,))
            res = cur.fetchone()
            new_words.append(res[0]) if res else new_words.append(word)
        output.write(reconstruct_line(new_words, non_words, word_start))

input.close()
output.close()



