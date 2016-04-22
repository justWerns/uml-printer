# -----------------------------------------------------------------------------
# PyToJava.py   Reads a Python parse tree file created by JawsUMLparser.py
#               and writes it to a java serializable file as a collection
#               of nested LinkedList and String objects.

import sys
import pprint
from java.lang import String
from java.util import LinkedList
from java.io import FileOutputStream, ObjectOutputStream,   \
    FileInputStream, ObjectInputStream

def serializeTree(parsetree, filename):
    '''
    Serialize the Python parsetree consisting up tuples and strings
    into Java LinkedList and String objects, and save into filename.
    '''
    def p2j(subtree):
        if type(subtree) == str:
            return String(subtree)
        elif type(subtree) == tuple:
            l = LinkedList()
            for entry in subtree:
                l.add(p2j(entry))
            return l
        else:
            raise ValueError, ("ERROR, bad type in parse tree: "
                + str(type(subtree)))
    jtree = p2j(parsetree)
    fileout = FileOutputStream(filename)
    oostream = ObjectOutputStream(fileout)
    oostream.writeObject(jtree)
    oostream.close()

def deserializeTree(filename):
    ''' For testing purposes, load & print a Java object parsetree. '''
    filein = FileInputStream(filename)
    oostream = ObjectInputStream(filein)
    jtree = oostream.readObject()
    oostream.close()
    f = open(filename + ".debug", 'w')
    deepstr = pprint.pformat(jtree, indent=4, width=80)
    f.write("TESTING JAVA OBJ:\n" + str(deepstr) + '\n')
    f.close()

if __name__=='__main__':
    usage = \
      "python|jython PyToJava.py PARSETREEFILE"
    if len(sys.argv) != 2:
        sys.stderr.write(usage + '\n')
        sys.exit(1)
    else:
        exec("from " + sys.argv[1] + " import parsetree")
        serializeTree(parsetree, sys.argv[1] + ".jobj")
        deserializeTree(sys.argv[1] + ".jobj")
