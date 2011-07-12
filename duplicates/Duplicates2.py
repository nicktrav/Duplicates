import os
import sys
import re
import hashlib
import getopt

# test the timing
import timeit

# Globals
_BUFFER_SIZE = 128

def hash_file(abs_path):
    """A function to hash a file based on its contents"""
    h = hashlib.sha1()
    
    # try to open the file 
    try:
        f = open(abs_path, 'rb')
    except IOError:
        print 'Could not open file %s' % abs_path
        return None
    
    # read the contents of the file
    byte = f.read(_BUFFER_SIZE)
    while byte != "":
        # update the hash
        h.update(byte)
        # get the next chunk of data
        byte = f.read(_BUFFER_SIZE)

    # close the file
    f.close()

    # return the hash
    return h.hexdigest()

def hash_file_whole(abs_path):
    """
    Hash the whole file at once
    """
    """A function to hash a file based on its contents"""
    h = hashlib.sha1()
    
    # try to open the file 
    try:
        f = open(abs_path, 'rb')
    except IOError:
        print 'Could not open file %s' % abs_path
        return None

    # read in the data
    data = f.read()

    # update the hash
    h.update(data)

    # close the file
    f.close()

    # return the hash
    return h.hexdigest()

def check_file(abs_path):
    """Check to see if the file should be hashed.
    - Files such as /path/to/.file/ should be excluded.
    - Files with a preceeding '.' should also be exclude.
    Returns 'True' if file to be checked, 'False' otherwise.
    Assumes 'True' as a default.
    """
    # check for a dot in the filename
    filename = os.path.split(abs_path)
    if filename[1][0] == '.':
        return False

    # check for a '.' in the path
    result = re.search(r'\/\.', os.path.split(abs_path)[0])
    if result != None:
        return False
    
    return True

def print_summary(list_duplicates, dict_files, output):
    """
    Print out a summary.
    """
    # Display the number of duplicates
    total = 0
    for duplicate in list_duplicates:
        total += len(dict_files[duplicate])
    
    # adjust for original occurence of file
    total -= len(list_duplicates)

    if total != 0:
        print 'Found %d duplicate files!\n' % total        
    else:
        print 'No duplicates found.\n'

def list_files(list_duplicates, dict_files, output):
    """
    Print out a list of the duplicate files
    """
    # if outputting to file, open the file
    if output[0] == True:
        try:
            f = open(output[1], 'w')
        except IOError:
            print 'Could not print to file!'
            output[0] = False

    print "------ Summary ------"

    for item in list_duplicates:
        
        duplicate_files = dict_files[item]
        
        # print the original file
        print "%s" % duplicate_files[0]
        if output[0] == True:
            f.write("%s\n" % duplicate_files[0])
        
        # print the other files
        for other in duplicate_files[1:]:
            print "\t--> %s" % other
            if output[0] == True:
                f.write("\t--> %s\n" % other)

    # if file was open, close it
    if output[0] == True:
        print '\nSummary printed to file: %s' % output[1]
        f.close()

def Duplicates():
    # set DEBUG to be 'False' by default
    DEBUG = False

    # the empty dictionary to hold all of the hashed files
    dict_files = {}
    # a list for the duplicate files
    list_duplicates = []
    # a count of the number of duplicate files found
    duplicates = 0
    # output to file should be off by default
    output = (False, '')

    # parse the command line arguments
    try:
        optlist, args = getopt.getopt(sys.argv[1:],'vd:o:')
    except:
        print 'Usage: Duplicates [-v] [-o] filename [-d] directory'
        return
    
    # look for elements in the opl list
    for o,a in optlist:
        
        if o == '-v':
            DEBUG = True
        
        if o == '-d':
            path = a
        
        if o == '-o':
            output = (True, a)

    # iterate through the directories
    for root, dirs, files in os.walk(path):
        if DEBUG == True:
            print root
        
        # for each file in the directory
        for filename in files:

            # generate the full path name
            full_path = root + '/' + filename


            # print the file name, if DEBUG == True
            if DEBUG == True:
                print '\t%s' % full_path
            
            # should the file be included??
            check = check_file(full_path)
            
            # generate the hash
            if check == True:
                hash_val = hash_file(full_path)
            else:
                continue
                    
            # check if the file is already in the hash list
            if hash_val not in dict_files:
                dict_files[hash_val] = []
                dict_files[hash_val].append(os.path.abspath(full_path))
            else:
                duplicates += 1
                dict_files[hash_val].append(os.path.abspath(full_path))

                list_duplicates.append(hash_val)
    
    # print out summary information
    print_summary(list_duplicates, dict_files, output)

    # list the files
    list_files(list_duplicates, dict_files, output)

if __name__ == '__main__':
    t = timeit.Timer("Duplicates()", "from __main__ import Duplicates")
    print 'Took: %s seconds' % t.timeit(1)