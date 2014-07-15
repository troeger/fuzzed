define(['factory', 'faulttree/editor', 'fuzztree/graph', 'fuzztree/config', 'fuzztree/node'],
function(Factory, FaulttreeEditor, FuzztreeGraph, FuzztreeConfig) {
    /**
     * Package: Fuzztree
     */

    /**
     * Class: FuzztreeEditor
     *      Fuzztree-specific <Base::Editor> class.
     *
     * Extends: <Faulttree::FaultTreeEditor>
     */
    return FaulttreeEditor.extend({
        /**
         * Group: Accessors
         */

        getFactory: function() {
            return new Factory(undefined, 'fuzztree');
        },

        /**
         * Method: getConfig
         *
         * Returns:
         *      The <FuzztreeConfig> object.
         */
        getConfig: function() {
            return FuzztreeConfig;
        },

        /**
         * Method: getGraphClass
         *
         * Returns:
         *      The <FuzztreeGraph> class.
         */
        getGraphClass: function() {
            return FuzztreeGraph;
        }
    });
});
