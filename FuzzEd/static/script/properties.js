define(['config', 'class', 'underscore'],
       function(Config, Class) {

    function _getFloat(definition, key, defaultValue) {
        if (!_.has(definition, key)) return defaultValue;

        var number = parseFloat(definition[key]);
        if (isNaN(number)) return defaultValue;
        return number;
    }
    
    var Property = Class.extend({
        id:       undefined,
        input:    undefined,
        disabled: undefined,
        mirror:   undefined,
        name:     undefined,
        node:     undefined,
        property: undefined,
        visual:   undefined,

        init: function(node, mirror, propertyDefinition) {
            this.id       = _.uniqueId('property-visual');
            this.disabled = propertyDefinition.disabled || false;
            this.mirror   = mirror;
            this.name     = propertyDefinition.displayName || '';
            this.node     = node;
            this.property = propertyDefinition.property;
            
            jQuery.extend(this, this._setupVisual());
            this._mirror();
        },

        hide: function() {
            this.visual.remove();

            return this;
        },

        insertAfter: function(element) {
            this.visual.insertAfter(element);
            this._setupCallbacks();

            return this;
        },

        show: function(container) {
            container.append(this.visual);
            this._setupCallbacks();

            return this;
        },

        _inputValue: function() {
            return this.input.val();
        },

        _mirror: function() {
            if (typeof this.mirror !== 'undefined') {
                this.mirror.show(this._inputValue());
            }
        },

        _sendChange: function() {
            if (this.property) {
                var property = this.property;
                var value = this._value();

                // update function that will be called after 1 sec. of inactivity
                var sendChange = function() {
                    var properties = {};
                    properties[property] = value;

                    jQuery(document).trigger(Config.Events.NODE_PROPERTY_CHANGED, [this.node.id, properties]);
                }.bind(this);

                // discard old timeout
                clearTimeout(this._sendChangeTimeout);
                // create a new one
                this._sendChangeTimeout = setTimeout(sendChange, 1000);
            }
        },

        _setupCallbacks: function() {
            // iterate over the handable input events (Config.Properties.Events), figure if we 
            // have defined such an event handler (_<EVENT>, e.g. _change) and bind it as well as 
            // user defined handler (<EVENT>, e.g. change)
            _.each(Config.Properties.Events, function(eventType) {
                var typeCallback = this['_' + eventType];
                if (typeof typeCallback !== 'undefined') {
                    this.input.bind(eventType, typeCallback.bind(this));
                }

                var userCallback = this[eventType];
                if (typeof userCallback !== 'undefined') {
                    this.input.bind(eventType, userCallback);
                }
            }.bind(this));
        },

        _setupControlGroup: function() {
            return jQuery(
                '<div class="control-group">\
                    <label class="control-label" for="' + this.id + '">' + this.name + '</label>\
                    <div class="controls"></div>\
                </div>'
            );
        },

        _setupInput: function() {
            throw '[ABSTRACT] Override in subclass';
        },

        _setupVisual: function() {
            var group = this._setupControlGroup();
            var input = this._setupInput();
            group.children('.controls').append(input);

            return {
                visual: group,
                input:  input
            };
        },

        _value: function(value) {
            if (typeof value === 'undefined') return this.node[this.property];
            this.node[this.property] = value;

            return this;
        },

        /**
         *  Method: _warn
         *      Highlight the control group. Use this to notify the user that he/she entered a wrong value.
         *
         *  Parameters:
         *      warn - [optional] Boolean to indicate whether to set or remove warning state. (Default: true)
         */
        _warn: function(warn) {
            if (typeof warn === 'undefined') warn = true;

            if (warn) {
                this.visual.addClass('error');
            } else {
                this.visual.removeClass('error');
            }
        }
    });

    var Checkbox = Property.extend({
        _change: function() {
            this._mirror();
            this._value(this._inputValue());
            this._sendChange();
        },

        _inputValue: function() {
            return this.input.attr('checked') ? true : false  
        },

        _setupInput: function() {
            return jQuery('<input type="checkbox">')
                .attr('id', this.id)
                .attr('disabled', this.disabled ? 'disabled' : null)
                .attr('checked', this._value() ? 'checked' : null);
        }
    });

    var Compound = Property.extend({
        choices: undefined,

        init: function(node, mirror, propertyDefinition) {
            this.choices  = propertyDefinition.choices;
            if (typeof this.choices === 'undefined' || _.keys(this.choices).length < 2) {
                throw 'Not enough choices for compound property';
            }
            this.node     = node;
            this.property = propertyDefinition.property;

            _.each(_.keys(this.choices), function(choice) {
                var compoundPropertyDefinition = this.choices[choice];
                compoundPropertyDefinition.property = this.property;

                this.choices[choice] = newFrom(node, mirror, compoundPropertyDefinition);
            }.bind(this));

            propertyDefinition.property = propertyDefinition.property + 'Selected';
            this._super(node, mirror, propertyDefinition);
        },

        hide: function() {
            this._activeChoice().hide();
            this.visual.remove();

            return this;
        },

        show: function(container) {
            container.append(this.visual);
            this._setupCallbacks();
            this._activeChoice().show(container);

            return this;
        },

        _active: function() {
            return this.buttons.filter('.active');
        },

        _activeChoice: function() {
            return this.choices[this._active().html()];
        },

        _click: function(eventObject) {
            this._activeChoice().hide();
            this._active().removeClass('active');
            jQuery(eventObject.target).addClass('active');

            var newChoice = this._activeChoice();
            newChoice._value(newChoice._inputValue());

            newChoice.insertAfter(this.visual);
            newChoice._mirror();
            newChoice._sendChange();

            this._value(this._active().html());
            this._sendChange();
        },

        _mirror: function() {
            this._activeChoice()._mirror();
        },

        _setupInput: function() {
            var buttonGroup = jQuery('<div class="btn-group">');
            var selected    = this.node[this.property];
            var activeSet   = false;

            _.each(_.keys(this.choices), function(choice) {
                var active = (choice === selected ? 'active' : undefined);
                activeSet  = activeSet || active;

                buttonGroup.append(jQuery('<button type="button" class="btn">')
                    .html(choice)
                    .addClass(active));
            });

            if (!activeSet) buttonGroup.children().eq(0).addClass('active');

            return buttonGroup;
        },

        _setupVisual: function() {
            var visuals     = this._super();
            visuals.buttons = visuals.input.children('button');

            return visuals;
        }
    });

    var Number = Property.extend({
        min:  undefined,
        max:  undefined,
        step: undefined,

        init: function(node, mirror, propertyDefinition) {
            this.min  = this._getFloat(propertyDefinition, 'min', -window.Number.MAX_VALUE);
            this.max  = this._getFloat(propertyDefinition, 'max',  window.Number.MAX_VALUE);
            this.step = this._getFloat(propertyDefinition, 'step', 1);

            this._super(node, mirror, propertyDefinition);
        },

        _getFloat: _getFloat,

        _change: function() {
            this._keyup();
        },

        _keyup: function() {
            this._mirror();
            this._validate();
            this._value(this._inputValue());
            this._sendChange();
        },

        _blur: function() {
            // reset input value to actual value
            // (necessary if the user entered a value which is not within the bounds)
            this.input.val(this._inputValue());
            this._validate();
        },

        _inputValue: function() {
            var value;
            if (this._super() == "") {
                // allow null values in case the user cleared the field
                value = null;
            } else {
                value = parseFloat(this._super());
                // keep value within bounds
                if (value < this.min) value = this.min;
                if (value > this.max) value = this.max;
            }
            return value;
        },

        /**
         *  Method: _validate
         *      Check the validity of the input and warn in case of an invalid value.
         */
        _validate: function() {
            if (this._inputValue() != this.input.val())
                this._warn(true);
            else
                this._warn(false);
        },

        _setupInput: function() {
            return jQuery('<input type="number" class="input-medium">')
                .attr('id',       this.id)
                .attr('min',      this.min)
                .attr('max',      this.max)
                .attr('step',     this.step)
                .attr('disabled', this.disabled ? 'disabled' : null)
                .val(this._value())
        }
    });

    var Range = Property.extend({
        _lower: undefined,
        _upper: undefined,

        init: function(node, mirror, propertyDefinition) {
            this.min  = this._getFloat(propertyDefinition, 'min', -window.Number.MAX_VALUE);
            this.max  = this._getFloat(propertyDefinition, 'max',  window.Number.MAX_VALUE);
            this.step = this._getFloat(propertyDefinition, 'step', 1)

            this._super(node, mirror, propertyDefinition);
        },

        _keyup: function(eventObject) {
            this._change(eventObject);
        },

        _change: function(eventObject) {
            var lower = parseFloat(this._lower.val());
            var upper = parseFloat(this._upper.val());

            if (isNaN(lower) || isNaN(upper)) return;

            if (lower > upper && this._lower.is(eventObject.target)) {
                upper = lower;
            } else if (lower > upper && this._upper.is(eventObject.target)) {
                lower = upper;
            }

            this._lower.val(lower);
            this._upper.val(upper);
            this._mirror();
            this._value(this._inputValue());
            this._sendChange();
        },

        _createNumberInput: function() {
            return jQuery('<input type="number" class="input-mini">')
                .attr('min',      this.min)
                .attr('max',      this.max)
                .attr('step',     this.step)
                .attr('disabled', this.disabled ? 'disabled' : null);
        },

        _getFloat: _getFloat,

        _inputValue: function() {
            return [parseFloat(this._lower.val()), parseFloat(this._upper.val())];
        },

        _mirror: function() {
            if (typeof this.mirror !== 'undefined') {
                var values = this._inputValue();
                this.mirror.show(values[0] + '-' + values[1]);
            }
        },

        _setupInput: function() {
            var value = this._value();
            var inlineForm = jQuery('<form class="form-inline">');
            var lower = this._createNumberInput().val(value[0]);
            var upper = this._createNumberInput().val(value[1]);

            return inlineForm.append(lower, upper);
        },

        _setupVisual: function() {
            var visuals = this._super();
            var inputs  = visuals.input.children('input');

            visuals._lower = inputs.eq(0);
            visuals._upper = inputs.eq(1);

            return visuals;
        }
    });

    var Select = Property.extend({
        choices: undefined,

        init: function(node, mirror, propertyDefinition) {
            this.choices = propertyDefinition.choices;
            if (typeof this.choices === 'undefined' || this.choices.length < 2) {
                throw 'Not enough choices for Select property';
            }

            this._super(node, mirror, propertyDefinition);
        },

        _change: function() {
            this._value(this._inputValue());
            this._mirror();
            this._sendChange();
        },

        _setupInput: function() {
            var value    = this._value();
            var select   = jQuery('<select class="input-medium">');
            var selected = typeof value !== 'undefined' ? value : this.choices[0];

            // model each choice as an option of the select
            _.each(this.choices, function(choice) {
                select.append(jQuery('<option>')
                    .html(choice)
                    .attr('value', choice)
                    .attr('selected', choice === selected ? 'selected' : null)
                    .appendTo(select));
            })

            return select;
        }
    });

    var Text = Property.extend({
        _keyup: function() {
            this._mirror();
            this._value(this._inputValue());
            this._sendChange();
        },

        _setupInput: function() {
            return jQuery('<input type="text" class="input-medium">')
                .attr('id', this.id)
                .attr('disabled', this.disabled ? 'disabled' : null)
                .val(this._value());
        }
    });

    function newFrom(node, mirror, propertyDefinition) {
        var kind = propertyDefinition.kind;

        if (kind === 'checkbox') {
            return new Checkbox(node, mirror, propertyDefinition);
        } else if (kind === 'compound') {
            return new Compound(node, mirror, propertyDefinition);
        } else if (kind === 'number') {
            return new Number(node, mirror, propertyDefinition);
        } else if (kind === 'range') {
            return new Range(node, mirror, propertyDefinition);
        } else if (kind === 'select') {
            return new Select(node, mirror, propertyDefinition);
        } else {
            return new Text(node, mirror, propertyDefinition);
        }
    }

    return {
        Checkbox: Checkbox,
        Compound: Compound,
        Number:   Number,
        Range:    Range,
        Select:   Select,
        Text:     Text,

        newFrom: newFrom
    };
});