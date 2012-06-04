define(['require-config', 'require-oop'], function(Config) {

    /*
     *  Abstract Property
     */
    function Property(node, options) {
        // skip inheritance call
        if (this.constructor === Property) return;

        this._node     = node;
        this._name     = options.name  || '';
        this._type     = options.type  || 'text';
        this._hasLabel = options.label || false;


        this._value    = typeof options.value === 'undefined' ? ''   : options.value;
        this._edit     = typeof options.edit  === 'undefined' ? true : options.edit;

        if (this._type === 'number') {
            this._min  = typeof options.min  === 'undefined' ? 0 : options.min;
            this._max  = typeof options.max  === 'undefined' ? Number.MAX_VALUE : options.max;
            this._step = typeof options.step === 'undefined' ? 1 : options.step;
        }

        if (this._hasLabel) {
            this._label = jQuery('<span>').html(this._value);
            this._node.addLabel(this._label);
        }
    }

    Property.prototype.show = function() {
        throw 'Abstract Method - overwrite in subclass';
    }

    /*
     *  Text Property
     */
    function Text(node, options) {
        Text.Super.constructor.call(this, node, options);

        this._onBlur   = options.onBlur   || jQuery.noop;
        this._onChange = options.onChange || jQuery.noop;
        this._onFocus  = options.onFocus  || jQuery.noop;
        this._onKeyup  = options.onKeyup  || jQuery.noop;
    }
    Text.Extends(Property);

    Text.prototype.show = function(container) {
        var id               = _.uniqueId('label');
        this._fieldcontainer = jQuery('<div data-role="fieldcontain">');
        this._inputLabel     = jQuery('<label>');
        this._input          = jQuery('<input data-mini="true" type="' + this._type + '">');

        this._fieldcontainer
            .append(this._inputLabel, this._input)
            .appendTo(container)
            .fieldcontain();

        this._inputLabel
            .attr('for', id)
            .html(this._name)
            .addClass(Config.Classes.PROPERTY_LABEL);

        this._input
            .attr('id', id)
            .attr('min', this._min)
            .attr('max', this._max)
            .attr('step', this._step)
            .attr('disabled', !this._edit)

            .val(this._value)
            .addClass(Config.Classes.PROPERTY_TEXT)
            .textinput()

            // callbacks
            .blur(this._blur.bind(this))
            .change(this._change.bind(this))
            .focus(this._focus.bind(this))
            .keyup(this._keyup.bind(this));
    }

    Text.prototype.value = function() {
        return this._value;
    }

    Text.prototype._blur = function(eventObject) {
        this._onBlur(eventObject, this);
    }

    Text.prototype._change = function(eventObject) {
        // TODO: send properties changed command here
        if (this._type === 'number') {
            var n = parseFloat(this._input.val());

            this._value = Math.max(this._min, Math.min(n, this._max));
            this._input.val(this._value)

        } else {
            this._value = this._input.val();
        }

        this._onChange(eventObject, this); 
    }

    Text.prototype._focus = function(eventObject) {
        this._onFocus(eventObject, this);
    }

    Text.prototype._keyup = function(eventObject) {
        if (this._hasLabel) {
            this._value = this._input.val();
            this._label.html(this._value);
        }

        this._onKeyup(eventObject, this);
    }

    return {
        Text: Text
    };
});