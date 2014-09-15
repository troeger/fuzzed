define(['factory', 'editor', 'rbd/graph', 'rbd/config'], function(Factory, Editor, RbdGraph, RbdConfig) {
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
        init: function(graphId) {
            if (typeof Factory.kind === 'undefined') Factory.kind = 'rbd';
            this._super(graphId);
        }
    });
});
