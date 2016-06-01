package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class TrivialNode extends AbstractNode {
    public TrivialNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder output = new StringBuilder();
        for (Object obj : parsetree) {
            if (obj instanceof String) {
                output.append(obj);
                output.append(' ');
            } else {
                output.append(
                    AbstractNode.buildNode((List<?>) obj).printUMLIndented());
                output.append('\n');
            } // end if
        } // end for
        return output.toString();
    } // end printUMLIndented

    @Override
    public String printUMLJaws()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        StringBuilder output = new StringBuilder();
        for (Object obj : parsetree) {
            if (obj instanceof String) {
                output.append(obj);
                output.append(' ');
            } else {
                output.append(
                    AbstractNode.buildNode((List<?>) obj).printUMLJaws());
                output.append('\n');
            } // end if
        } // end for
        return output.toString();
    } // end printUMLJaws
} // end TrivialNode
