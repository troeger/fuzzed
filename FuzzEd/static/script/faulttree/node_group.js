define(['node_group', 'config'], function(NodeGroup, Config) {

    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNodeGroup
     *
     * Extends: <Base::NodeGroup>
     */
    return NodeGroup.extend({
        init: function(definition, nodes, properties) {
            this._super(definition, nodes, properties);

            _.each(this.nodes, function(node) {
                node.addToNodeGroup(this);
            }.bind(this));
        },
        _setupVisualRepresentation: function() {
            return this;
        },
        redraw: function() {
            return this;
        },
        _setupDragging: function() {
            return this;
        },
        _setupMouse: function() {
            return this;
        },
        _setupSelection: function() {
            return this;
        },

        /**
         * Method: _setupProperties
         *      Converts the informal properties stored in <properties> into Property objects ordered by this graph's
         *      propertiesDisplayOrder (see <Graph::getNotation()> or the respective notations json-file).
         *
         *      ! Exact code duplication in <Node::_setupProperties()>  and <Edge::_setupPropertes()>
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
                this.properties[propertyName] = this.factory.getClassModule('Property')
                                                            .from(this.factory, this, this.nodes, property);
            }.bind(this));

            return this;
        },
        remove: function() {
            if (!this.deletable) return false;

            // unaffect all currently affected nodes (you know, the purple ones) and remove their reference to us
            _.each(this.nodes, function(node) {
                node.unaffect();
                node.removeNodeGroup();
            }.bind(this));

            // don't listen anymore
            jQuery(document).off([ Config.Events.NODES_MOVED,
                                   Config.Events.NODE_PROPERTY_CHANGED ].join(' '), this.redraw.bind(this));

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_DELETED, [this.id, this.nodeIds()]);

            return true;
        },
        addNode: function(node) {
            this.nodes[node.id] = node;
            node.addToNodeGroup(this);
            this._refreshProperties();
        },
        _refreshProperties: function() {
            _.each(this.properties, function(prop) {
                prop.removeAllMirrors();
                prop.restoreMirrors();
            }.bind(this));
        }
    });
});
