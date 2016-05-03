package umlprinter;

import java.lang.reflect.InvocationTargetException;

public interface Node {
    String printUMLIndented() throws InvocationTargetException, NoSuchMethodException, InstantiationException, IllegalAccessException;

    String printUMLJaws();

    void createGraph();
} // end Node
