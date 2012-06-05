define(['require-config', 'require-oop'], function(Config) {

    /*
     *  Abstract Property
     */
    function Property(options, node) {
        // skip inheritance call
        if (this.constructor === Property) return;

        this._id      = _.uniqueId('property');
        this._node    = node;
        this._options = jQuery.extend({}, Config.Properties.Defaults.Basic, options);

        // remove the value member from the options and keep track of it for ourselves
        this._value   = this._options.value;
        delete this._options.value;

        if (typeof this._options.mirrorClass === 'string') this._options.mirrorClass = [this._options.mirrorClass];

        // if a container on where to mirror the value was given
        // we need to create a container and append it to it
        if (this._options.mirror) {
            this._mirror = this._setupMirror().appendTo(this._options.mirror); 
        }
    }

    Property.prototype.name = function() {
        return this._options.name;
    }

    Property.prototype.options = function() {
        return this._options;
    }

    Property.prototype.show = function(container) {
        this._fieldcontain = this._setupFieldcontain();
        this._label        = this._setupLabel();
        this._input        = this._setupInput();

        // have to call the jQuery Mobile methods here - elements have to be in DOM
        this._fieldcontain
            .append(this._label, this._input)
            .appendTo(container)
            .fieldcontain();
        this._input.textinput();

        this._setupCallbacks(this._input);

        return this;
    }

    Property.prototype.value = function() {
        return this._value;
    }

    Property.prototype._setupCallbacks = function(input) {
        _.each(Config.Properties.Events, function(eventType) {
            var ownCallback    = this['_' + eventType];
            var optionCallback = this._options[eventType];

            // important: do not change order here
            // first we do our stuff (ownCallback) and then allow them 
            // to alter our behaviour by calling the programmers registered function
            if (typeof ownCallback    !== 'undefined') input.bind(eventType, ownCallback.bind(this));
            if (typeof optionCallback !== 'undefined') input.bind(eventType, optionCallback.bind(this));
        }.bind(this));

        return this;
    }

    Property.prototype._setupFieldcontain = function() {
        return jQuery('<div>').attr('data-role', 'fieldcontain');
    }

    Property.prototype._setupInput = function() {
        throw 'Abstract Method - declare here how the property input field looks like';
    }

    Property.prototype._setupLabel = function() {
        return jQuery('<label>')
            .attr('for', this._id)
            .html(this._options.name)
            .addClass(Config.Classes.PROPERTY_LABEL);
    }

    Property.prototype._setupMirror = function() {
        var mirror = jQuery('<span>')
            .html(this._mirrorString())
            .addClass(Config.Classes.NODE_LABEL)
            .width(Config.Grid.SIZE);

        _.each(this._options.mirrorClass, function(mirrorClass) {
            mirror.addClass(mirrorClass);
        }.bind(this));

        return mirror;
    }

    Property.prototype._mirrorString = function() {
        return this._options.mirrorPrefix + this._value + this._options.mirrorSuffix;
    }

    /*
     *  Text Property
     */
    function Text(options, node) {
        Text.Super.constructor.call(this, options, node);

        // input type
        this._options.type = this._options.type || 'text';

        if (this._options.type === 'number') {
            this._options = jQuery.extend({}, Config.Properties.Defaults.Number, this._options);

        } else if (this._type === 'pattern') {
            this._options = jQuery.extend({}, Config.Properties.Defaults.Pattern, this._options);
        }
    }
    Text.Extends(Property);

    Text.prototype._setupInput = function() {
        return jQuery('<input data-mini="true" type="' + this._options.type + '">')
            .attr('id',       this._id)
            .attr('min',      this._options.min)
            .attr('max',      this._options.max)
            .attr('step',     this._options.step)
            .attr('disabled', this._options.disabled)

            .val(this._value)
            .addClass(Config.Classes.PROPERTY_TEXT);
    }

    Text.prototype._change = function(eventObject) {
        // TODO: send properties changed command here
        if (this._options.type === 'number') {
            var n = parseFloat(this._input.val());
            if (Number.isNaN(n)) n = this._options.min;

            this._value = Math.max(this._options.min, Math.min(n, this._options.max));
            this._input.val(this._value)

        } else {
            this._value = this._input.val();
        }

        this._mirror.html(this._mirrorString());
    }

    Text.prototype._keyup = function(eventObject) {
        if (this._mirror) {
            this._value = this._input.val();
            this._mirror.html(this._mirrorString());
        }
    }

    /*
     *  Select Property
     */
    function Select(options, node) {

    }
    Select.Extends(Property);

    return {
        Text:   Text,
        Select: Select
    };
});