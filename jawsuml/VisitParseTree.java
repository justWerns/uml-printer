import java.util.List ;
import java.io.* ;

/**
 *  VisitParseTree visits a UML diagram description parse tree
 *  created by PyToJava.py and prints out the nestingLevel::typeTag
 *  for each node in the parse tree.
 *  D. Parson Spring 2016
**/
public class VisitParseTree {
    private static List deserializeTree(String filename) {
        try {
            FileInputStream filein = new FileInputStream(filename);
            ObjectInputStream oostream = new ObjectInputStream(filein);
            List jtree = (List) oostream.readObject();
            oostream.close();
            return jtree ;
        } catch (Exception exx) {
            String msg = "ERROR DESERIALIZING FILE " + filename
                + ": " + exx.getClass().getName() + ", "
                + exx.getMessage();
            System.err.println(msg);
            throw new RuntimeException(msg);
        }
    }
    private static void printTree(List jtree, int level) {
        Object firstobj = jtree.get(0);
        if (firstobj instanceof String) {
            System.out.println("" + level + "::" + (String) firstobj);
        } else {
            System.out.println("" + level + "::LIST::" + firstobj.toString());
        }
        for (Object o : jtree) {
            if (o instanceof List) {
                printTree((List)o, level+1);
            }
        }
    }
    private static final String usage =
        "USAGE: java VisitParseTree FILE_WITH_PARSE_TREE";
    public static void main(String [] args) {
        if (args.length < 1) {
            throw new RuntimeException(usage);
        }
        for (int i = 0 ; i < args.length ; i++) {
            printTree(deserializeTree(args[i]),1);
        }
    }
}
