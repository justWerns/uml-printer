package umlprinter;

import java.lang.reflect.InvocationTargetException;
import java.util.InputMismatchException;
import java.util.List;

public class DiagramNode extends AbstractNode {
    public DiagramNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    public String printUMLIndented()
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException {
        if (!validateDiagramSyntax()) {
            throw new InputMismatchException(
                "Found diagram node with unexpected content. Is this a parse "
                + "error or does the node need to be updated?"
            );
        } // end if
        StringBuilder output = new StringBuilder();
        String diagramType = (String) parsetree.get(0);
        output.append(diagramType.substring(0, diagramType.length() - 1))
              .append(' ')
              .append(parsetree.get(1))
              .append(" {\n");
        for(int i = 3; i < parsetree.size() - 1; i++) {
            output.append(AbstractNode.buildNode(
                (List<?>) parsetree.get(i)).printUMLIndented());
            output.append('\n');
        } // end for
        output.append("}\n");
        return output.toString();
    } // end printUMLIndented

    private boolean validateDiagramSyntax() {
        boolean valid =
               parsetree.size() >= 4
               && parsetree.get(0) instanceof String
               && parsetree.get(1) instanceof String
               && parsetree.get(2) instanceof String
               && parsetree.get(parsetree.size() - 1) instanceof String;
        for(int i = 3; valid && i < parsetree.size() - 1; i++) {
            valid = parsetree.get(i) instanceof List;
        } // end for
        return valid;
    } // end validateDiagramSyntax
} // end DiagramNode
