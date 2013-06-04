define(['class', 'config'], function(Class, Config) {

    var NUMBER_REGEX = /^[+\-]?(?:0|[1-9]\d*)(?:[.,]\d*)?(?:[eE][+\-]?\d+)?$/;

    var Entry = Class.extend({
        id:            undefined,
        property:      undefined,
        container:     undefined,
        inputs:        undefined,

        _editing:      false,
        _preEditValue: undefined,
        _editTarget:   undefined,
        _timer:        undefined,

        init: function(property) {
            this.id = _.uniqueId('property');
            this.property = property;

            this._setupVisualRepresentation()
                ._setupEvents();
        },

        blurEvents: function() {
            return ['blur', 'remove'];
        },

        blurred: function(event, ui) {
            this.fix(event, ui);

            this._abortChange().unwarn();

            if (this.property.validate(this._value(), {})) {
                this.property.setValue(this._value(), this);
            } else {
                this._value(this._preEditValue);
                this.property.setValue(this._preEditValue, this, false);
            }

            this._editing      = false;
            this._editTarget   = undefined;
            this._preEditValue = undefined;

            return this;
        },

        changeEvents: function() {
            return [];
        },

        changed: function(event, ui) {
            if (!this._editing) {
                this._preEditValue = this.property.value;
            }

            var validationResult = {};
            this._editing    = true;
            this._editTarget = event.target;

            this.fix(event, ui);

            if (this.property.validate(this._value(), validationResult)) {
                this._sendChange().unwarn();
            } else {
                this._abortChange().warn(validationResult.message);
            }

            return this;
        },

        _abortChange: function() {
            window.clearTimeout(this._timer);

            return this;
        },

        _sendChange: function() {
            // discard old timeout
            window.clearTimeout(this._timer);
            // create a new one
            this._timer = window.setTimeout(function() {
                this.property.setValue(this._value(), this);
            }.bind(this), Config.Menus.PROPERTIES_MENU_TIMEOUT);

            return this;
        },

        fix: function(event, ui) {
            return this;
        },

        show: function(on) {
            on.append(this.container);
            this._setupCallbacks();

            return this;
        },

        hide: function() {
            this.container.remove();

            return this;
        },

        warn: function(text) {
            this.container
                .addClass(Config.Classes.PROPERTY_WARNING)
                .attr('data-original-title', text)
                .tooltip('show');

            return this;
        },

        unwarn: function() {
            this.container.removeClass(Config.Classes.PROPERTY_WARNING).tooltip('hide');

            return this;
        },

        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();
            this.container.find('.controls').append(this.inputs);

            return this;
        },

        _setupContainer: function() {
            this.container = jQuery(
                '<div class="control-group" data-toggle="tooltip" data-trigger="manual" data-placement="left">\
                    <label class="control-label" for="' + this.id + '">' + (this.property.displayName || '') + '</label>\
                    <div class="controls"></div>\
                </div>'
            );

            return this;
        },

        _setupInput: function() {
            throw '[ABSTRACT] subclass responsibility';
        },

        _setupCallbacks: function() {
            _.each(this.blurEvents(), function(event) {
                this.inputs.on(event, this.blurred.bind(this));
            }.bind(this));

            _.each(this.changeEvents(), function(event) {
                this.inputs.on(event, this.changed.bind(this));
            }.bind(this));

            return this;
        },

        _setupEvents: function() {
            jQuery(this.property).on(Config.Events.NODE_PROPERTY_CHANGED, function(event, newValue, issuer) {
                // ignore changes issued by us in order to prevent race conditions with the user
                if (issuer === this) return;
                this._value(newValue);
            }.bind(this));
        },

        _value: function(newValue) {
            throw '[ABSTRACT] subclass responsibility';
        }
    });

    var BoolEntry = Entry.extend({
        blurEvents: function() { return ['change']; },

        _setupInput: function() {
            this.inputs = jQuery('<input type="checkbox">').attr('id', this.id);

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.attr('checked') === 'checked';
            this.inputs.attr('checked', newValue ? 'checked' : null);

            return this;
        }
    });

    var NumericEntry = Entry.extend({
        changeEvents: function() {
            return ['change', 'keyup', 'cut', 'paste'];
        },

        _setupInput: function() {
            this.inputs = jQuery('<input type="number" class="input-medium">')
                .attr('id',   this.id)
                .attr('min',  this.property.min)
                .attr('max',  this.property.max)
                .attr('step', this.property.step);

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                var val = this.inputs.val();
                if (this.inputs.is(':invalid') || !NUMBER_REGEX.test(val)) return window.NaN;
                return window.parseFloat(val);
            }
            this.inputs.val(newValue);

            return this;
        }
    });

    var RangeEntry = Entry.extend({
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        fix: function(event, ui) {
            var val = this._value();
            var lower = val[0];
            var upper = val[1];

            if (_.isNaN(lower) || _.isNaN(upper)) return this;

            var target = jQuery(event.target);
            if (target.is(this.inputs.eq(0)) && lower > upper) {
                this._value([lower, lower]);
            } else if (target.is(this.inputs.eq(1)) && upper < lower) {
                this._value([upper, upper]);
            }

            return this;
        },

        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();

            jQuery('<form class="form-inline">')
                .append(this.inputs)
                .appendTo(this.container.find('.controls'));

            return this;
        },

        _setupInput: function() {
            var value = this.property.value;

            this.inputs = this._setupMiniNumeric(value[0])
                .attr('id', this.id) // clicking the label should focus the first input
                .add(this._setupMiniNumeric(value[1]));

            return this;
        },

        _setupMiniNumeric: function(value) {
            return jQuery('<input type="number" class="input-mini">')
                .attr('min',  this.property.min.toFloat())
                .attr('max',  this.property.max.toFloat())
                .attr('step', this.property.step)
                .val(value)
        },

        _value: function(newValue) {
            var lower = this.inputs.eq(0);
            var upper = this.inputs.eq(1);

            if (typeof newValue === 'undefined') {
                var lowerVal = (lower.is(':invalid') || !NUMBER_REGEX.test(lower.val()))
                    ? window.NaN : window.parseFloat(lower.val());
                var upperVal = (upper.is(':invalid') || !NUMBER_REGEX.test(upper.val()))
                    ? window.NaN : window.parseFloat(upper.val());
                return [lowerVal, upperVal];
            }
            lower.val(newValue[0]);
            upper.val(newValue[1]);

            return this;
        }
    });

    var TextEntry = Entry.extend({
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        _setupInput: function() {
            this.inputs = jQuery('<input type="text" class="input-medium">').attr('id', this.id);

            //TODO: deactivate and/or disable
            //.attr('disabled', this.options.disabled ? 'disabled' : null)

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.val();
            this.inputs.val(newValue);

            return this;
        }
    });

    return {
        'BoolEntry':    BoolEntry,
        'NumericEntry': NumericEntry,
        'RangeEntry':   RangeEntry,
        'TextEntry':    TextEntry
    }
});
