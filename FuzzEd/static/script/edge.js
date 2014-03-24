define(['class', 'config', 'jquery', 'jsplumb'],
function(Class, Config) {
    /**
     *  Class: {Abstract} Edge
     *
     *  Blah
     *
     */
    return Class.extend({
        id:         undefined,
        source:     undefined,
        target:     undefined,
        properties: undefined,
        graph:      undefined,

        _jsPlumbEdge: undefined,

        init: function(graph, sourceOrJsPlumbEdge, target, properties) {
            this.graph = graph;

            if (arguments.length === 2) {
                // case 1: create Edge instance for existing jsPlumbConnection (e.g. as event handler)
                this.source = sourceOrJsPlumbEdge.source;
                this.target = sourceOrJsPlumbEdge.target;
                this.properties = {};
                this._initFromJsPlumbEdge(sourceOrJsPlumbEdge);

            } else {
                // case 2: create Edge instance and create corresponding jsPlumbConnection (programmatic creation)
                this._init(sourceOrJsPlumbEdge, target, properties);
            }
        },

        _init: function(source, target, properties) {
            this.source = source;
            this.target = target;

            // having properties implies already having an id
            this.id = typeof properties.id !== 'undefined' ? this.graph.createId() : properties.id;
            this.properties = properties;

            var jsPlumbEdge = jsPlumb.connect({
                source:    source.container,
                target:    target.container,
                fireEvent: false
            });
            this._initFromJsPlumbEdge(jsPlumbEdge);
        },

        _initFromJsPlumbEdge: function(jsPlumbEdge) {
            this._jsPlumbEdge = jsPlumbEdge;

            jsPlumbEdge._fuzzedId = (typeof jsPlumbEdge._fuzzedId === 'undefined') ? this.createId() : jsPlumbEdge._fuzzedId;

            // store the ID in an attribute so we can retrieve it later from the DOM element
            jQuery(jsPlumbEdge.canvas).data(this.config.Keys.CONNECTION_ID, jsPlumbEdge._fuzzedId);

            var sourceNode = jQuery(jsPlumbEdge.source).data(this.config.Keys.NODE);
            var targetNode = jQuery(jsPlumbEdge.target).data(this.config.Keys.NODE);

            sourceNode.setChildProperties(targetNode);

            // correct target and source node incoming and outgoing edges
            sourceNode.outgoingEdges.push(jsPlumbEdge);
            targetNode.incomingEdges.push(jsPlumbEdge);

            // call home
            jQuery(document).trigger(
                this.config.Events.GRAPH_EDGE_ADDED,
                [jsPlumbEdge._fuzzedId, sourceNode.id, targetNode.id]
            );

            return this;
        }
    });
});
