package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class MethodNode extends AbstractNode {
    public MethodNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder(getIndent());
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                out.append(obj);
                if (!obj.equals(";") && !obj.equals("(")) {
                    out.append(' ');
                }
            } else {
                List<?> subnode = (List) obj;
                if (subnode.get(0).equals("static")) {
                    out.append("static ");
                } else {
                    out.append(AbstractNode.buildNode(
                        (List) obj).printUMLIndented());
                }
            }
        }
        return out.toString();
    } // end UML indented

    @Override
    public String printUMLJaws()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder();
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                out.append(obj);
            } else {
                List<?> subnode = (List) obj;
                if (subnode.get(0).equals("static")) {
                    out.append("static ");
                } else {
                    out.append(AbstractNode.buildNode(
                        (List) obj).printUMLJaws());
                }
            }
        }
        return out.toString();
    } // end printUMLJaws
} // end MethodNode
