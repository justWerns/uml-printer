package umlprinter;

import java.util.List;

public class CommentNode extends AbstractNode {
    public CommentNode(List<Object> parsetree) {
        super(parsetree);
    } // end constructor

    @Override
    public String printUMLIndented() {
        StringBuilder out = new StringBuilder(getIndent());
        for (Object obj : parsetree) {
            out.append(obj);
        }
        return out.toString();
    }
} // end CommentNode
