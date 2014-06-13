define(['faulttree/config', 'node'], function(Config, AbstractNode) {

    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNode
     *
     * Tiny class introduced for clearer typing and to adjust config to <Faultree::Config>.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        nodegroup: undefined,
        ownProperties: undefined,

        init: function(definition) {
            this._super(definition);

            jQuery(document).on(Config.Events.NODEGROUP_ADDED, function (event, id, nodeIds, properties, nodegroup) {
                if (_.contains(nodeIds, this.id)) {
                   // if we are contained in the newly created node group
                   this.addToNodeGroup(nodegroup);
                }
            }.bind(this));
            jQuery(document).on(Config.Events.NODEGROUP_DELETED, function (event, id, nodeIds) {
                if (_.contains(nodeIds, this.id)) {
                   // if we were part of the deleted node group
                    this.removeNodeGroup();
                }
            }.bind(this));
        },

        getConfig: function() {
            return Config;
        },

        select: function() {
            this._super();

            if (typeof this.nodegroup !== 'undefined') {
                _.invoke(_.without(this.nodegroup.nodes, this), 'affect');
            }
        },

        deselect: function() {
            this._super();

            if (typeof this.nodegroup !== 'undefined') {
                _.invoke(_.without(this.nodegroup.nodes, this), 'unaffect');
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
            this.ownProperties = this.properties;
            this.properties = nodegroup.properties;
            this.nodegroup  = nodegroup;

            _.each(this.ownProperties, function(prop) {
                prop.removeAllMirrors();
            }.bind(this));
        },

        removeNodeGroup: function() {
            _.each(this.properties, function(prop) {
                prop.removeAllMirrors();
            });

            this.properties = this.ownProperties;
            this.nodegroup  = undefined;

            _.each(this.properties, function(prop) {
                prop.restoreMirrors();
            });
        }
    });
});
