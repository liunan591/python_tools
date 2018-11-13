# -*- coding: utf-8 -*-

import csv

#%%read
def read_to_iterator(file):
    #Return: an iterator with split column     
    with open(file, mode = "r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')
        return reader
    
def read_to_list(file):
    #Return: a list with split column
    clist = list()
    with open(file, mode = "r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')
        for line in reader:
            clist.append(line)
    return clist

#%%write
def write_line_to_csv(line,csv_file,mode):
    csvfile = open(csv_file, mode)
    csvwriter = csv.writer(csvfile, quotechar='\"', lineterminator=u'\n', quoting=csv.QUOTE_ALL)
    c = map(encode_line, line)
    csvwriter.writerow(c)

def add_csv_to_csv(file,file2,tittle = True):
    with open(file, mode = "r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')
        a = 0
        if tittle: a = 1
        for line in reader:
            a = a-1
            if a ==0:continue
            if line:
                write_line_to_csv(line,file2,"a")
        print("%i item add to %s"%(0-a,file2))

#%%assistent
def encode_line(x):
    if not x:
        return u""
    return x.encode('utf-8', errors='ignore')