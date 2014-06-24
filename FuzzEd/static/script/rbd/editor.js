define(['editor', 'factory', 'rbd/graph', 'rbd/config'], function(Editor, Factory, RbdGraph, RbdConfig) {
    /**
     * Package: RBD
     */

    /**
     * Class: RbdEditor
     *      RBD-specific <Base::Editor> class.
     *
     * Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         * Group: Accessors
         */

        getFactory: function() {
            return new Factory(undefined, 'rbd');
        },

        /**
         * Method: getConfig
         *
         * Returns:
         *      The <RbdConfig> object.
         */
        getConfig: function() {
            return RbdConfig;
        },

        /**
         * Method: getGraphClass
         *
         * Returns:
         *      The <RbdGraph> class.
         */
        getGraphClass: function() {
            return RbdGraph;
        }
    });
});
