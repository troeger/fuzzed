define(['editor', 'factory', 'dfd/graph', 'dfd/config', 'jquery', 'underscore'], function(Editor, Factory, DfdGraph, DfdConfig) {
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

        getFactory: function() {
            return new Factory(undefined, 'dfd');
        },

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
        },

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