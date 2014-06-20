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

            //this.properties = this.ownProperties;
            /*_.each(this.properties, function(prop) {
                prop.changeOwnerTo(this);
            }.bind(this));*/

            /*var jsonNode = jQuery.extend({},
                _.pick(this,
                    'id',
                    'kind',
                    'x',
                    'y'
                ),
                {
                    properties: this.nodegroup.toDict().properties
                }
            );*/

            this.properties = this.ownProperties;
            this.nodegroup  = undefined;

            _.each(this.properties, function(prop) {
                prop.restoreMirrors();
            });

            //this.remove();
            //this.graph.addNode(jsonNode);
        }
    });
});
