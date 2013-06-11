define(['fuzztree/config', 'faulttree/node'], function(Config, FaulttreeNode) {
    /**
     *  Concrete fuzztree node implementation
     */
    return FaulttreeNode.extend({
        setOptional: function(optional) {
            // mark node optional (or remove mark)
            if (optional) {
                this.container.addClass(this.config.Classes.NODE_OPTIONAL);
                this._nodeImage.primitives.attr('stroke-dasharray', this.config.Node.OPTIONAL_STROKE_STYLE);
            } else {
                this.container.removeClass(this.config.Classes.NODE_OPTIONAL);
                this._nodeImage.primitives.removeAttr('stroke-dasharray');
            }

            return this;
        },

        getConfig: function() {
            return Config;
        },

        _setupProperties: function(propertyMenuEntries, propertiesDisplayOrder) {
            var returned = this._super(propertyMenuEntries, propertiesDisplayOrder);
            var optionalProperty = this.properties.optional;

            if (optionalProperty) {
                this.setOptional(optionalProperty.value);
                jQuery(optionalProperty).on(Config.Events.PROPERTY_CHANGED, function(event, newValue) {
                    this.setOptional(newValue);
                }.bind(this));
            }

            return returned;
        }
    });
});
