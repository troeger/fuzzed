define(['require-config', 'require-backend', 'require-oop', 'underscore'], 
       function(Config, Backend, Class) {

    /*
     *  Abstract Property
     */
    // var Property = Class.extend({
    //     init: function(options, node) {
    //         // skip inheritance call
    //         if (this.constructor === Property) return;

    //         this._id      = _.uniqueId('property');
    //         this._node    = node;
    //         this._options = jQuery.extend({}, Config.Properties.Defaults.Basic, options);
    //         this._element = this._setupElement();
    //     },

    //     hide: function() {
    //         this._element.remove();
    //         delete this._container;

    //         return this;
    //     },

    //     input: function() {
    //         return this._input;
    //     },

    //     name: function() {
    //         return this._options.name;
    //     },

    //     displayname: function() {
    //         return this._options.displayname;
    //     },

    //     mirror: function() {
    //         return this._mirror;
    //     },

    //     options: function() {
    //         return this._options;
    //     },

    //     show: function(container, index) {
    //         this._container = container;

    //         if (typeof index === 'undefined' || container.children().length === 0 || container.children().length <= index) {
    //             this._container.append(this._element)
    //         } else {
    //             this._container.children().eq(index || 0).before(this._element);
    //         }

    //         this._afterAppend();
    //         this._setupCallbacks();

    //         return this;
    //     },

    //     value: function() {
    //         throw 'Abstract Method - overwrite in subclass on how to obtain a value from the custom input';
    //     },


    //     _afterAppend: function() {
    //         // describes what happens after the element is inserted into the DOM
    //         // required for instance for the jQuery Mobile widget setup calls
    //         throw 'Abstract Method - overwrite in subclass with code that shall be executed after the element was inserted into DOM';
    //     },

    //     _callbackElement: function() {
    //         throw 'Abstract Method - return the element that shall get all callback function of _setupCallbacks registered';
    //     },

    //     _mirrorString: function() {
    //         return this._options.mirrorPrefix + this.value() + this._options.mirrorSuffix;
    //     },

    //     _sendChange: function() {
    //         if (this.name()) {
    //             Backend.changeProperty(this._node, this.name(), this.value());
    //         }
    //     },

    //     _setupCallbacks: function() {
    //         var input = this._callbackElement();

    //         _.each(Config.Properties.Events, function(eventType) {
    //             var ownCallback    = this['_' + eventType];
    //             var optionCallback = this._options[eventType];

    //             // important: do not change order here
    //             // first we do our stuff (ownCallback) and then allow programers
    //             // to alter our behaviour by calling their own registered function
    //             if (typeof ownCallback    !== 'undefined') input.bind(eventType, ownCallback.bind(this));
    //             if (typeof optionCallback !== 'undefined') input.bind(eventType, optionCallback.bind(this));
    //         }.bind(this));

    //         return this;
    //     },

    //     _setupElement: function() {
    //         throw 'Abstract Method - declare here how the property input field looks like';
    //     },

    //     _setupFieldcontain: function() {
    //         return jQuery('<div>').attr('data-role', 'fieldcontain');
    //     },

    //     _setupLabel: function(_id, text) {
    //         return jQuery('<label>')
    //             .attr('for', _id || this._id)
    //             .html(text || this.options().displayname)
    //             .addClass(Config.Classes.PROPERTY_LABEL);
    //     },

    //     _setupMirror: function() {
    //         var mirror        = this.options().mirror;
    //         var mirrorClasses = this.options().mirrorClass

    //         // if a container on where to mirror the value was given
    //         // we need to create a container and append it to it
    //         if (mirror) {
    //             if (typeof mirrorClasses === 'string') {
    //                 mirrorClasses = [mirrorClasses];
    //             }

    //             this._labels = mirror.children('.' + Config.Classes.NODE_LABELS);
    //             if (this._labels.length === 0) {
    //                 this._labels = jQuery('<div>')
    //                     .addClass(Config.Classes.NODE_LABELS)
    //                     .appendTo(mirror)
    //                     .width(Config.Node.LABEL_WIDTH)
    //                     .css({
    //                         top:  Config.Grid.SIZE + Config.Node.OPTIONAL_INDICATOR_RADIUS * 2,
    //                         left: Config.Grid.HALF_SIZE - Config.Node.HALF_LABEL_WIDTH
    //                     });
    //             }

    //             this._mirror = jQuery('<span>')
    //                 .html(this._mirrorString())
    //                 .addClass(Config.Classes.NODE_LABEL)
    //                 .appendTo(this._labels);

    //             _.each(mirrorClasses, function(mirrorClass) {
    //                 this._mirror.addClass(mirrorClass);
    //             }.bind(this));

    //             return this._mirror.appendTo(this._labels);
    //         }

    //         return null;
    //     }
    // });

    // /*
    //  *  Range Property
    //  */
    // var Range = Property.extend({
    //     init: function(options, node) {
    //         this._options = jQuery.extend({}, Config.Properties.Defaults.Range, this._options);
    //         this._super(options, node);

    //         var inputs = this._element.find('input');
    //         this._min  = inputs.eq(0);
    //         this._max  = inputs.eq(1);
    //         this._setupMirror();
    //     },

    //     value: function() {
    //         return [this._min.val(), this._max.val()];
    //     },

    //     _afterAppend: function() {
    //         this._min.textinput();
    //         this._max.textinput();
    //         this._element.fieldcontain();
    //     },

    //     _callbackElement: function() {
    //         return this._min.add(this._max);
    //     },

    //     _change: function(eventObject) {
    //         var options = this.options();
    //         var value   = this.value();
    //         var min     = parseFloat(value[0]);
    //         var max     = parseFloat(value[1]);

    //         if (isNaN(min)) min = options.min;
    //         if (isNaN(max)) max = options.max;

    //         if (min > max && this._min.is(eventObject.target)) {
    //             max = min;
    //         } else if (min > max && this._max.is(eventObject.target)) {
    //             min = max;
    //         }

    //         this._min.val(min);
    //         this._max.val(max);
    //         if (this._mirror) this._mirror.html(this._mirrorString());

    //         this._sendChange();
    //     },

    //     _keyup: function(eventObject) {
    //         if (this._mirror) this._mirror.html(this._mirrorString());
    //     },

    //     _mirrorString: function() {
    //         var value = this.value();
    //         return this._options.mirrorPrefix + value[0] + '-' + value[1] + this._options.mirrorSuffix;
    //     },

    //     _setupElement: function() {
    //         var fieldcontain = this._setupFieldcontain();
    //         var label        = this._setupLabel();
    //         var options      = this.options();

    //         var min = jQuery('<input type="number">')
    //             .attr('data-mini', 'true')
    //             .attr('id',        this._id)
    //             .attr('min',       options.min)
    //             .attr('max',       options.max)
    //             .attr('step',      options.step)
    //             .attr('disabled',  options.disabled)
    //             .val(this._options.value[0])
    //             .addClass(Config.Classes.PROPERTY_TEXT);

    //         var max = min
    //             .clone()
    //             .attr('id',  this._id + '-max')
    //             .val(options.value[1])
    //             .addClass(Config.Classes.PROPERTY_RANGE_MAX);

    //         min.addClass(Config.Classes.PROPERTY_RANGE_MIN);

    //         return fieldcontain
    //             .append(label)
    //             .append(min)
    //             .append(max);
    //     }
    // });

    // /*
    //  *  Radio Property
    //  */
    // var Radio = Property.extend({
    //     init: function(options, node) {
    //         // sanitize options
    //         this._options = jQuery.extend({}, Config.Properties.Defaults.Radio, options);
    //         if (this._options.options.length < 2) {
    //             throw 'Parameter Error - provide at least two radio button options';
    //         }

    //         var valueIndex = _.indexOf(this._options.options, this._options.value)
    //         // value not set? then preselect the first
    //         if (typeof this._options.value === 'undefined') {
    //             this._options.value = this._options.options[0];

    //             // value set but not in the options? show at first position
    //         } else if (valueIndex < 0) {
    //             this._options.options.unshift(this._options.value);
    //         }

    //         this._super(options, node);

    //         this._radios   = this._element.find('input:radio');
    //         this._selected = _.indexOf(this.options().options, this.options().value);
    //         this._setupMirror();
    //     },

    //     show: function(container, index) {
    //         this._element = this._setupElement();
    //         this._radios  = this._element.find('input:radio');
    //         this._super(container, index);
    //     },

    //     value: function() {
    //         return this._radios.eq(this._selected).val();
    //     },

    //     _afterAppend: function() {
    //         this._element.trigger('create');
    //     },

    //     _callbackElement: function() {
    //         return this._radios;
    //     },

    //     _change: function(eventObject) {
    //         this._selected = this._radios.index(eventObject.target);

    //         if (this.options().mirror) {
    //             this._mirror.html(this._mirrorString());
    //         }
    //         this._sendChange();
    //     },

    //     _setupElement: function() {
    //         var fieldcontain = this._setupFieldcontain();
    //         var fieldset     = this._setupFieldset();

    //         _.each(this.options().options, function(option, index) {
    //             var _id   = this._id + '-' + index;
    //             var input = jQuery('<input type="radio">')
    //                 .attr('data-mini', true)
    //                 .attr('name', this._id)
    //                 .attr('id', _id)
    //                 .attr('value', option)
    //                 .attr('checked', index === this._selected ? 'checked' : undefined);
    //             var label = jQuery('<label>')
    //                 .attr('for', _id)
    //                 .html(option);

    //             fieldset.append(input, label);
    //         }.bind(this));

    //         return fieldcontain.append(fieldset);
    //     },

    //     _setupFieldset: function() {
    //         return jQuery('<fieldset>')
    //             .attr('data-role', 'controlgroup')
    //             .append(jQuery('<legend>').html(this.displayname()));
    //     }
    // });

    // /*
    //  *  Select Property
    //  */
    // var Select = Property.extend({
    //     init: function(options, node) {
    //         this._super(options, node);

    //         // sanitize the options of this object and the options of the select (options.options)
    //         this._options = jQuery.extend({}, Config.Properties.Defaults.Select, this._options);

    //         var options   = this.options().options;
    //         var value     = this.options().value;
    //         if (_.indexOf(options, value) === -1) options.unshift(value);

    //         this._selectElement = this._element.find('select');
    //         this._setupMirror();
    //     },

    //     show: function(container, index) {
    //         /*
    //          *  XXX: Nasty hack here - I am sorry guys, when you find this and are annoyed by it get a free beer
    //          *  by writing to murxman@gmail.com :). Reason: jQuery Mobile in the as-is version would nest
    //          *  their custom selects each time _afterAppend is called (they have a weird, not-working existence
    //          *  check there). Idea: Remove the element before after append, rebuild it using the currently set
    //          *  value in the select box and let _afterAppend therefore run on a fresh select box.
    //          *
    //          *  And what about coffee? :P [Frank]
    //          *  This will hopefully be solved by using Bootstrap.
    //          */
    //         this._options.value = this.value();
    //         this._element = this._setupElement();
    //         this._selectElement = this._element.find('select');
    //         this._super(container, index);
    //     },

    //     value: function() {
    //         return this._selectElement.val();
    //     },

    //     _afterAppend: function() {
    //         this._element.fieldcontain();
    //         this._selectElement.selectmenu();
    //     },

    //     _callbackElement: function() {
    //         return this._selectElement;
    //     },

    //     _change: function() {
    //         // update the mirror if we have one
    //         if (this._mirror) this._mirror.html(this._mirrorString());
    //         this._sendChange();
    //     },

    //     _setupElement: function() {
    //         var fieldcontain = this._setupFieldcontain();
    //         var label        = this._setupLabel();
    //         var select       = jQuery('<select>')
    //             .attr('data-mini', 'true')
    //             .attr('id',        this._id)
    //             .attr('disabled',  this._options.disabled)
    //             .val(this.options().value)
    //             .addClass(Config.Classes.PROPERTY_SELECT);

    //         _.each(this._options.options, function(option) {
    //             jQuery('<option>')
    //                 .attr('value', option)
    //                 .attr('selected', option === this.options().value ? 'selected' : undefined)
    //                 .html(option)
    //                 .appendTo(select);
    //         }.bind(this));

    //         return fieldcontain
    //             .append(label)
    //             .append(select);
    //     }
    // });

    // /*
    //  *  SingleChoice
    //  */
    // var SingleChoice = Property.extend({
    //     init: function(options, node) {
    //         var choices = options.choices;

    //         // check whether choice are present and that there are at least two to choose from
    //         if (typeof choices === 'undefined' || choices.length < 2) {
    //             throw 'Parameter Error - please provide at least two choices to choose from';
    //         }

    //         // which one is preselected?
    //         this._selected = 0;
    //         for (var i = 0, iLen = choices.length; i < iLen; ++i) {
    //             if (choices[i].selected) {
    //                 this._selected = i;
    //                 break;
    //             }
    //         }
    //         this._super(options, node);
    //         this._radios = this._element.find('input:radio');
    //         this._setupMirror();
    //     },

    //     hide: function() {
    //         this._choice().hide();
    //         this._super();
    //     },

    //     show: function(container, index) {
    //         this._element = this._setupElement();
    //         this._radios  = this._element.find('input:radio');
    //         this._super(container, index);

    //         this._choice().show(container);
    //         if (this.options().mirror) this._setupChoiceHandler(this._choice());
    //     },

    //     value: function() {
    //         return this.options().choices[this._selected].input.value();
    //     },

    //     _afterAppend: function() {
    //         this._element.trigger('create');
    //     },

    //     _callbackElement: function() {
    //         return this._radios;
    //     },

    //     _change: function(eventObject) {
    //         var index = this._container.children().index(this._choice()._element);

    //         this._choice().hide();
    //         this._selected = this._radios.index(eventObject.target);
    //         this._choice().show(this._container, index);

    //         if (this.options().mirror) {
    //             this._mirror.html(this._mirrorString());
    //             this._setupChoiceHandler(this._choice());
    //         }

    //         this._sendChange();
    //     },

    //     _choice: function() {
    //         return this.options().choices[this._selected].input;
    //     },

    //     _setupChoiceHandler: function(choice) {
    //         var _this = this;
    //         var choiceOptions = choice.options();

    //         _.each(Config.Properties.Events, function(eventName) {
    //             if (choice['_' + eventName] || choiceOptions[eventName]) {
    //                 choice._callbackElement().bind(eventName, function() {
    //                     _this._mirror.html(_this._mirrorString());
    //                     _this._sendChange();
    //                 });
    //             }
    //         });
    //     },

    //     _setupElement: function() {
    //         var fieldcontain = this._setupFieldcontain();
    //         var fieldset     = this._setupFieldset();

    //         _.each(this.options().choices, function(choice, index) {
    //             var _id   = this._id + '-' + index;
    //             var input = jQuery('<input type="radio">')
    //                 .attr('data-mini', true)
    //                 .attr('name', this._id)
    //                 .attr('id', _id)
    //                 .attr('value', choice.name)
    //                 .attr('checked', index === this._selected ? 'checked' : undefined);
    //             var label = jQuery('<label>')
    //                 .attr('for', _id)
    //                 .html(choice.displayname);

    //             fieldset.append(input, label);
    //         }.bind(this));

    //         return fieldcontain.append(fieldset);
    //     },

    //     _setupFieldset: function() {
    //         return jQuery('<fieldset>')
    //             .attr('data-role', 'controlgroup')
    //             .append(jQuery('<legend>').html(this.displayname()));
    //     }
    // });

    // /*
    //  *  Text Property
    //  */
    // var Text = Property.extend({
    //     init: function(options, node) {
    //         // option sanitization for general text fields
    //         options = jQuery.extend({}, Config.Properties.Defaults.Text, options);

    //         // enrich with additional features when we it is a number field
    //         if (options.type === 'number') {
    //             options = jQuery.extend({}, Config.Properties.Defaults.Number, options);
    //         } else {
    //             options.type = 'text';
    //         }

    //         this._super(options, node);

    //         this._input = this._element.find('input');
    //         this._setupMirror();
    //     },

    //     value: function() {
    //         return this._input.val();
    //     },

    //     _afterAppend: function() {
    //         this._element.fieldcontain();
    //         this._input.textinput();
    //     },

    //     _callbackElement: function() {
    //         return this._input;
    //     },

    //     _change: function(eventObject) {
    //         if (this._options.type === 'number') {
    //             var n = parseFloat(this.value());
    //             if (isNaN(n)) {
    //                 n = this._options.min;
    //             }
    //             this._input.val(Math.max(this._options.min, Math.min(n, this._options.max)));
    //         }

    //         if (this._mirror) this._mirror.html(this._mirrorString());
    //         this._sendChange();
    //     },

    //     _keyup: function(eventObject) {
    //         if (this._mirror) {
    //             this._mirror.html(this._mirrorString());
    //         }
    //         this._sendChange();
    //     },

    //     _setupElement: function() {
    //         var fieldcontain = this._setupFieldcontain();
    //         var label        = this._setupLabel();
    //         var input        = jQuery('<input type="' + this._options.type + '">')
    //             .attr('data-mini', 'true')
    //             .attr('id',        this._id)
    //             .attr('min',       this._options.min)
    //             .attr('max',       this._options.max)
    //             .attr('step',      this._options.step)
    //             .attr('disabled',  this._options.disabled)
    //             .attr('pattern',   this._options.pattern)
    //             .val(this._options.value)
    //             .addClass(Config.Classes.PROPERTY_TEXT);

    //         return fieldcontain
    //             .append(label)
    //             .append(input);
    //     }
    // });
    // 
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
            
            var visual    = this._setupVisual();
            this.input    = visual.input;
            this.visual   = visual.visual;

            this._mirror();
        },

        hide: function() {
            this.visual.remove();

            return this;
        },

        show: function(container) {
            container.append(this.visual);
            this._setupCallbacks();

            return this;
        },

        _mirror: function() {
            if (typeof this.mirror !== 'undefined') {
                this.mirror.show(this.input.val());
            }
        },

        _sendChange: function() {
            if (this.name) {
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
            this._value(this.input.attr('checked') ? true : false);
            this._sendChange();
        },

        _setupInput: function() {
            var input = jQuery('<input type="checkbox">')
                .attr('id', this.id)
                .attr('disabled', this.disabled ? 'disabled' : undefined)
                .attr('checked', this._value() ? 'checked' : undefined);

            return input;
        }
    });

    var Compound = Property.extend({
        init: function(node, mirror, propertyDefinition) {

            this._super(node, mirror, propertyDefinition);
        },

        _setupInput: function() {

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
            this._value(this.input.val());
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
            this._value([lower, upper]);
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

        _mirror: function() {
            if (typeof this.mirror !== 'undefined') {
                this.mirror.show(this._lower.val() + '-' + this._upper.val());
            }
        },

        _sendChange: function() {
            if (this.name) {
                properties = {};
                properties[this.property] = '' + this._value();

                Backend.changeNode(this.node, properties);
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
            var group      = this._setupControlGroup();
            var inlineForm = this._setupInput();
            var inputs     = inlineForm.children('input');

            this._lower = inputs.eq(0);
            this._upper = inputs.eq(1);

            group.children('.controls').append(inlineForm);

            return {
                visual: group,
                input:  inputs
            };
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
            this._value(this.input.val());
            this._mirror();
            this._sendChange();
        },

        _setupInput: function() {
            var value    = this._value();
            var select   = jQuery('<select>');
            var selected = typeof value !== 'undefined' ? value : this.choices[0];

            // is the selected value no part of the available choices? add it to them!
            if (_.indexOf(this.choices, selected) < 0) this.choices.unshift(value);

            // model each choice as an option of the select
            _.each(this.choices, function(choice) {
                jQuery('<option>')
                    .html(choice)
                    .attr('value', choice)
                    .attr('selected', choice === selected ? 'selected', undefined)
                    .appendTo(select);
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
            this._value(this.input.val());
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

        if (kind === 'number') {
            return new Number(node, mirror, propertyDefinition);
        } else if (kind === 'checkbox') {
            return new Checkbox(node, mirror, propertyDefinition);
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