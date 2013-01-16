define(['config', 'decimal', 'class', 'underscore'], function(Config, Decimal, Class) {
    var get = function(object, key, defaultValue) {
        var value = object[key];
        return (typeof value !== 'undefined' ? value : defaultValue);
    };

    var setupMiniNumber = function(value) {
        return jQuery('<input type="number" class="input-mini">')
            .attr('min',      this.options.min)
            .attr('max',      this.options.max)
            .attr('step',     this.options.step)
            .attr('disabled', this.options.disabled ? 'disabled' : null)
            .val(value);
    };

    var Property = Class.extend({
        id:            undefined,
        input:         undefined,
        node:          undefined,
        options:       undefined,

        _editing:      undefined,
        _editTarget:   undefined,
        _preEditValue: undefined,
        _mirror:       undefined,
        _timer:        undefined,
        _visual:       undefined,

        init: function(node, mirror, propertyDefinition) {
            this.id      = _.uniqueId('property');
            this.node    = node;
            this.options = propertyDefinition;

            this._editing = false;
            this._mirror  = mirror;

            this.options.disabled    = this.options.disabled    || false;
            this.options.displayName = this.options.displayName || '';
            this.options.blur        = this.options.blur        || jQuery.noop;
            this.options.change      = this.options.change      || jQuery.noop;

            this._preSetup()
                ._setupVisualRepresentation()
                .mirror()
                ._postSetup();
        },

        show: function(container) {
            this._visual.appendTo(container);
            this._setupCallbacks();

            return this;
        },

        hide: function() {
            if (this._editing) this._editTarget.blur();
            this._visual.remove();

            return this;
        },

        mirror: function() {
            if (typeof this._mirror !== 'undefined') this._mirror.show(this.value());

            return this;
        },

        inputValue: function(newValue) { throw '[ABSTRACT] subclass responsiblity'; },

        value: function(newValue) {
            if (typeof this.options.property === 'undefined') return this;

            if (typeof newValue === 'undefined') return this.node[this.options.property];
            this.node[this.options.property] = newValue;

            return this;
        },

        blurEvents: function() { return ['blur']; },

        blurred: function(event, ui) {
            this.fix(event, ui);

            if (this.validate(event, ui)) {
                this.value(this.inputValue())
                    ._sendChange()
                    .unwarn();
            } else {
                this.value(this._preEditValue)
                    .inputValue(this._preEditValue)
                    ._abortChange()
                    .unwarn();
            }
            this.options.blur(event, ui);
            this.mirror();

            this._editing      = false;
            this._editTarget   = undefined;
            this._preEditValue = undefined;

            return this;
        },

        changeEvents: function() { return []; },

        changed: function(event, ui) {
            if (!this._editing) { this._preEditValue = this.value(); }

            this._editing    = true;
            this._editTarget = event.target;

            this.fix(event, ui);

            if (this.validate(event, ui)) {
                this.value(this.inputValue())
                    ._sendChange()
                    .unwarn();
            } else {
                this.value(this._preEditValue)
                    ._abortChange()
                    .warn();
            }
            this.options.change(event, ui);
            this.mirror();

            return this;
        },

        registerOn: function() {
            return this.input;
        },

        fix: function(event, ui) { return this; },

        validate: function(event, ui) { return true; },

        warn: function() {
            this._visual.addClass(Config.Classes.PROPERTY_WARNING);

            return this;
        },

        unwarn: function() {
            this._visual.removeClass(Config.Classes.PROPERTY_WARNING);

            return this;
        },

        _preSetup: function() { return this; },

        _postSetup: function() { return this; },

        _abortChange: function() {
            window.clearTimeout(this._timer);

            return this;
        },

        _sendChange: function() {
            // discard old timeout
            window.clearTimeout(this._timer);
            // create a new one
            this._timer = window.setTimeout(function() {
                // update function that will be called after 1 sec. of inactivity
                var properties = {};
                properties[this.options.property] =  this.value();

                // call home!
                jQuery(document).trigger(Config.Events.NODE_PROPERTY_CHANGED, [this.node.id, properties]);
            }.bind(this), 1000);

            return this;
        },

        _setupCallbacks: function() {
            var register = this.registerOn();

            _.each(this.blurEvents(), function(event) {
                register.on(event, this.blurred.bind(this));
            }.bind(this));

            _.each(this.changeEvents(), function(event) {
                register.on(event, this.changed.bind(this));
            }.bind(this));
        },

        _setupInput: function() { throw '[ABSTRACT] subclass responsibility'; },

        _setupVisualRepresentation: function() {
            this._visual = jQuery(
                '<div class="control-group">\
                    <label class="control-label" for="' + this.id + '">' + this.options.displayName + '</label>\
                    <div class="controls"></div>\
                </div>'
            );
            this.input = this._setupInput();
            this._visual.children('.controls').append(this.input);

            return this;
        }
    });

    var Checkbox = Property.extend({
        blurEvents:   function() { return ['blur']; },
        changeEvents: function() { return ['change']; },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return this.input.attr('checked') ? true : false;
            this.input.attr('checked', newValue ? 'checked' : null);

            return this;
        },

        _setupInput: function() {
            return jQuery('<input type="checkbox">')
                .attr('id', this.id)
                .attr('disabled', this.options.disabled ? 'disabled' : null)
                .attr('checked', this.value() ? 'checked' : null);
        }
    });

    var Compound = Property.extend({
        _buttons: undefined,
        _choices: undefined,

        changeEvents: function() { return ['click']; },
        registerOn: function() { return this._buttons; },

        changed: function(event, ui) {
            var previousSelection = this.value();
            this._super(event, ui);
            var currentSelection = this.inputValue();

            if (previousSelection !== currentSelection) {
                var previous  = this._choices[previousSelection];
                previous.hide();

                var siblings  = this._visual.nextAll();
                siblings.remove();

                var current   = this._choices[currentSelection];
                var container = this._visual.parent();
                current.show(container);
                siblings.appendTo(container);
                current.inputValue(this.options.defaults[currentSelection]).registerOn().blur();
            }

            return this;
        },

        fix: function(event) {
            this.inputValue(event.target.innerHTML);

            return this;
        },

        hide: function() {
            this._choices[this.inputValue()].hide();
            return this._super();
        },

        show: function(container) {
            this._super(container);
            this._choices[this.inputValue()].show(container);

            return this;
        },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return this._buttons.filter('.active').html();
            this._buttons
                .removeClass('active')
                .filter(':contains(' + newValue + ')')
                .addClass('active');

            return this;
        },

        _preSetup: function() {
            var property = this.options.property;
            var defaults = this.options.defaults;
            var mirror   = this._mirror;
            var value    = this.node[property];

            this.options.property += 'Selected';
            this._mirror = undefined;

            if (!_.isObject(this.options.choices)) {
                throw '[TYPE ERROR] choices must be object, but was: ' + this.options.choices;
            } else if (!_.has(this.options.choices, this.value())) {
                throw '[VALUE ERROR] unknown choice: ' + this.options.property;
            } else if (!_.isObject(this.options.defaults)) {
                throw '[TYPE ERROR] defaults must be object, but was: ' + this.options.defaults;
            }

            this._choices = {};

            _.each(this.options.choices, function(definition, choice) {
                if (typeof defaults[choice] === 'undefined') {
                    throw '[VALUE ERROR] missing default value for choice: ' + choice;
                }

                this.node[property] = choice === this.value() ? value : defaults[choice];
                var compoundDefinition = jQuery.extend(true, { property: property }, definition);
                var compound = newFrom(this.node, mirror, compoundDefinition);
                compound.options.blur = function() {
                    defaults[choice] = this.value();
                }.bind(compound);
                this._choices[choice] = compound;
            }.bind(this));

            this.node[property] = value;
            this._choices[this.value()].mirror();

            return this;
        },

        _postSetup: function() {
            this._buttons = this.input.find('button');
        },

        _setupInput: function() {
            var buttons  = jQuery('<div class="btn-group">');
            var selected = this.value();

            if (typeof selected === 'undefined') throw '[VALUE ERROR] no compound selected: ' + selected;

            _.each(this.options.choices, function(definition, choice) {
                jQuery('<button type="button" class="btn">')
                    .html(choice)
                    .addClass(choice === selected ? 'active' : null)
                    .attr(this.options.disabled ? 'disabled' : null)
                    .appendTo(buttons);
            }.bind(this));

            return buttons;
        }
    });

    var Neighborhood = Property.extend({
        _value:        undefined,
        _epsilon:      undefined,
        _register:     undefined,

        _initialValue: undefined,

        changeEvents: function() { return ['keyup', 'change']; },

        fix: function(event) {
            if (event.type !== 'change' && event.type !== 'blur') return this;

            var inputValue = this.inputValue();
            var value      = inputValue[0];
            var epsilon    = inputValue[1];

            if (window.isNaN(value) || window.isNaN(epsilon)) return this;
            value   = new Decimal(value);
            epsilon = new Decimal(epsilon);

            // fix value
            if (value.plus(epsilon).gt(this.options.max) && this._value.is(event.target)) {
                this._epsilon.val(this.options.max.minus(value));
            } else if (value.minus(epsilon).lt(this.options.min) && this._value.is(event.target)) {
                this._epsilon.val(value.minus(this.options.min));

            // fix epsilon
            } else if (value.plus(epsilon).gt(this.options.max) && this._epsilon.is(event.target)) {
                this._value.val(this.options.max.minus(epsilon));
            } else if (value.minus(epsilon).lt(this.options.min) && this._epsilon.is(event.target)) {
                this._value.val(this.options.min.plus(epsilon));
            }

            return this;
        },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined')
                return [window.parseFloat(this._value.val()), window.parseFloat(this._epsilon.val())];
            this._value.val(newValue[0]);
            this._epsilon.val(newValue[1]);

            return this;
        },

        mirror: function() {
            if (typeof this._mirror !== 'undefined') {
                var value = this.value();
                this._mirror.show(value[0] + ' ± ' + value[1]);
            }

            return this;
        },

        registerOn: function() {
            return this._register;
        },

        validate: function() {
            var inputValue = this.inputValue();
            var value      = inputValue[0];
            var epsilon    = inputValue[1];

            return !window.isNaN(value) && !window.isNaN(epsilon)
                && this.options.min.lte(value) && this.options.epsilonMin.lte(epsilon)
                && this.options.max.gte(value) && this.options.epsilonMax.gte(epsilon)
                && (this.options.step ? this._initialValue[0].minus(value).mod(this.options.step).eq(0) : true)
                && (this.options.step ? this._initialValue[1].minus(epsilon).mod(this.options.step).eq(0) : true);
        },

        _preSetup: function() {
            this.options.min  = new Decimal(get(this.options, 'min', -Decimal.MAX_VALUE));
            this.options.max  = new Decimal(get(this.options, 'max',  Decimal.MAX_VALUE));
            this.options.step = this.options.step ? new Decimal(this.options.step) : null;

            this.options.epsilonMin  = new Decimal(get(this.options, 'epsilonMin', 0));
            this.options.epsilonMax  = new Decimal(get(this.options, 'epsilonMax', Decimal.MAX_VALUE));
            this.options.epsilonStep = this.options.epsilonStep ? new Decimal(this.options.epsilonStep) : null;

            if (this.options.min.gt(this.options.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.options.min + '/' + this.options.max;
            }
            else if (this.options.epsilonMin.isNeg()) {
                throw '[VALUE ERROR] epsilon must be positive epsilonMin: ' + this.options.epsilonMin;
            }
            else if (this.options.epsilonMin.gt(this.options.epsilonMax)) {
                throw '[VALUE ERROR] bounds violation epsilonMin/epsilonMax: '
                    + this.options.epsilonMin + '/' + this.options.epsilonMax;
            } else if (this.options.step && this.options.step.lte(0)) {
                throw '[VALUE ERROR] step must be positive: ' + this.options.step;
            } else if (this.options.epsilonStep && this.options.epsilonStep.lte(0)) {
                throw '[VALUE ERROR] step of epsilon must be positive: ' + this.options.epsilonStep;
            }

            return this;
        },

        _postSetup: function() {
            var value = this.value();

            this._value        = this.input.children().eq(0);
            this._epsilon      = this.input.children().eq(1);
            this._register     = jQuery(this._value).add(this._epsilon);

            this._initialValue = [new Decimal(value[0]), new Decimal(value[1])];

            return this;
        },

        _setupInput: function() {
            var value   = this.value();
            var form    = jQuery('<form class="form-inline">');
            var val     = this._setupMiniNumber(value[0]).attr('id', this.id);
            var epsilon = this._setupMiniNumber(value[1]);

            return form.append(val, epsilon);
        },

        _setupMiniNumber: setupMiniNumber
    });

    var Numeric = Property.extend({
        min:  undefined,
        max:  undefined,
        step: undefined,

        _initialValue: undefined,

        changeEvents: function() { return ['keyup', 'change']; },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return window.parseFloat(this.input.val());
            this.input.val(newValue);

            return this;
        },

        validate: function() {
            var value = this.inputValue();

            return !window.isNaN(value) && this.options.min.lte(value) && this.options.max.gte(value)
                && (this.options.step ? this._initialValue.minus(value).mod(this.options.step).eq(0) : true);
        },

        _preSetup: function() {
            this.options.min  = new Decimal(get(this.options, 'min', -Decimal.MAX_VALUE));
            this.options.max  = new Decimal(get(this.options, 'max',  Decimal.MAX_VALUE));
            this.options.step = this.options.step ? new Decimal(this.options.step) : null;

            if (this.options.min.gt(this.options.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.options.min + '/' + this.options.max;
            } else if (this.options.step && this.options.step.lt(0)) {
                throw '[VALUE ERROR] step must be positive: ' + this.options.step;
            }

            return this;
        },

        _postSetup: function() {
            if (this.options.step) this._initialValue = new Decimal(this.value());

            return this;
        },

        _setupInput: function() {
            return jQuery('<input type="number" class="input-medium">')
                .attr('id',       this.id)
                .attr('min',      this.options.min)
                .attr('max',      this.options.max)
                .attr('step',     this.options.step)
                .attr('disabled', this.disabled ? 'disabled' : null)
                .val(this.value())
        }
    });

    var Range = Property.extend({
        _lower:        undefined,
        _upper:        undefined,
        _register:     undefined,
        _initialValue: undefined,

        changeEvents: function() { return ['keyup', 'change']; },

        fix: function(event) {
            if (event.type !== 'change' && event.type !== 'blur') return this;

            var value = this.inputValue();
            var lower = value[0];
            var upper = value[1];

            if (window.isNaN(lower) || window.isNaN(upper)) return this;

            lower = new Decimal(lower);
            upper = new Decimal(upper);

            if (upper.lt(lower) && this._upper.is(event.target) && upper.gte(this.options.min)) {
                this._lower.val(upper);
            } else if (lower.gt(upper) && this._lower.is(event.target) && lower.lte(this.options.max)) {
                this._upper.val(lower);
            }

            return this;
        },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined')
                return [window.parseFloat(this._lower.val()), window.parseFloat(this._upper.val())];
            this._lower.val(newValue[0]);
            this._upper.val(newValue[1]);

            return this;
        },

        mirror: function() {
            if (typeof this._mirror !== 'undefined') {
                var value = this.value();
                this._mirror.show(value[0] + '-' + value[1]);
            }

            return this;
        },

        registerOn: function() {
            return this._register;
        },

        validate: function() {
            var value = this.inputValue();
            var lower = value[0];
            var upper = value[1];

            return !window.isNaN(lower) && !window.isNaN(upper)
                && this.options.min.lte(lower) && this.options.min.lte(upper)
                && this.options.max.gte(lower) && this.options.max.gte(upper)
                && this._initialValue[0].minus(lower).mod(this.options.step).eq(0)
                && this._initialValue[1].minus(upper).mod(this.options.step).eq(0)
        },

        _preSetup: function() {
            this.options.min  = new Decimal(get(this.options, 'min', -Decimal.MAX_VALUE));
            this.options.max  = new Decimal(get(this.options, 'max',  Decimal.MAX_VALUE));
            this.options.step = this.options.step ? new Decimal(this.options.step) : null;

            if (this.options.min.gt(this.options.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.options.min + '/' + this.options.max;
            } else if (this.options.step && this.options.step.lt(0)) {
                throw '[VALUE ERROR] step must be positive: ' + this.options.step;
            }

            return this;
        },

        _postSetup: function() {
            var value = this.value();

            this._lower        = this.input.children().eq(0);
            this._upper        = this.input.children().eq(1);
            this._register     = jQuery(this._lower).add(this._upper);

            this._initialValue = [new Decimal(value[0]), new Decimal(value[1])];

            return this;
        },

        _setupInput: function() {
            var value = this.value();
            var form  = jQuery('<form class="form-inline">');
            var lower = this._setupMiniNumber(value[0]).attr('id', this.id);
            var upper = this._setupMiniNumber(value[1]);

            return form.append(lower, upper);
        },

        _setupMiniNumber: setupMiniNumber
    });

    var Select = Property.extend({
        _options: undefined,

        changeEvents: function() { return ['change']; },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return this.input.val();
            this._options
                .attr('selected', null)
                .filter("[value='" + newValue + "']")
                .attr('selected', 'selected');

            return this;
        },

        _preSetup: function() {
            var value = this.value();

            if (!this.options.choices || this.options.choices.length < 2) {
                throw '[VALUE ERROR] not enough choices: ' + this.options.choices;
            } else if (typeof value !== 'undefined' && _.indexOf(this.options.choices, value) === -1) {
                throw '[VALUE ERROR] no choice for value: ' + value + '/' + this.options.choices;
            }

            return this;
        },

        _postSetup: function() {
            this._options = this.input.children('options');

            return this;
        },

        _setupInput: function() {
            var value    = this.value();
            var select   = jQuery('<select class="input-medium">');
            var selected = typeof value !== 'undefined' ? value : this.options.choices[0];

            // model each choice as an option of the select
            _.each(this.options.choices, function(choice) {
                select.append(jQuery('<option>')
                    .html(choice)
                    .attr('value', choice)
                    .attr('selected', choice === selected ? 'selected' : null)
                    .appendTo(select));
            });

            return select;
        }
    });

    var Text = Property.extend({
        changeEvents: function() { return ['keyup', 'change']; },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return this.input.val();
            this.input.val(newValue);

            return this;
        },

        _setupInput: function() {
            return jQuery('<input type="text" class="input-medium">')
                .attr('id', this.id)
                .attr('disabled', this.options.disabled ? 'disabled' : null)
                .val(this.value());
        }
    });

    var newFrom = function(node, mirror, propertyDefinition) {
        var kind = propertyDefinition.kind;

             if (kind === 'checkbox')     return new Checkbox(node, mirror, propertyDefinition);
        else if (kind === 'compound')     return new Compound(node, mirror, propertyDefinition);
        else if (kind === 'neighborhood') return new Neighborhood(node, mirror, propertyDefinition);
        else if (kind === 'number')       return new Numeric(node, mirror, propertyDefinition);
        else if (kind === 'range')        return new Range(node, mirror, propertyDefinition);
        else if (kind === 'select')       return new Select(node, mirror, propertyDefinition);
        else if (kind === 'text')         return new Text(node, mirror, propertyDefinition);

        throw 'Unknown property kind: ' + kind;
    };

    return {
        Checkbox:     Checkbox,
        Compound:     Compound,
        Neighborhood: Neighborhood,
        Numeric:      Numeric,
        Range:        Range,
        Text:         Text,

        newFrom:      newFrom
    };
});
