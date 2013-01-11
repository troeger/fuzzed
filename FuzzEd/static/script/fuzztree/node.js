define(['fuzztree/config', 'faulttree/node'], function(Config, FaulttreeNode) {
    /**
     *  Concrete fuzztree node implementation
     */
    return FaulttreeNode.extend({
        optionalIndicator: undefined,

        setOptional: function(optional) {
            this.optional = optional;

            if (optional) {
                this.optionalIndicator.attr('fill', this.config.Node.OPTIONAL_INDICATOR_FILL);
            } else if (this._selected) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_SELECTED);
            } else if (this._highlighted) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_HIGHLIGHTED);
            } else {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_NORMAL);
            }

            return this;
        },

        getConfig: function() {
            return Config;
        },

        _visualSelect: function() {
            this._super();

            this.optionalIndicator.attr('stroke', this.config.Node.STROKE_SELECTED);
            if (!this.optional) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_SELECTED);
            }

            return this;
        },

        _visualHighlight: function() {
            this._super();

            this.optionalIndicator.attr('stroke', this.config.Node.STROKE_HIGHLIGHTED);
            if (!this.optional) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_HIGHLIGHTED);
            }

            return this;
        },

        _visualDisable: function() {
            this._super();

            this.optionalIndicator.attr('stroke', this.config.Node.STROKE_DISABLED);
            if (!this.optional) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_DISABLED);
            }

            return this;
        },

        _visualReset: function() {
            this._super();

            this.optionalIndicator.attr('stroke', this.config.Node.STROKE_NORMAL);
            if (!this.optional) {
                this.optionalIndicator.attr('fill', this.config.Node.STROKE_NORMAL);
            }

            return this;
        },

        _setupVisualRepresentation: function() {
            this._super();

            var optionalIndicatorWrapper = jQuery('<div>').svg();
            var optionalIndicator = optionalIndicatorWrapper.svg('get');
            var radius = this.config.Node.OPTIONAL_INDICATOR_RADIUS;

            var optionalIndicatorCircle = optionalIndicator.circle(null, radius + 1, radius + 1, radius, {
                strokeWidth: this.config.Node.OPTIONAL_INDICATOR_STROKE,
                fill: this.optional ? this.config.Node.OPTIONAL_INDICATOR_FILL : this.config.Node.STROKE_NORMAL,
                stroke: this.config.Node.STROKE_NORMAL
            });

            // external method for changing attributes of the circle later
            optionalIndicator.attr = function(attr, value) {
                var setting = {};
                setting[attr] = value;
                optionalIndicator.change(optionalIndicatorCircle, setting);
            };

            optionalIndicatorWrapper
                .addClass(this.config.Classes.NODE_OPTIONAL_INDICATOR)
                .prependTo(this.container);

            // hide the optional indicator for nodes with undefined value
            if (typeof this.optional === 'undefined' || this.optional == null) {
                optionalIndicatorWrapper.css('visibility', 'hidden');
            }
            this.optionalIndicator = optionalIndicator;

            return this;
        },

        _setupPropertyMenuEntries: function(propertyMenuEntries, propertiesDisplayOrder) {
            if (this.propertyMenuEntries['optional']) {
                this.propertyMenuEntries.optional.change = function() {
                    this.setOptional(this.optional);
                }.bind(this);
            }
            this._super(propertyMenuEntries, propertiesDisplayOrder);

            return this;
        },

        _connectorOffset: function() {
            var offsets = this._super();

            if (typeof this.optional !== 'undefined' && this.optional != null) {
                offsets.in.y = jQuery(this.optionalIndicator._container).offset().top - this.container.offset().top;
            }

            return offsets;
        }
    });
});
