define(['fuzztree/config', 'faulttree/node'], function(Config, FaulttreeNode) {
    /**
     *  Concrete fuzztree node implementation
     */
    return FaulttreeNode.extend({
        optionalIndicator: undefined,

        setOptional: function(optional) {
            this.optional = optional;

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

        _setupVisualRepresentation: function() {
            this._super();
            this.setOptional(this.optional);

            return this;
        },

        _setupProperties: function(propertyMenuEntries, propertiesDisplayOrder) {
            if (propertyMenuEntries && propertyMenuEntries.optional) {
                propertyMenuEntries.optional.change = function() {
                    this.setOptional(this.optional);
                }.bind(this);
            }
            return this._super(propertyMenuEntries, propertiesDisplayOrder);
        }
    });
});
