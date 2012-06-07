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
        this._element = this._setupElement();
    }

    Property.prototype.hide = function() {
        this._element.remove();
        delete this._container;

        return this;
    }

    Property.prototype.input = function() {
        return this._input;
    }

    Property.prototype.name = function() {
        return this._options.name;
    }

    Property.prototype.mirror = function() {
        return this._mirror;
    }

    Property.prototype.options = function() {
        return this._options;
    }

    Property.prototype.show = function(container) {
        this._container = container;

        this._container.append(this._element);
        this._afterAppend();
        this._setupCallbacks();

        return this;
    }

    Property.prototype.value = function() {
        throw 'Abstract Method - overwrite in subclass on how to obtain a value from the custom input';
    }

    Property.prototype._afterAppend = function() {
        // describes what happens after the element is inserted into the DOM
        // required for instance for the jQuery Mobile widget setup calls
        throw 'Abstract Method - overwrite in subclass with code that shall be executed after the element was inserted into DOM';
    }

    Property.prototype._callbackElement = function() {
        throw 'Abstract Method - return the element that shall get all callback function of _setupCallbacks registered';
    }

    Property.prototype._mirrorString = function() {
        return this._options.mirrorPrefix + this.value() + this._options.mirrorSuffix;
    }

    Property.prototype._setupCallbacks = function() {
        var input = this._callbackElement();

        _.each(Config.Properties.Events, function(eventType) {
            var ownCallback    = this['_' + eventType];
            var optionCallback = this._options[eventType];

            // important: do not change order here
            // first we do our stuff (ownCallback) and then allow programers 
            // to alter our behaviour by calling their own registered function
            if (typeof ownCallback    !== 'undefined') input.bind(eventType, ownCallback.bind(this));
            if (typeof optionCallback !== 'undefined') input.bind(eventType, optionCallback.bind(this));
        }.bind(this));

        return this;
    }

    Property.prototype._setupElement = function() {
        throw 'Abstract Method - declare here how the property input field looks like';
    }

    Property.prototype._setupFieldcontain = function() {
        return jQuery('<div>').attr('data-role', 'fieldcontain');
    }

    Property.prototype._setupLabel = function(_id, text) {
        return jQuery('<label>')
            .attr('for', _id || this._id)
            .html(text || this._options.name)
            .addClass(Config.Classes.PROPERTY_LABEL);
    }

    Property.prototype._setupMirror = function() {
        // if a container on where to mirror the value was given
        // we need to create a container and append it to it
        if (this.options().mirror) {
            if (typeof this.options().mirrorClass === 'string') {
                this.options().mirrorClass = [this.options().mirrorClass];
            }

            this._mirror = jQuery('<span>')
                .html(this._mirrorString())
                .addClass(Config.Classes.NODE_LABEL)
                .width(Config.Grid.SIZE);

            _.each(this.options().mirrorClass, function(mirrorClass) {
                this._mirror.addClass(mirrorClass);
            }.bind(this));

            return this._mirror.appendTo(this.options().mirror);
        }

        return null;
    }

    /*
     *  Select Property
     */
    function Select(options, node) {
        Select.Super.constructor.call(this, options, node);

        // sanitize the options of this object and the options of the select (options.options)
        this._options = jQuery.extend({}, Config.Properties.Defaults.Select, this._options);
        if (_.indexOf(this._options.options, this._value) === -1) this._options.options.unshift(this._value);

        this._selectElement = this._element.find('select');
        this._setupMirror();
    }
    Select.Extends(Property);

    Select.prototype.show = function(container) {
        /*
         *  Nasty hack here - I am sorry guys, when you find this and are annoyed by it get a free beer
         *  by writing to murxman@gmail.com :). Reason: jQuery Mobile in the as-is version would nest 
         *  their custom selects each time _afterAppend is called (they have a weird, not-working existence
         *  check there). Idea: Remove the element before after append, rebuild it using the currently set
         *  value in the select box and let _afterAppend therefore run on a fresh select box.
         */
        this._options.value = this.value();
        this._element = this._setupElement();
        this._selectElement = this._element.find('select');
        Select.Super.show.call(this, container);
    }

    Select.prototype.value = function() {
        return this._selectElement.val();
    }

    Select.prototype._afterAppend = function() {
        this._element.fieldcontain();
        this._selectElement.selectmenu();
    }

    Select.prototype._callbackElement = function() {
        return this._selectElement;
    }

    Select.prototype._change = function() {
        // update the mirror if we have one
        if (this._mirror) this._mirror.html(this._mirrorString());
    }

    Select.prototype._setupElement = function() {
        var fieldcontain = this._setupFieldcontain();
        var label        = this._setupLabel();
        var select       = jQuery('<select>')
            .attr('data-mini', 'true')
            .attr('id',        this._id)
            .attr('disabled',  this._options.disabled)
            .val(this.options().value)
            .addClass(Config.Classes.PROPERTY_SELECT);

        _.each(this._options.options, function(option) {
            jQuery('<option>')
                .attr('value', option)
                .attr('selected', option === this.options().value ? 'selected' : undefined)
                .html(option)
                .appendTo(select);
        }.bind(this));

        return fieldcontain
            .append(label)
            .append(select);
    }

    /*
     *  SingleChoice
     */
    function SingleChoice(options, node) {
        if (typeof options.choices === 'undefined' || options.choices.length < 2) {
            throw 'Parameter Error - please provide at least two choices to choose from';
        }
        SingleChoice.Super.constructor.call(this, options, node);

        this._options = jQuery.extend({}, Config.Properties.Defaults.SingleChoice, this._options);
        this._chosen  = this._options.chosen;
        this._radios  = this._element.find('input[type="radio"]');
        this._setupMirror();
    }
    SingleChoice.Extends(Property);

    SingleChoice.prototype.value = function() {
        return this._options.choices[this._chosen].value();
    }

    SingleChoice.prototype._afterAppend = function() {
        this._element.fieldcontain();
    }

    SingleChoice.prototype._callbackElement = function() {
        return this._radios;
    }

    SingleChoice.prototype._setupElement = function() {
        var fieldcontain = this._setupFieldcontain();
        var fieldset     = this._setupFieldset();
        var legend       = this._setupLegend();

        _.each(this._options.choices, function(choice, index) {
            var _id   = this._id + '-' + index;
            var radio = this._setupRadio(_id);
            var label = this._setupLabel(_id, choice.name);

            fieldset.append(radio, label);
        }.bind(this));

        return fieldcontain.append(fieldset.append(legend));
    }

    SingleChoice.prototype._setupFieldset = function() {
        return jQuery('<fieldset>')
            .attr('data-role', 'controlgroup')
            .attr('data-type', 'horizontal');
    }

    SingleChoice.prototype._setupLegend = function() {
        return jQuery('<legend>').html(this._options.name);
    }

    SingleChoice.prototype._setupRadio = function(_id) {
        return jQuery('<input type="radio">').attr('id', _id);
    }

    /*
     *  Text Property
     */
    function Text(options, node) {
        Text.Super.constructor.call(this, options, node);

        // option sanitization for general text fields
        this._options = jQuery.extend({}, Config.Properties.Defaults.Text, this._options);

        // enrich with additional features when we it is a number or pattern field
        if (this._options.type === 'number') {
            this._options = jQuery.extend({}, Config.Properties.Defaults.Number, this._options);

        } else if (this._type === 'pattern') {
            this._options = jQuery.extend({}, Config.Properties.Defaults.Pattern, this._options);
        }

        this._input = this._element.find('input');
        this._setupMirror();
    }
    Text.Extends(Property);

    Text.prototype.value = function() {
        return this._input.val();
    }

    Text.prototype._afterAppend = function() {
        this._element.fieldcontain();
        this._input.textinput();
    }

    Text.prototype._callbackElement = function() {
        return this._input;
    }

    Text.prototype._change = function(eventObject) {
        if (this._options.type === 'number') {
            var n = parseFloat(this.value());
            if (isNaN(n)) {
                n = this._options.min;
            }
            this._input.val(Math.max(this._options.min, Math.min(n, this._options.max)));
        }

        if (this._mirror) this._mirror.html(this._mirrorString());
    }

    Text.prototype._keyup = function(eventObject) {
        if (this._mirror) {
            this._mirror.html(this._mirrorString());
        }
    }

    Text.prototype._setupElement = function() {
        var fieldcontain = this._setupFieldcontain();
        var label        = this._setupLabel();
        var input        = jQuery('<input type="' + this._options.type + '">')
            .attr('data-mini', 'true')
            .attr('id',        this._id)
            .attr('min',       this._options.min)
            .attr('max',       this._options.max)
            .attr('step',      this._options.step)
            .attr('disabled',  this._options.disabled)
            .val(this._options.value)
            .addClass(Config.Classes.PROPERTY_TEXT);

        return fieldcontain
            .append(label)
            .append(input);
    }

    return {
        Select:       Select,
        SingleChoice: SingleChoice,
        Text:         Text
    };
});