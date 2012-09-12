define(['require-config', 'require-backend', 'require-oop', 'underscore'], 
       function(Config, Backend, Class) {

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

            if (typeof propertyDefinition._value !== 'undefined') {
                this._value = propertyDefinition._value;
            }
            
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
                properties = {};
                properties[this.property] = this._value();

                Backend.changeNode(this.node, properties);
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
                .attr('disabled', this.disabled ? 'disabled' : undefined)
                .attr('checked', this._value() ? 'checked' : undefined);
        }
    });

    var Compound = Property.extend({
        choices: undefined,

        init: function(node, mirror, propertyDefinition) {
            this.choices  = propertyDefinition.choices;
            if (typeof this.choices === 'undefined' || _.keys(this.choices).length < 2) {
                throw 'Not enough choices for Compound property';
            }
            this.node     = node;
            this.property = propertyDefinition.property;

            _.each(_.keys(this.choices), function(choice) {
                var compoundPropertyDefintion = this.choices[choice];
                compoundPropertyDefintion.property = this.property;

                this.choices[choice] = newFrom(node, mirror, compoundPropertyDefintion);
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
            this._sendChange();
        },

        _keyup: function() {
            this._mirror();
            this._value(this._inputValue());
        },

        _setupInput: function() {
            return jQuery('<input type="number" class="input-medium">')
                .attr('id',       this.id)
                .attr('min',      this.min)
                .attr('max',      this.max)
                .attr('step',     this.step)
                .attr('disabled', this.disabled ? 'disabled' : undefined)
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
                .attr('disabled', this.disabled ? 'disabled' : undefined);
        },

        _getFloat: _getFloat,

        _inputValue: function() {
            return [this._lower.val(), this._upper.val()];
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
                    .attr('selected', choice === selected ? 'selected' : undefined)
                    .appendTo(select));
            })

            return select;
        }
    });

    var Text = Property.extend({
        _blur: function() {
            this._sendChange();
        },

        _keyup: function() {
            this._mirror();
            this._value(this._inputValue());
        },

        _setupInput: function() {
            return jQuery('<input type="text" class="input-medium">')
                .attr('id', this.id)
                .attr('disabled', this.disabled ? 'disabled' : undefined)
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