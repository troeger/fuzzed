define(['factory', 'editor', 'rbd/graph'], function(Factory, Editor, RbdGraph) {
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
        // nothing to overwrite here, but this file is necessary to import graph specific modules at the top
    });
});
