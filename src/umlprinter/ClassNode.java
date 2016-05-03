package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.InputMismatchException;
import java.util.List;

public class ClassNode extends AbstractNode {
    private int contentIdx = 0;
    public ClassNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        if (!validateParsetree()) {
            throw new InputMismatchException(
                "Found class node with unexpected content. Is this a parse "
                + "error, or does the node need to be updated?"
                + parsetree.get(2)
            );
        } // end if
        StringBuilder output = new StringBuilder();
        output.append("class ")
              .append(parsetree.get(2))
              .append(' ');
        output.append(getInheritanceStr());
        output.append("{\n");
        if (contentIdx > 0) {
            output.append(AbstractNode.buildNode(
                (List) parsetree.get(contentIdx)).printUMLIndented());
        } // end for
        output.append("}\n");
        return output.toString();
    } // end printUMLIndented

    // LAYOUT: (Note the first element in the parsetree is the class: typetag)
    // class <name> [extends <parent class>]
    //              [implements <interface>(, <interface>)*] {
    //     <contents>?
    // }
    private boolean validateParsetree() {
        int pos = 1;
        boolean valid = parsetree.size() >= 5
                        && parsetree.get(pos++).equals("class")
                        && parsetree.get(pos++) instanceof String;
        for (; valid && pos < 5 && parsetree.get(pos) instanceof List; pos++) {
            List<?> subnode = (List) parsetree.get(pos);
            if (!(
                    subnode.get(0).equals("extends")
                    || subnode.get(0).equals("implements"))) {
                throw new InputMismatchException(
                    "Received an invalid subnode in the extends/implements "
                    + "section of " + parsetree.get(2) + "'s class node."
                );
            } // end if
        } // end for
        valid = valid && parsetree.get(pos++).equals("{");
        if (!(parsetree.get(pos) instanceof String)) {
            contentIdx = pos;
            if (!((List) parsetree.get(pos++)).get(0)
                                                 .equals("class-contents:")) {
                throw new InputMismatchException(
                    "Received an invalid subnode where class-contents "
                    + "should be in the " + parsetree.get(2) + "class."
                );
            } // end if
        } // end if
        return valid
               && pos == parsetree.size() - 1
               && parsetree.get(pos).equals("}");
    } // end validateParsetree

    private String getInheritanceStr() {
        // TODO: Rewrite this function to not be stupid
        Object nextToken = parsetree.get(3);
        if (nextToken instanceof String) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        List<?> subnode = (List) nextToken;
        if (subnode.get(0).equals("extends")) {
            out.append("extends ").append(subnode.get(1)).append(' ');
            nextToken = parsetree.get(4);
        }
        if (nextToken instanceof String) {
            return out.toString();
        }
        subnode = (List) nextToken;
        out.append("implements ").append(subnode.get(1));
        for (int i = 2; i < subnode.size(); i++) {
            out.append(", ").append(subnode.get(i));
        }
        return out.append(' ').toString();
    }

} // end ClassNode
