package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class TypeNode extends AbstractNode {
    public TypeNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented() {
        StringBuilder out = new StringBuilder(": ");
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                out.append(obj).append(' ');
            } else {
                for (Object item : (List) obj) {
                    out.append(item);
                }
                out.append(' ');
            }
        }
        out.deleteCharAt(out.length() - 1);
        return out.toString();
    } // end UML indented

    @Override
    public String printUMLJaws()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder(":");
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                out.append(obj).append(' ');
            } else {
                for (Object item : (List) obj) {
                    out.append(item);
                }
            }
        }
        out.deleteCharAt(out.length() - 1);
        return out.toString();
    } // end printUMLJaws
} // end TypeNode
