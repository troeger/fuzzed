define(['factory', 'property', 'class', 'canvas', 'config', 'jquery', 'd3'],
function(Factory, Property, Class, Canvas, Config) {
    /**
     * Package: Base
     */

    /**
     * Abstract Class: NodeGroup
     *
     *  This class models a generic group of nodes, further specified in the respective notations file.
     */
    return Class.extend({
        /**
         * Group: Members
         *      {DOMElement}    container       - A jQuery object referring to the node group's html representation.
         *      {<Graph>}       graph           - The Graph this node group belongs to.
         *      {Number}        id              - A client-side generated id to uniquely identify the node group in the
         *                                        frontend. It does NOT correlate with database ids in the backend.
         *                                        Introduced to save round-trips and to later allow for an offline mode.
         *      {Array[<Node>]} nodes           - Enumeration of all nodes this node group belongs to
         *      {Object}        properties      - A dictionary of the node group's properties
         *
         */
        graph:         undefined,
        id:            undefined,
        nodes:         undefined,
        properties:    undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *      A node group's constructor. Merges the given definition and individual properties. Assigns the node
         *      group a unique client id.
         *
         * Parameters:
         *      {Object}       definition - An object containing default values for the node's definition.
         *      {Array[<Node>] nodes      - A list of nodes the node group is supposed to connect.
         *      {Object}       properties - Initial properties to be carried into the NodeGroup object
         *
         */
        init: function(definition, nodes, properties) {
            jQuery.extend(this, definition);

            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition.properties, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;

            _.each(this.nodes, function(node) {
                node.addToNodeGroup(this);
            }.bind(this));

            delete this.properties.id;
            delete this.properties.graph;

            this._setupProperties();

            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODEGROUP_ADDED, [
                this.id,
                this.nodeIds(),
                this.toDict().properties,
                this
            ]);
        },

        /**
         * Method: _setupProperties
         *      Creates the node's properties instances sorted by the passed display order. If a property passed in the
         *      display order is not present in the node it is skipped silently. When a property in the node's
         *      definition is set to null the property is not created and eventually removed if inherited from its
         *      parent.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */
        _setupProperties: function() {
            _.each(Factory.getNotation().propertiesDisplayOrder, function(propertyName) {
                var property = this.properties[propertyName];

                if (typeof property === 'undefined') {
                    return;
                } else if (property === null) {
                    delete this.properties[propertyName];
                    return;
                }

                property.name = propertyName;
                this.properties[propertyName] = Factory.getModule('Property')
                                                            .from(this, [ this ], property);
            }.bind(this));

            return this;
        },
        
        /**
         * Method: addNode
         *      Adds a node instance to the node group and forwards the add operation to the node..
         *
         * Parameters:
         *      {Node} node - the node to be added.
         *
         * Returns:
         *      This {NodeGroup} instance for chaining.
         */
        addNode: function(node) {
            node.addToNodeGroup(this);
            return this._addNode(node);
        },

        /**
         * Method: _addNode
         *      Internal method that does the actual addition of a node instance to the node group. addNode should be
         *      called from outside, since it also establishes the double link with the node instance.
         *
         * Parameters:
         *      {Node} node - the node instance to be added.
         *
         * Returns:
         *      This {NodeGroup} for chaining.
         */
        _addNode: function(node) {
            this.nodes[node.id] = node;
            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODEGROUP_NODEIDS_CHANGED, [this.id, this.nodeIds()]);

            return this;
        },

        /**
         * Method: removeNode
         *      Removes a given node instance from the node group.
         *
         * Parameters:
         *      {Node} node - the node instance to be removed
         *
         * Returns:
         *      This {NodeGroup} instance for chaining.
         */
        removeNode: function(node) {
            delete this.nodes[node.id];

            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODEGROUP_NODEIDS_CHANGED, [this.id, this.nodeIds()]);

            // if we have less than two members left, remove us, as we are no longer relevant
            if (_.size(this.nodes) < 2) {
                this.graph.deleteNodeGroup(this);
            }

            return this;
        },

        /**
         * Method: nodeIds
         *      Used for lightweight node identification.
         *
         * Returns:
         *      An array {Array[Number]} of all nodes' ids, the NodeGroup holds.
         *
         */

        nodeIds: function() {
            return _.map(this.nodes, function(node) { return node.id });
        },

        /**
         * Method: select
         *      Marks the node group as selected by adding the corresponding CSS class.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */
        select: function() {
            this.path().addClass(Factory.getModule('Config').Classes.SELECTED);

            return this;
        },

        /**
         * Method: highlight
         *      This method highlights the node group visually as long as the node is not already disabled or selected.
         *      It is for instance called when the user hovers over a node group.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */
        highlight: function() {
            this.container.addClass(Factory.getModule('Config').Classes.HIGHLIGHTED);

            return this;
        },

        /**
         * Method: unhighlight
         *      Unhighlights the node group's visual appearance. The method is for instance calls when the user leaves a
         *      hovered node group. NOTE: The weird word unhighlighting is an adoption of the jQueryUI dev team speak,
         *      all credits to them :)!
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */
        unhighlight: function() {
            this.container.removeClass(Factory.getModule('Config').Classes.HIGHLIGHTED);

            return this;
        },

        /**
         * Method: remove
         *      Removes the whole visual representation from the canvas, deactivates listeners and calls home.
         *
         * Returns:
         *      A {Boolean} indicating successful deletion.
         */
        remove: function() {
            if (!this.deletable) return false;

            // notify our members of our deletion
            _.each(this.nodes, function(node) {
                node.removeFromNodeGroup(this);
            }.bind(this));

            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODEGROUP_DELETED, [this.id, this.nodeIds()]);

            return true;
        },

        /**
         * Method: toDict
         *
         * Returns:
         *      A key-value {Object} representing the node group.
         */
        toDict: function() {
            var properties = _.map(this.properties, function(prop) { return prop.toDict() });

            return {
                id:         this.id,
                nodeIds:    this.nodeIds(),
                properties: _.reduce(properties, function(memo, prop) {
                    return _.extend(memo, prop);
                })
            };
        }
    });
});
