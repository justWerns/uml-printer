package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class AttributeNode extends AbstractNode {
    public AttributeNode(List<Object> parsetree) {
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
                if (!obj.equals(";")) {
                    out.append(' ');
                }
            } else {
                out.append(AbstractNode.buildNode(
                    (List) obj).printUMLIndented());
            }
        }
        return out.toString();
    }

    @Override
    public String printUMLJaws()
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder();
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String)
                out.append(obj);
            else
                out.append(AbstractNode.buildNode(
                    (List) obj).printUMLJaws());
            }
        return out.toString();
    }
} // end AttributeNode
