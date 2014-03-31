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
        property:          undefined,

        _jsPlumbConnection: undefined,

        init: function(property, jsPlumbConnection, properties) {
            this.property = property;
            this._jsPlumbConnection = jsPlumbConnection;

            this._jsPlumbConnection.addOverlay(["Label", {
                label:  property.value || property.defaultValue,
                id:     Config.JSPlumb.LABEL_OVERLAY_ID
            }]);

            this._setupEvents();
        },

        show: function(text) {
            var overlay = this._jsPlumbConnection.getOverlay(Config.JSPlumb.LABEL_OVERLAY_ID);
            overlay.setLabel(text);
        },

        _setupEvents: function() {
            jQuery(this.property).on(Config.Events.EDGE_PROPERTY_CHANGED, function(event, newValue, text, issuer) {
                this.show(text);
            }.bind(this));
        }
    });
});
