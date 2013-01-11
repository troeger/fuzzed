define(['config', 'class', 'underscore'], function(Config, Class) {

    var defaultFloat = function(object, key, defaultValue) {
        var value = window.parseFloat(object[key]);

        return window.isNaN(value) ? defaultValue : value;
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
            if (typeof newValue === 'undefined') return this.node[this.options.property];
            this.node[this.options.property] = newValue;

            return this;
        },

        blurEvents: function() { return []; },

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

    var Number = Property.extend({
        min:  undefined,
        max:  undefined,
        step: undefined,

        _initialValue: undefined,

        blurEvents:   function() { return ['blur']; },
        changeEvents: function() { return ['keyup', 'change']; },

        inputValue: function(newValue) {
            if (typeof newValue === 'undefined') return window.parseFloat(this.input.val());
            this.input.val(newValue);

            return this;
        },

        validate: function() {
            var value = this.inputValue();

            return !window.isNaN(value) && this.options.min <= value && value <= this.options.max
                && (value - this._initialValue) % this.options.step == 0;
        },

        _preSetup: function() {
            this.options.min  = defaultFloat(this.options, 'min', -window.Number.MAX_VALUE);
            this.options.max  = defaultFloat(this.options, 'max',  window.Number.MAX_VALUE);
            this.options.step = defaultFloat(this.options, 'step', 1);

            if (this.options.min > this.options.max) {
                throw '[VALUE ERROR] bound violation min/max: ' + this.options.min + '/' + this.options.max;
            }

            return this;
        },

        _postSetup: function() {
            this._initialValue = this.value();
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

        blurEvents:   function() { return ['blur']; },
        changeEvents: function() { return ['keyup', 'change']; },

        fix: function(event) {
            if (event.type !== 'change' && event.type !== 'blur') return this;

            var value = this.inputValue();
            var lower = value[0];
            var upper = value[1];

            if (window.isNaN(lower) || window.isNaN(upper)) return this;

            if (upper < lower && this._upper.is(event.target) && upper >= this.options.min) {
                this._lower.val(upper);
            } else if (lower > upper && this._lower.is(event.target) && lower <= this.options.max) {
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
                && this.options.min <= lower && this.options.min <= upper
                && lower <= this.options.max && upper <= this.options.max
                && (lower - this._initialValue[0]) % this.options.step == 0
                && (upper - this._initialValue[1]) % this.options.step == 0;
        },

        _preSetup: function() {
            this.options.min  = defaultFloat(this.options, 'min', -window.Number.MAX_VALUE);
            this.options.max  = defaultFloat(this.options, 'max',  window.Number.MAX_VALUE);
            this.options.step = defaultFloat(this.options, 'step', 1);

            return this;
        },

        _postSetup: function() {
            this._lower        = this.input.children().eq(0);
            this._upper        = this.input.children().eq(1);
            this._register     = jQuery(this._lower).add(this._upper);
            this._initialValue = this.value();

            return this;
        },

        _setupBoundsInput: function(value) {
            return jQuery('<input type="number" class="input-mini">')
                .attr('min',      this.options.min)
                .attr('max',      this.options.max)
                .attr('step',     this.options.step)
                .attr('disabled', this.options.disabled ? 'disabled' : null)
                .val(value);
        },

        _setupInput: function() {
            var value = this.value();
            var form  = jQuery('<form class="form-inline">');
            var lower = this._setupBoundsInput(value[0]).attr('id', this.id);
            var upper = this._setupBoundsInput(value[1]);

            return form.append(lower, upper);
        }
    });

    var Text = Property.extend({
        blurEvents:   function() { return ['blur']; },
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

             if (kind === 'checkbox') return new Checkbox(node, mirror, propertyDefinition)
        else if (kind === 'number')   return new   Number(node, mirror, propertyDefinition)
        else if (kind === 'range')    return new    Range(node, mirror, propertyDefinition)
        else if (kind === 'text')     return new     Text(node, mirror, propertyDefinition);

        return new Text(node, mirror, propertyDefinition);
        //throw 'Unknown property kind: ' + kind;
    };

    return {
        Checkbox: Checkbox,
        Number:   Number,
        Range:    Range,
        Text:     Text,

        newFrom:  newFrom
    };
});
