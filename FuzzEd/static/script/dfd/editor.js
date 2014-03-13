define(['editor', 'dfd/graph', 'dfd/config'], function(Editor, DfdGraph, DfdConfig) {
    /**
     *  Package: DFD
     */

    /**
     *  Class: DfdEditor
     *    DFD-specific <Base::Editor> class.
     *
     *  Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *
         *  Returns:
         *    The <DfdConfig> object.
         *
         *  See also:
         *    <Base::Editor::getConfig>
         */
        getConfig: function() {
            return DfdConfig;
        },

        /**
         *  Method: getGraphClass
         *
         *  Returns:
         *    The <DfdGraph> class.
         *
         *  See also:
         *    <Base::Editor::getGraphClass>
         */
        getGraphClass: function() {
            return DfdGraph;
        }
    });
});