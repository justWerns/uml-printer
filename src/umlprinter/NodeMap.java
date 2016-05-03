package umlprinter;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class NodeMap {
    private static final Map<String, Class<? extends Node>> nodeMap;

    static {
        Map<String, Class<? extends Node>> buildMap = new HashMap<>();
        buildMap.put("@", CommentNode.class);
        buildMap.put("diagram:", DiagramNode.class);
        buildMap.put("classDiagram:", DiagramNode.class); // TODO: probably wrong
        buildMap.put("class-sequence:", RootNode.class); // TODO: definitely wrong
        buildMap.put("class:", ClassNode.class);
        buildMap.put("extends", ExtendsNode.class);
        buildMap.put("class-contents:", RootNode.class);
        buildMap.put("attribute:", AttributeNode.class);
        buildMap.put("type:", TypeNode.class);
        buildMap.put("[", RootNode.class);
        buildMap.put("method:", MethodNode.class);
        buildMap.put("static", RootNode.class);
        buildMap.put("param-list:", ParamNode.class);
        buildMap.put("passedArgs", RootNode.class);
        buildMap.put("interface:", ClassNode.class);
        buildMap.put("implements", ImplementsNode.class);
        nodeMap = Collections.unmodifiableMap(buildMap);
    } // end static

    public static Class<? extends Node> get(String typetag) {
        return nodeMap.get(typetag);
    } // end get

    public static boolean validTypetag(String typetag) {
        return nodeMap.containsKey(typetag);
    } // end validTypetag
}
