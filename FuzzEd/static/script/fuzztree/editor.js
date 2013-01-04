define(['faulttree/editor', 'fuzztree/graph', 'fuzztree/config'],
function(FaulttreeEditor, FuzztreeGraph, FuzztreeConfig) {
    /**
     *  Package: Fuzztree
     */

    /**
     *  Class: FuzztreeEditor
     *    Fuzztree-specific <Base::Editor> class.
     *
     *  Extends: <Faulttree::FaultTreeEditor>
     */
    return FaulttreeEditor.extend({
        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *
         *  Returns:
         *    The <FuzztreeConfig> object.
         *
         *  See also:
         *    <Base::Editor::getConfig>
         */
        getConfig: function() {
            return FuzztreeConfig;
        },

        /**
         *  Method: getGraphClass
         *
         *  Returns:
         *    The <FuzztreeGraph> class.
         *
         *  See also:
         *    <Base::Editor::getGraphClass>
         */
        getGraphClass: function() {
            return FuzztreeGraph;
        }
    });
});
