#!/usr/bin/env python3
import os
import shutil
import sqlite3

frmdir = 'C:/Users/Kees/Downloads/Glacier/'
dstdir = 'C:/Users/Kees/Pictures/'
mapping = 'mapping.sqlite3'


def move(frm, dst):
	""" Move file from source to destinatin """
	exists=[]		           # cache existing dirs
	dir = os.path.normpath(dstdir+dst) # normalize destination	
	dirname = os.path.dirname(dir)	   # fetch dirname of dst
	
	if dirname in exists:
		pass
	else:
		if not os.path.isdir(dirname):
			os.makedirs(dirname)
		exists.append(dirname)

	shutil.copyfile(frmdir+frm, dir)



def main(mapping):
	''' retrieve list of files from the mapping and move files
	    to the appropriate location
	'''
	notfound=[]
	found=[]
	conn = sqlite3.connect(mapping)

	c = conn.cursor()
	c.execute('select basePath, archiveID from file_info_tb')

	row = c.fetchone()
	while not row is None:
		if not os.path.isfile(frmdir+row[1]):
			notfound.append(row[1])
		else:
			found.append(row[1])
			move(row[1], row[0])
		row = c.fetchone()

	return found,notfound


if __name__ == "__main__":
	found,notfound = main(frmdir+'/mapping.sqlite3')
	print("{} files found and {} not found".format(
                len(found), len(notfound)))
