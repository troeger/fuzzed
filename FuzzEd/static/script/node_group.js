define(['property', 'class', 'jquery'],
function(Property, Class) {
    /**
     *  Class: NodeGroup
     *
     *  Blah
     *
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *
         */
        container:     undefined,
        graph:         undefined,
        id:            undefined,
        nodes:         undefined,
        properties:    undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         *
         */
        init: function(definition, nodes, properties) {
            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;
            this.properties = jQuery.extend(true, {}, properties);

            delete this.properties.id;
            delete this.properties.graph;

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_ADDED, [this.id, this.nodeIds()]);
        },

        nodeIds: function() {
            return _.map(this.nodes, function(node) { return node.id });
        }
    });
});
