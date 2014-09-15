define(['factory', 'node_group', 'config'], function(Factory, NodeGroup, Config) {

    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNodeGroup
     *
     * Extends: <Base::NodeGroup>
     */
    return NodeGroup.extend({
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
                this.properties[propertyName] = Factory.getClassModule('Property')
                                                            .from(this, this.nodes, property);
            }.bind(this));

            return this;
        },

        remove: function() {
            this._super();

            // unaffect all currently affected nodes (you know, the purple ones) and remove their reference to us
            _.each(this.nodes, function(node) {
                node.unaffect();
                node.removeFromNodeGroup(this);
            }.bind(this));

            return true;
        },

        _addNode: function(node) {
            this._super(node);
            this._refreshProperties();
        },

        removeNode: function(node) {
            delete this.nodes[node.id];

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_NODEIDS_CHANGED, [this.id, this.nodeIds()]);

            // if we have less than one member node left, remove us, as we are no longer relevant
            if (_.size(this.nodes) == 1) {
                // and replace the last standing node with a new node, that carries forth our properties

                // as we assured that the size of this.nodes is 1 we can just pick any key
                var key = Object.keys(this.nodes)[0];
                var lastStandingNode = this.nodes[key];

                var jsonNode = jQuery.extend({},
                   _.pick(lastStandingNode,
                        'kind',
                        'x',
                        'y'
                    ),
                    {
                        properties: this.toDict().properties
                    }
                );

                this.graph.addNode(jsonNode);

                this.graph.deleteNodeGroup(this);

                this.graph.deleteNode(lastStandingNode);
            }
        },

        _refreshProperties: function() {
            _.each(this.properties, function(prop) {
                prop.removeAllMirrors();
                prop.restoreMirrors();
            }.bind(this));
        }
    });
});
