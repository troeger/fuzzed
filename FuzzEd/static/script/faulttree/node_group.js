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

            // if we have less than two members left, remove us, as we are no longer relevant
            if (_.size(this.nodes) < 2) {
                this.graph.deleteNodeGroup(this);
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
