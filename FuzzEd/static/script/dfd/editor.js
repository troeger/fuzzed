define(['factory', 'editor', 'dfd/graph', 'dfd/config', 'jquery', 'underscore', 'dfd/node_group'],
    function(Factory, Editor, DfdGraph, DfdConfig) {
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
         * Method: _setupJsPlumb
         *      Overrides the editor's standard behaviour of JsPlumb edges in order to add an outline to them.
         *
         * Returns:
         *      This {<DFDEditor>} instance for chaining.
         */
        _setupJsPlumb: function() {
            this._super();
            jsPlumb.connectorClass += " outlined";
            return this;
        },


        _setupMenuActions: function() {
            this._super();

            jQuery('#' + this.config.IDs.ACTION_GROUP).click(function() {
                this._groupSelection();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_UNGROUP).click(function() {
                this._ungroupSelection();
            }.bind(this));

            // set the shortcut hints from 'Ctrl+' to '⌘' when on Mac
            if (navigator.platform == 'MacIntel' || navigator.platform == 'MacPPC') {
                jQuery('#' + this.config.IDs.ACTION_GROUP + ' span').text('⌘G');
                jQuery('#' + this.config.IDs.ACTION_UNGROUP + ' span').text('⌘U');
            }


            return this;
        },

        _setupKeyBindings: function(readOnly) {
            this._super(readOnly)
            if (readOnly) return this;

            jQuery(document).keydown(function(event) {
                if (event.which === 'G'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._groupPressed(event);
                } else if (event.which === 'U'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._ungroupPressed(event);
                }
            }.bind(this));

            return this;
        },

        _groupPressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();

            this._groupSelection();

            return this;
        },

        _ungroupPressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();

            this._ungroupSelection();

            return this;
        }
    });
});