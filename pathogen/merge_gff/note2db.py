#!/usr/bin/python

'''
This tool can be used to add a note attribute to a gff feature in a 
gffutils database. Gff features matching a given ID will have notes 
added to them. IDs can be searched in other attributes as well such
as Names using the "--attribute" option
'''

import sys,argparse
import gffutils
from itertools import chain


#######################################
#           Load sys. args.           #
#                                     #
#                                     #
#######################################

ap = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument('--in_db',required=True,type=str,help='The gffutils database to be searched')
ap.add_argument('--out_db',required=True,type=str,help='The name of the output gff file')
ap.add_argument('--id_file',required=True,type=str,help='A text file containing gene IDs or transcript IDs for annotation')
ap.add_argument('--str',required=True,type=str,help='Text to add to the notes section for each matched feature.')
ap.add_argument('--attribute',required=False,default='ID',type=str,help='The attribute to search for the IDs within, default is ID')

conf = ap.parse_args() #sys.argv

#######################################
#      Load the ID file into          #
#             a dict.                 #
#                                     #
#######################################

dict = {}
with open(conf.id_file) as f:
    for line in f:
    	id = line.strip()
    	dict[id] = None

dict_len = len(dict.keys())
print("No. IDs in infile:\t" + str(dict_len))

#######################################
#      Define the transformation      #
#          functions used to          #
#          edit the database          #
#######################################

new_note = conf.str
a = conf.attribute
i = 0
def transform_func(x):
	if a in x.attributes:
		this_id = "".join(x.attributes[a])
		if this_id in dict.keys():
			if not 'Note' in x.attributes:
				x.attributes['Note'] = new_note
			else:
				x.attributes['Note'].append(new_note)
			global i
			i += 1
	return x

#######################################
#        Create output database       #
#                                     #
#                                     #
#######################################

f = conf.in_db
in_db = gffutils.FeatureDB(f)

gffutils.create_db(
	in_db,
	dbfn=conf.out_db,
	force=True,
	keep_order=True, 
	merge_strategy='merge',
	transform=transform_func, 
	sort_attribute_values=True
	)
	
print("Number of features with notes added:\t" + str(i))