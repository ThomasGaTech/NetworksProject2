# Script to validate output for OMS 6250 Project 2  
# Based on Project 2 Autograder by Michael Brown
# Copyright 2017 Kelly Parks 

import os
import getopt
import sys
import decimal

#Helper Function: Opens a logfile and reads line by line 
#                 Returns a dictionary representing the final result
#		  Key will be switch ID
#		  Entry will be the entire line in file to ensure correct order is used
def getResultFromLog(filename):
   with open(filename) as f:
      st = {}
      for line in f:
	    line = line.rstrip()
	    line = line.replace(" ","")
	    if line != "":
                label = ""
                label = line.split("-")[0]
                st[label] = line.split(",")           
   return st 

#Helper Function: Checks two output dictionaries for equivalence
#Returns True if the two topologies are equivalent, False if not.
def tablesEquivalent(refST, studentST):
   #Shallow Check - do both STs have the same number of key value pairs?
   if len(refST) != len(studentST):
      print "Different number of lines present in two files"
      return False
   else:
      #Ensure all nodes in reference are present in student log
      for node in refST:
         if studentST.has_key(node):
	    for entry in refST[node]:
	    	if entry not in studentST[node]:
		    print "Link " + entry + " missing from student spanning tree" 
	            return False
         else:
	    print "Switch " + node + " missing in student spanning tree"
            return False
      #Ensure all nodes in student log are present in reference log 
      for node in studentST: 
	 if refST.has_key(node):
	    for entry in studentST[node]:
	        if entry not in refST[node]:
		    print "Link " + entry + " extra in student spanning tree"
		    return False
	 else:
	    print "Switch " + node + " extra in student spanning tree"
            return False
   return True

def main(argv):
    student_file = ' '
    ref_file = ' '
    try:
        opts, args = getopt.getopt(argv,"s:r:",["student_file=","ref_file="])
    except getopt.GetoptError:
        print 'ValidateAnswer.py -s <student_file> -r <ref_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--student_file"):
           student_file = arg
        elif opt in ("-r", "--ref_file"):
           ref_file = arg
    refST1 = getResultFromLog(ref_file)
    studentST1 = getResultFromLog(student_file)

    comp = tablesEquivalent(refST1, studentST1)

if __name__ == "__main__":
   main(sys.argv[1:])

