package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class CallNode extends AbstractNode {
    public CallNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder out = new StringBuilder(getIndent());
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                String objStr = (String) obj;
                out.append(objStr);
                if (!"();".contains(objStr) && !objStr.contains(".")) {
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
        return "STUB";
    } // end printUMLJaws
}
