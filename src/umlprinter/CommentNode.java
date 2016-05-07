package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class CommentNode extends AbstractNode {
    public CommentNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented() {
        StringBuilder out = new StringBuilder("\n");
        out.append(getIndent());
        for (Object obj : parsetree) {
            out.append(obj);
        }
        return out.append('\n').toString();
    }

    @Override
    public String printUMLJaws()
        throws InvocationTargetException, NoSuchMethodException,
        InstantiationException, IllegalAccessException {
        return "STUB";
    } // end printUMLJaws
} // end CommentNode
