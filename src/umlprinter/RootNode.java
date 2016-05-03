package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

// TODO: Pretty sure this gets replaced by the ContainerNode.
public class RootNode extends AbstractNode {
    public RootNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    public String printUMLIndented()
            throws InvocationTargetException, NoSuchMethodException,
            InstantiationException, IllegalAccessException {
        StringBuilder output = new StringBuilder();
        for (Object obj : parsetree.subList(1, parsetree.size())) {
            if (obj instanceof String) {
                output.append(obj);
            } else {
                output.append(
                    AbstractNode.buildNode((List<?>) obj).printUMLIndented());
            } // end if
            output.append('\n');
        } // end for
        return output.toString();
    }
} // end RootNode
