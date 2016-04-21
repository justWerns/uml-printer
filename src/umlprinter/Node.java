package umlprinter;

import java.util.List;

public interface Node {
    String printUMLIndented();
    String printUMLJaws();
    void createGraph();
    static Node buildNode(List<Object> parsetree) {
        return new RootNode();
    }
}
