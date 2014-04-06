define(['config', 'class', 'jquery'], function(Config, Class) {
    /**
     * Package: Base
     */

    /**
     * Class: Label
     *
     * Labels are small text boxes above an edge, which display the edge's name. Their sole purpose is visualization,
     * meaning that they do not allow edit operations.
     *
     */
    return Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *   {Property}   property     - The property object displayed by the label
         *
         *   {jsPlumbConnection} _jsPlumbConnection - The jsPlumbConnection the label is connected to
         */
        property:          undefined,

        _jsPlumbConnection: undefined,

        /**
         * Constructor: init
         *
         * This method constructs a new label object.
         *
         * Parameters:
         *   {Property}   property    - The property object to visualize
         *   {jsPlumbConnection} _jsPlumbConnection - The jsPlumbConnection the label is connected to
         *   {Objects}    properties  - Object with mirror configuration options (e.g. style)
         */

        init: function(property, jsPlumbConnection, properties) {
            this.property = property;
            this._jsPlumbConnection = jsPlumbConnection;

            // initial creation of the overlay
            this._jsPlumbConnection.addOverlay(["Label", {
                label:    property.value || property.defaultValue,
                id:       Config.JSPlumb.LABEL_OVERLAY_ID,
                location: 0.4   // temporary work around to shift edge labels a bit from the center, so that they don't
                                //   overlap each other as soon as there are two edges between two nodes
            }]);

            //TODO: implement usage of properties (e.g. style)
            this._setupEvents();
        },

        /**
         * Method: show
         *
         * This method allows to change the text of the label to the one specified in the method's only parameter.
         *
         * Parameters:
         *   {String} text - The text to show in the label
         *
         * Returns:
         *   This {Label} instance for chaining.
         */
        show: function(text) {
            var overlay = this._jsPlumbConnection.getOverlay(Config.JSPlumb.LABEL_OVERLAY_ID);
            overlay.setLabel(text);

            return this;
        },

        /**
         *  Method: _setupEvents
         *      Register for changes of the associated <Property> object.
         *
         *  Returns:
         *      This {Label} instance for chaining.
         */
        _setupEvents: function() {
            jQuery(this.property).on(Config.Events.EDGE_PROPERTY_CHANGED, function(event, newValue, text, issuer) {
                this.show(text);
            }.bind(this));

            return this;
        }
    });
});
