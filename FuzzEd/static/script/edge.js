define(['class', 'config', 'property', 'jquery', 'jsplumb'],
function(Class, Config, Property) {
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
        jsPlumbEdge: undefined,

        init: function(definition, sourceOrJsPlumbEdge, targetOrProperties, properties) {
            if (typeof properties === 'undefined') {
                // case 1: create Edge instance for existing jsPlumbConnection (e.g. as event handler)
                properties  = jQuery.extend(true, {}, definition, targetOrProperties);
                this.source = jQuery(sourceOrJsPlumbEdge.source).data(Config.Keys.NODE);
                this.target = jQuery(sourceOrJsPlumbEdge.target).data(Config.Keys.NODE);
                this._initFromJsPlumbEdge(sourceOrJsPlumbEdge, properties);

            } else {
                // case 2: create Edge instance and create corresponding jsPlumbConnection (programmatic creation)
                properties = jQuery.extend(true, {}, definition, properties);
                this._init(sourceOrJsPlumbEdge, targetOrProperties, properties);
            }
        },

        _init: function(source, target, properties) {
            this.source = source;
            this.target = target;

            var jsPlumbEdge = jsPlumb.connect({
                source:    source.container,
                target:    target.container,
                fireEvent: false
            });
            jsPlumbEdge._fuzzedId = this.id;
            this._initFromJsPlumbEdge(jsPlumbEdge, properties);
        },

        _initFromJsPlumbEdge: function(jsPlumbEdge, properties) {
            this.jsPlumbEdge = jsPlumbEdge;
            this.jsPlumbEdge._fuzzedId = this.id;

            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;
            this.properties = jQuery.extend(true, {}, properties);
            delete this.properties.id;
            delete this.properties.graph;

            // store the edge instance in an attribute so we can retrieve it later from the DOM element
            jQuery(jsPlumbEdge.canvas).data(Config.Keys.EDGE, this);
            this.source.setChildProperties(this.target);

            // correct target and source node incoming and outgoing edges
            this.source.outgoingEdges.push(this);
            this.target.incomingEdges.push(this);

            this._setupProperties();

            // call home
            jQuery(document).trigger(Config.Events.EDGE_ADDED, [this.id, this.source.id, this.target.id]);
        },

        select: function() {
            jQuery(this.jsPlumbEdge.canvas).addClass(Config.Classes.SELECTED);
        },

        remove: function() {
            // To cover both the case that the jsPlumbEdge was already detached and that it wasn't we detach it again
            jsPlumb.detach(this.jsPlumbEdge);

            if (typeof this.target === 'undefined') return false;
            this.source.restoreChildProperties(this.target);

            // correct target and source node incoming and outgoing edges
            this.source.outgoingEdges = _.without(this.source.outgoingEdges, this);
            this.target.incomingEdges = _.without(this.target.incomingEdges, this);

            // call home
            jQuery(document).trigger(Config.Events.EDGE_DELETED, this.id);

            return true;
        },

        toDict: function() {
            return {
                id:           this.id,
                sourceNodeId: this.source.id,
                targetNodeId: this.target.id,
                properties:   this.properties //TODO: make it right
            }
        },

        /**
         * Method: _setupProperties
         *
         * Returns:
         *   This {<Edge>} instance for chaining.
         */
        _setupProperties: function() {
            _.each(this.graph.getNotation().propertiesDisplayOrder, function(propertyName) {
                var property = this.properties[propertyName];

                if (typeof property === 'undefined') {
                    return;
                } else if (property === null) {
                    delete this.properties[propertyName];
                    return;
                }

                property.name = propertyName;
                this.properties[propertyName] = Property.from(this, property);
            }.bind(this));

            return this;
        }
    });
});
