package umlprinter;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class NodeMap {
    private static final Map<String, Class<? extends Node>> nodeMap;
    static {
        Map<String, Class<? extends Node>> buildMap = new HashMap<>();
        buildMap.put("@", CommentNode.class);
        nodeMap = Collections.unmodifiableMap(buildMap);
    }

    public static Class<? extends Node> get(String typetag) {
        return nodeMap.get(typetag);
    }

    public static boolean validTypetag(String typetag) {
        return nodeMap.containsKey(typetag);
    }
}
