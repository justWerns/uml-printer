package umlprinter;

import java.io.*;
import java.util.List;

public class JawsUMLPrinter {
    private final List<Object> parsetree;
    private final String readFile;
    private final String printFile;

    JawsUMLPrinter(String readFile, String printFile)
            throws IOException, ClassNotFoundException {
        this.readFile = readFile;
        this.printFile = printFile;
        ObjectInputStream ois =
                new ObjectInputStream(new FileInputStream(readFile));
        parsetree = (List<Object>) ois.readObject();
        OutputStream outStream = new FileOutputStream(printFile);
    } // end JawsUMLPrinter

    private void run() {

    } // end run

    public static void main(String... args) {

    } // end main
} // end JawsUMLPrinter
