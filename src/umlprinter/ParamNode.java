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
        output.append(printParam((List<?>) parsetree.get(1)));
        for (Object obj : parsetree.subList(2, parsetree.size())) {
            output.append(", ");
            output.append(printParam((List<?>) obj));
        } // end for
        return output.toString();
    } // end printUMLIndented

    private String printParam(List<?> param)
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException {
        return (String) param.get(0) + ' '
            + AbstractNode.buildNode((List<?>) param.get(1)).printUMLIndented();
    } // end printParam
} // end ParamNode
