package umlprinter;

import java.util.List;

public interface Node {
    String printUMLIndented();

    String printUMLJaws();

    void createGraph();

    static Node buildNode(List<Object> parsetree)
            throws IllegalAccessException, InstantiationException {
        String typetag = (String) parsetree.get(0);
        if (!NodeMap.validTypetag(typetag)) {
            throw new IllegalStateException(
                    "Found invalid typetag: " + typetag);
        }
        return NodeMap.get(typetag).newInstance();
    } // end buildNode
} // end Node
