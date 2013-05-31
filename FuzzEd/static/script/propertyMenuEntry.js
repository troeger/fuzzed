define(['class', 'config'], function(Class, Config) {

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

        fix: function(event, ui) {},

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

    var NumericEntry = Entry.extend({
        _setupInput: function() {
            this.inputs = jQuery('<input type="number" class="input-medium">')
                .attr('id',       this.id)
                .attr('min',      this.property.min)
                .attr('max',      this.property.max)
                .attr('step',     this.property.step);

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return window.parseFloat(this.inputs.val());
            this.inputs.val(newValue);

            return this;
        },

        changeEvents: function() {
            return ['change', 'keyup', 'cut', 'paste'];
        }
    });

    var TextEntry = Entry.extend({
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
        },

        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        }
    });

    return {
        'NumericEntry': NumericEntry,
        'TextEntry': TextEntry
    }
});
