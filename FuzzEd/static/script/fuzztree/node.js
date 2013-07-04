define(['fuzztree/config', 'faulttree/node'], function(Config, FaulttreeNode) {
    /**
     *  Concrete fuzztree node implementation
     */
    return FaulttreeNode.extend({
        setOptional: function(optional) {
            // mark node optional (or remove mark)
            if (optional) {
                this.container.addClass(this.config.Classes.OPTIONAL);
            } else {
                this.container.removeClass(this.config.Classes.OPTIONAL);
            }

            return this;
        },

        getConfig: function() {
            return Config;
        },

        _setupProperties: function(propertyMenuEntries, propertiesDisplayOrder) {
            this._super(propertyMenuEntries, propertiesDisplayOrder);
            var optionalProperty = this.properties.optional;

            if (optionalProperty) {
                this.setOptional(optionalProperty.value);
                jQuery(optionalProperty).on(Config.Events.PROPERTY_CHANGED, function(event, newValue) {
                    this.setOptional(newValue);
                }.bind(this));
            }

            return this;
        }
    });
});
