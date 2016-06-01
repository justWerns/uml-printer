package umlprinter;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class JawsUMLPrinter {
    private final List<?> parsetree;
    private final PrintWriter outStream;

    private JawsUMLPrinter(String readFile, String printFile)
            throws IOException, ClassNotFoundException {
        ObjectInputStream ois =
                new ObjectInputStream(new FileInputStream(readFile));
        parsetree = (List<?>) ois.readObject();
        this.outStream = new PrintWriter(printFile);
    } // end JawsUMLPrinter

    private void run(String printType)
            throws InstantiationException, IllegalAccessException, NoSuchMethodException, InvocationTargetException {
        Node base = AbstractNode.buildNode(parsetree);
        switch (printType) {
            case "jaws":
                outStream.print(base.printUMLJaws());
                break;
            case "indented":
                outStream.print(base.printUMLIndented());
                break;
            case "graph":
                System.out.println(
                        "Diagram creation has not been implemented yet.");
                break;
            default:
                System.out.println(
                        "Invalid print type given. Restart the program with one "
                        + "of the following print types: jaws, indented, graph"
                );
                break;
        } // end switch
        outStream.close();
    } // end run

    private static JawsUMLPrinter createPrinter(String... args) {
        try {
            return new JawsUMLPrinter(args[1], args[2]);
        } catch (IOException iox) {
            System.err.println(
                    "An IO error occured while creating the printer: "
                            + iox.getMessage()
            );
        } catch (ClassNotFoundException cnfx) {
            System.err.println(
                    "Class not found while creating the printer: "
                            + cnfx.getMessage()
            );
        } // end try-catch
        return null;
    } // end createPrinter

    public static void main(String... args)
            throws IllegalAccessException, InstantiationException, NoSuchMethodException, InvocationTargetException {
        final String USAGE = "java JawsUMLPrinter PRINTTYPE INFILE OUTFILE";
        JawsUMLPrinter printer;

        if (args.length != 3) {
            System.err.println(USAGE);
            System.exit(1);
        } // end if

        printer = createPrinter(args);
        if (printer == null) {
            System.out.println(
                    "An error occurred while creating the "
                    + "printer. Please see error output."
            );
            System.exit(1);
        } // end if
        printer.run(args[0]);
    } // end main
} // end JawsUMLPrinter
