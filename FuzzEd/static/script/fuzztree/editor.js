define(['factory', 'faulttree/editor', 'fuzztree/config', 'fuzztree/node'],
function(Factory, FaulttreeEditor, FuzztreeConfig) {
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
        // nothing to overwrite here, but this file is necessary to import graph specific modules at the top
    });
});
