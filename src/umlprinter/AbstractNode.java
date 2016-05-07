package umlprinter;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.List;

// abstract node class
public abstract class AbstractNode implements Node {
    protected final List<Object> parsetree;
    protected static int indentLevel = 0;

    public AbstractNode() {
        throw new UnsupportedOperationException(
            "A node cannot be constructed using the default constructor.");
    } // end default constructor

    public AbstractNode(List<Object> parsetree) {
        this.parsetree = parsetree;
    } // end constructor

    public abstract String printUMLIndented()
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException;

    public abstract String printUMLJaws()
            throws InvocationTargetException, NoSuchMethodException,
                   InstantiationException, IllegalAccessException;

    public void createGraph() {
        // stub to be implemented.
    } // end createGraph

    static Node buildNode(List<?> parsetree)
            throws IllegalAccessException, InstantiationException,
                   NoSuchMethodException, InvocationTargetException {
        String typetag = (String) parsetree.get(0);
        if (!NodeMap.validTypetag(typetag)) {
            throw new IllegalStateException(
                    "Found invalid typetag: " + typetag);
        } // end if
        Constructor<? extends Node> constructor =
            NodeMap.get(typetag).getConstructor(List.class);
        return constructor.newInstance(parsetree);
    } // end buildNode

    protected String getIndent() {
        return new String(new char[indentLevel * 4]).replace('\0', ' ');
    }
} // end AbstractNode
