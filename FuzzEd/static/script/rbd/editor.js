define(['editor', 'factory', 'rbd/graph', 'rbd/config'], function(Editor, Factory, RbdGraph, RbdConfig) {
    /**
     *  Package: RBD
     */

    /**
     *  Class: RbdEditor
     *    RBD-specific <Base::Editor> class.
     *
     *  Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         *  Group: Accessors
         */

        getFactory: function() {
            return new Factory(undefined, 'rbd');
        },

        /**
         *  Method: getConfig
         *
         *  Returns:
         *    The <RbdConfig> object.
         *
         *  See also:
         *    <Base::Editor::getConfig>
         */
        getConfig: function() {
            return RbdConfig;
        },

        /**
         *  Method: getGraphClass
         *
         *  Returns:
         *    The <RbdGraph> class.
         *
         *  See also:
         *    <Base::Editor::getGraphClass>
         */
        getGraphClass: function() {
            return RbdGraph;
        }
    });
});
