define(['faulttree/config', 'node'], function(Config, AbstractNode) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNode
     *      Tiny class introduced for clearer typing and to adjust config to <Faultree::Config>.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        ownProperties: undefined,

        getConfig: function() {
            return Config;
        },

        select: function() {
            this._super();

            if (!_.isEmpty(this.nodegroups)) {
                // invoke 'affect' on all our NodeGroups' nodes (normally should only have one NodeGroup)
                _.each(this.nodegroups, function(nodegroup) {
                    _.each(nodegroup.nodes, function(node) {
                        if (this != node) node.affect();
                    }.bind(this));
                }.bind(this));
            }
        },

        deselect: function() {
            this._super();

            if (!_.isEmpty(this.nodegroups)) {
                // invoke 'unaffect' on all our NodeGroups' nodes (normally should only have one NodeGroup)
                _.each(this.nodegroups, function(nodegroup) {
                    _.each(nodegroup.nodes, function(node) {
                        if (this != node) node.unaffect();
                    }.bind(this));
                }.bind(this));
            }
        },

        affect: function() {
            this.container.addClass(this.config.Classes.AFFECTED);

            return this;
        },

        unaffect: function() {
            this.container.removeClass(this.config.Classes.AFFECTED);

            return this;
        },

        addToNodeGroup: function(nodegroup) {
            this._super(nodegroup);

            this.ownProperties = this.properties;
            this.properties = nodegroup.properties;

            _.each(this.ownProperties, function(prop) {
                prop.removeAllMirrors();
            }.bind(this));
        },

        removeFromNodeGroup: function(nodegroup) {
            this._super(nodegroup);

            // if we were the last node of the node group
            if (_.isEmpty(nodegroup.nodes)) {
                var jsonNode = jQuery.extend({},
                    _.pick(this,
                        'kind',
                        'x',
                        'y'
                    ), {
                        properties: this.nodegroup.toDict().properties
                    });

                this.remove();
                this.graph.addNode(jsonNode);
            }
        }
    });
});
