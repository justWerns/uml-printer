package umlprinter;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class NodeMap {
    private static final Map<String, Class<? extends Node>> nodeMap;

    static {
        Map<String, Class<? extends Node>> buildMap = new HashMap<>();
        buildMap.put("@", CommentNode.class);
        buildMap.put("diagram:", ContainerNode.class);
        buildMap.put("classDiagram:", DiagramNode.class);
        buildMap.put("class-sequence:", ContainerNode.class);
        buildMap.put("class:", ClassNode.class);
        buildMap.put("class-contents:", ContainerNode.class);
        buildMap.put("attribute:", AttributeNode.class);
        buildMap.put("type:", TypeNode.class);
        buildMap.put("method:", MethodNode.class);
        buildMap.put("static", TrivialNode.class);
        buildMap.put("param-list:", ParamNode.class);
        buildMap.put("interface:", ClassNode.class);
        nodeMap = Collections.unmodifiableMap(buildMap);
    } // end static block

    public static Class<? extends Node> get(String typetag) {
        return nodeMap.get(typetag);
    } // end get

    public static boolean validTypetag(String typetag) {
        return nodeMap.containsKey(typetag);
    } // end validTypetag
} // end NodeMap
