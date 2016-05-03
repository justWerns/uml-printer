package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class ParamNode extends AbstractNode {
    public ParamNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    public String printUMLIndented()
            throws InvocationTargetException, NoSuchMethodException,
            InstantiationException, IllegalAccessException {
        StringBuilder output = new StringBuilder();
        for (Object obj : parsetree) {
            if (obj instanceof String) {
                output.append(obj);
            } else {
                output.append(printParam((List<?>) obj));
            } // end if
            output.append(' ');
        }
        return output.toString();
    } // end printUMLIndented

    private String printParam(List<?> param)
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException {
        return param.get(0)
            + " : "
            + AbstractNode.buildNode((List<?>) param.get(1)).printUMLIndented();
    } // end printParam
} // end ClassNode
