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

    Property.prototype.show = function(container, index) {
        this._container = container;

        if (typeof index === 'undefined' || container.children().length === 0) {
            this._container.append(this._element)
        } else {
            this._container.children().eq(index || 0).before(this._element);
        }

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
            .html(text || this.options().name)
            .addClass(Config.Classes.PROPERTY_LABEL);
    }

    Property.prototype._setupMirror = function() {
        var mirror        = this.options().mirror;
        var mirrorClasses = this.options().mirrorClass

        // if a container on where to mirror the value was given
        // we need to create a container and append it to it
        if (mirror) {
            if (typeof mirrorClasses === 'string') {
                mirrorClasses = [mirrorClasses];
            }

            var container = mirror.children('.' + Config.Classes.NODE_LABELS);
            if (container.length === 0) {
                container = jQuery('<div>')
                    .addClass(Config.Classes.NODE_LABELS)
                    .appendTo(mirror)
                    .width(Config.Node.LABEL_WIDTH)
                    .css({
                        top:  Config.Grid.SIZE,
                        left: Config.Grid.HALF_SIZE - Config.Node.HALF_LABEL_WIDTH
                });
            }

            this._mirror = jQuery('<span>')
                .html(this._mirrorString())
                .addClass(Config.Classes.NODE_LABEL);

            _.each(mirrorClasses, function(mirrorClass) {
                this._mirror.addClass(mirrorClass);
            }.bind(this));

            return this._mirror.appendTo(container);
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
        
        var options   = this.options().options;
        var value     = this.options().value;
        if (_.indexOf(options, value) === -1) options.unshift(value);

        this._selectElement = this._element.find('select');
        this._setupMirror();
    }
    Select.Extends(Property);

    Select.prototype.show = function(container, index) {
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
        Select.Super.show.call(this, container, index);
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
        var choices = options.choices;

        // check whether choice are present and that there are at least two to choose from
        if (typeof choices === 'undefined' || choices.length < 2) {
            throw 'Parameter Error - please provide at least two choices to choose from';
        }

        // which one is preselected?
        this._selected = 0;
        for (var i = 0, iLen = choices.length; i < iLen; ++i) {
            if (choices[i].selected) {
                this._selected = i;
                break;
            }
        }
        SingleChoice.Super.constructor.call(this, options, node);
        this._radios = this._element.find('input:radio');
        this._setupMirror();
    }
    SingleChoice.Extends(Property);

    SingleChoice.prototype.hide = function() {
        this._choice().hide();
        SingleChoice.Super.hide.call(this);
    }

    SingleChoice.prototype.show = function(container, index) {
        this._element = this._setupElement();
        this._radios  = this._element.find('input:radio');
        SingleChoice.Super.show.call(this, container, index);

        this._choice().show(container);
        if (this.options().mirror) this._setupChoiceHandler(this._choice());
    }

    SingleChoice.prototype.value = function() {
        return this.options().choices[this._selected].input.value();
    }

    SingleChoice.prototype._afterAppend = function() {
        this._element.trigger('create');
    }

    SingleChoice.prototype._callbackElement = function() {
        return this._radios;
    }

    SingleChoice.prototype._change = function(eventObject) {
        var index = this._container.children().index(this._choice()._element);

        this._choice().hide();
        this._selected = this._radios.index(eventObject.target);
        this._choice().show(this._container, index);

        if (this.options().mirror) {
            this._mirror.html(this._mirrorString());
            this._setupChoiceHandler(this._choice());
        }
    }

    SingleChoice.prototype._choice = function() {
        return this.options().choices[this._selected].input;
    }

    SingleChoice.prototype._setupChoiceHandler = function(choice) {
        var _this = this;
        var choiceOptions = choice.options();

        _.each(Config.Properties.Events, function(eventName) {
            if (choice['_' + eventName] || choiceOptions[eventName]) {
                choice._callbackElement().bind(eventName, function() {
                    _this._mirror.html(_this._mirrorString());
                });
            }
        })
    }

    SingleChoice.prototype._setupElement = function() {
        var fieldcontain = this._setupFieldcontain();
        var fieldset     = this._setupFieldset();

        _.each(this.options().choices, function(choice, index) {
            var _id   = this._id + '-' + index;
            var input = jQuery('<input type="radio">')
                .attr('data-mini', true)
                .attr('name', this._id)
                .attr('id', _id)
                .attr('value', choice.name)
                .attr('checked', index === this._selected ? 'checked' : undefined);
            var label = jQuery('<label>')
                .attr('for', _id)
                .html(choice.name);

            fieldset.append(input, label);
        }.bind(this));

        return fieldcontain.append(fieldset);
    }

    SingleChoice.prototype._setupFieldset = function() {
        var fieldset = jQuery('<fieldset>').attr('data-role', 'controlgroup');
        var legend   = jQuery('<legend>').html(this.name());

        fieldset.append(legend);
        _.each(this.options().choices, function(choice) {

        })

        return fieldset;
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