define(['class', 'config', 'property', 'jquery', 'jsplumb'],
function(Class, Config, Property) {
    /**
     * Package: Base
     */

    /**
     * Class: {Abstract} Edge
     *      This class models a generic connection of two nodes, further specified in the respective notations file.
     *
     *  This class models a generic connection of two nodes, further specified in the respective notations file.
     *
     */
    return Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *      {int}        id              - A client-side generated id to uniquely identify the edge in the frontend.
         *                                     It does NOT correlate with database ids in the backend. Introduced to
         *                                     save round-trips and to later allow for an offline mode.
         *      {<Node>}     source          - The source Node instance
         *      {<Node>}     target          - The target Node instance
         *      {Object}     properties      - A dictionary of the edge's properties
         *      {<Graph>}    graph           - The Graph this edge belongs to.
         *      {DOMElement} jsPlumbEdge     - The responsible jsPlumbEdge connecting source and target
         *
         */
        id:         undefined,
        source:     undefined,
        target:     undefined,
        properties: undefined,
        graph:      undefined,
        jsPlumbEdge: undefined,

        /**
         * Constructor: init
         *      Merges the given definition and properties into the object. When called with _four_ arguments, they are
         *      interpreted as (definition, source, target, properties). This is for a programmatic creation of an Edge,
         *      where jsPlumb has yet to be informed about the connection to create a jsPlumbEdge. When called with
         *      _three_ arguments though, they are interpreted as (definition, jsPlumbEdge, properties). This is
         *      supposed to just create the Edge model object for an existing jsPlumbEdge, e.g. when manually creating a
         *      connection by drag and drop. In either case, _initFromJsPlumbEdge is called afterwards.
         *
         * Parameters:
         *      {Object} definition - An object containing default values for the node's definition.
         *      [...]
         *      {Object} properties - A key-value declaration of the edge's properties. See also the notation files.
         *
         */
        init: function(definition, sourceOrJsPlumbEdge, targetOrProperties, properties) {
            jQuery.extend(this, definition);

            if (typeof properties === 'undefined') {
                // case 1: create Edge instance for existing jsPlumbConnection
                properties  = jQuery.extend(true, {}, definition.properties, targetOrProperties);
                this.source = jQuery(sourceOrJsPlumbEdge.source).data(Config.Keys.NODE);
                this.target = jQuery(sourceOrJsPlumbEdge.target).data(Config.Keys.NODE);
                this._initFromJsPlumbEdge(sourceOrJsPlumbEdge, properties);

            } else {
                // case 2: create Edge instance and create corresponding jsPlumbConnection (programmatic creation)
                properties = jQuery.extend(true, {}, definition.properties, properties);
                this._init(sourceOrJsPlumbEdge, targetOrProperties, properties);
            }
        },

        /**
         * Method: _init
         *      Acts as a follow up for the constructor in case there is no jsPlumbConnection yet. Connects source and
         *      target with jsPlumb's API and prevents the jsPlumbConnection-Event to circumvent another call of an
         *      Edge constructor by the <Editor>.
         *
         * Parameters:
         *      {<Node>} source             - source Node instance
         *      {<Node>} target             - target Node instance
         *      {Object} properties         - properties to be used
         */
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

        /**
         * Method: _initFromJsPlumbEdge
         *      Acts as a follow up for the constructor in either case. Stores the jsPlumbEdge as a member and
         *      serializes properties. Gives the Edge a unique frontend id, if it doesn't have one already. Calls home.
         *
         * Parameters:
         *      {DOMElement} jsPlumbEdge - jsPlumbEdge to be stored
         *      {Object}     properties  - properties to be used
         */
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
            jQuery(document).trigger(Config.Events.EDGE_ADDED, [
                this.id,
                this.source.id,
                this.target.id,
                this.toDict().properties
            ]);
        },

        /**
         * Method: _setupProperties
         *      Converts the informal properties stored in <properties> into Property objects ordered by this graph's
         *      propertiesDisplayOrder (see <Graph::getNotation()> or the respective notations json-file).
         *
         *      Note: Exact duplication of the code in <Node::_setupProperties()>
         *
         * Parameters:
         *      {Array[str]} propertiesDisplayOrder - The order in which to create the properties.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
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
                this.properties[propertyName] = this.factory.getClassModule('Property').from(this.factory, this, [], property);
            }.bind(this));

            return this;
        },

        /**
         * Method: select
         *      Marks the edge as selected by adding the corresponding CSS class.
         *
         * Returns:
         *      This {<Edge>} instance for chaining.
         */
        select: function() {
            jQuery(this.jsPlumbEdge.canvas).addClass(Config.Classes.SELECTED);

            return this;
        },

        /**
         * Method: highlight
         *      Marks the edge as being hovered (hovering class is added).
         *
         * Returns:
         *      This {<Edge>} instance for chaining.
         */
        highlight: function(){
            this.jsPlumbEdge.setHover(true);
            
            return this
        },
        
        /**
         * Method: unhighlight
         *      Removes hovering class from the Edge.
         *
         * Returns:
         *      This {<Edge>} instance for chaining.
         */
        unhighlight: function(){
            this.jsPlumbEdge.setHover(false);
            
            return this
        },
        
        /**
         * Method: remove
         *      Removes the whole visual representation from the canvas, restores child properties and calls home.
         *
         * Returns:
         *      {boolean} Successful deletion.
         */
        remove: function() {
            if (!this.deletable) return false;

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

        /**
         * Method: toDict
         *      Serializes the edge to a key-value representation.
         *
         * Returns:
         *      An {Object} representation of the edge avoiding any circular structures.
         */
        toDict: function() {
            var properties = _.map(this.properties, function(prop) { return prop.toDict() });

            return {
                id:           this.id,
                sourceNodeId: this.source.id,
                targetNodeId: this.target.id,
                properties:   _.reduce(properties, function(memo, prop) { return _.extend(memo, prop);}, {})
            }
        }
    });
});
