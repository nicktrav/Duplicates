#!/usr/bin/python
# Nick Travers, 2011

import sys, os
import hashlib
import re

def chunk_reader(fobj, chunk_size=128):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def hash_file(abs_path):
    """A function to hash a file based on its contents"""
    h = hashlib.sha1()
    
    # try to open the file 
    try:
        f.open(abs_path, 'rb')
    except IOError:
        print 'Could not open file %s' % abs_path
        return None
    
    # read the contents of the file
    data = f.read()

    # update the hash
    h.update(data)

    # return the hash
    return h.hexdigest()


def main():
    dict_files = {}
    list_duplicates = []
    duplicates = 0
    
    path = '/Users/nick/Documents/Dropbox/Developer/Duplicates/Tests/'

    current_dir = ''

    try:
        if sys.argv[1] == '-v':
            DEBUG = True
    except:
        DEBUG = False

    for root, dirs, files in os.walk(path):

        for filename in files:
            full_path = root + '/' + filename

            if os.path.split(full_path)[1][0] == '.':
                continue

            res = re.search(r'.*\/\.(\w+).*',os.path.split(full_path)[0])
            try:
                if res.groups() != None:
                    continue
            except:
                pass

            if DEBUG and os.path.split(full_path)[0] != current_dir:
                print current_dir
                current_dir = os.path.split(full_path)[0]

            try:
                f = open(full_path, 'rb')
            except IOError:
                continue
                
            h = hashlib.sha1()
            try:
                byte = f.read(128)
                while byte != "":
                    # Do stuff with byte
                    h.update(byte)
                    byte = f.read(128)
            finally:
                f.close()

            sha1 = h.hexdigest()
                    
            if sha1 not in dict_files:
                dict_files[sha1] = []
                dict_files[sha1].append(os.path.abspath(full_path))
            else:
                duplicates += 1
                dict_files[sha1].append(os.path.abspath(full_path))

                list_duplicates.append(sha1)
    
    print 'Found %d duplicates.' % duplicates
    
    for duplicate in list_duplicates:
        print (duplicate, dict_files[duplicate])

if __name__ == '__main__':
    main()