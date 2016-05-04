package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.InputMismatchException;
import java.util.List;

public class ClassNode extends AbstractNode {
    // LAYOUT: (Note the first element in the parsetree is the class: typetag)
    // [visibility] class <name> [extends <parent class>]
    //                           [implements <interface>(, <interface>)*] {
    //     <contents>?
    // }
    public ClassNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented()
            throws InvocationTargetException, NoSuchMethodException,
            InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder();
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                if (obj.equals("{") || obj.equals("}")) {
                    out.append(obj).append('\n');
                } else {
                    out.append(obj).append(' ');
                }
            } else {
                List<?> subnode = (List) obj;
                if (subnode.get(0).equals("extends")
                        || subnode.get(0).equals("implements")) {
                    out.append(printInheritance(subnode));
                } else {
                    out.append(
                        AbstractNode.buildNode(subnode).printUMLIndented());
                } // end if
            } // end if
        } // end for
        return out.toString();
    } // end printUMLIndented

    private String printInheritance(List<?> subnode) {
        StringBuilder out = new StringBuilder((String) subnode.get(0));
        out.append(' ').append(subnode.get(1));
        for (int i = 2; i < subnode.size(); i++) {
            out.append(", ").append(subnode.get(i));
        } // end for
        out.append(' ');
        return out.toString();
    } // end printInheritance
} // end ClassNode
