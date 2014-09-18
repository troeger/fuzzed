define(['factory', 'class', 'config', 'jquery'], function(Factory, Class, Config) {
    /**
     * Package: Base
     */

    /**
     * Constants:
     *      {RegEx} NUMBER_REGEX - RegEx for matching all kind of number representations with strings.
     */
    var NUMBER_REGEX = /^[+\-]?(?:0|[1-9]\d*)(?:[.,]\d*)?(?:[eE][+\-]?\d+)?$/;

    /**
     * Function: capitalize
     *      Helper function for capitalizing the first letter of a string.
     *
     * Returns:
     *      {String} capitalized - Capitalized copy of the string.
     */
    var capitalize = function(aString) {
        return aString.charAt(0).toUpperCase() + aString.slice(1);
    };

    /**
     * Function: escape
     *      HTML escapes the provided text to only contain break tags instead of linebreaks.
     *
     * Returns:
     *      {String} escaped - The HTML escaped version of the string.
     */
	var escape = function(aString) {
		return _.escape(aString).replace(/\n/g, '<br>');
	};
	
    /**
     * Abstract Class: Entry
     *      Abstract base class for an entry in the property menu of a node. It's associated with a <Property> object
     *      and handles the synchronization with it.
     */
    var Entry = Class.extend({
        /**
         * Group: Members
         *      {String}     id            - Form element ID for value retrieval.
         *      {<Property>} property      - The associated <Property> object.
         *      {DOMElement} container     - The container element in the property dialog.
         *      {DOMElement} inputs        - A selector containing all relevant form elements.
         *
         *      {Boolean}    _editing      - A flag that marks this entry as currently beeing edited.
         *      {Object}     _preEditValue - The last valid value stored before editing this entry.
         *      {DOMElement} _editTarget   - A selector containing the one form element that is being edited.
         *      {Timeout}    _timer        - The Timeout object used to prevent updates from firing immediately.
         */
        id:            undefined,
        property:      undefined,
        container:     undefined,
        inputs:        undefined,

        _editing:      false,
        _preEditValue: undefined,
        _editTarget:   undefined,
        _timer:        undefined,

        /**
         * Constructor: init
         *      Initializes the menu entry. Sets up the node's visual representation, event handler and state during the
         *      process.
         *
         *  Parameters:
         *      {<Property>} property - The associated <Property> object.
         */
        init: function(property) {
            this.id       = _.uniqueId('property');
            this.property = property;

            this._setupVisualRepresentation()
                ._setupEvents();
        },

        /**
         * Section: Event Handling
         */

        /**
         * Method: blurEvents
         *      States the blur (think: 'stop editing') events this Entry should react on.
         *
         * Returns:
         *      {Array[String]} - Array of blury events.
         */
        blurEvents: function() {
            return ['blur', 'remove'];
        },

        /**
         * Method: blurred
         *      Callback method that gets fired when one of the blur events specified in <blurEvents> was fired. Takes
         *      care of validation and propagating the new value of the Entry to the associated <Property>. If the new
         *      value is not valid for the property, its old value will be restored.
         *
         * Parameters:
         *      See jQuery event callbacks.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        blurred: function(event, ui) {
            if (!this._editing) {
                this._preEditValue = this.property.value;
            }

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

        /**
         * Method: changeEvents
         *      Return the change ('currently editing') events this Entry should react on.
         *
         *  Returns:
         *      {Array[String]} - Array of change event names.
         */
        changeEvents: function() {
            return [];
        },

        /**
         * Method: changed
         *      Callback method that gets fired when one of the change events specified in <changeEvents> was fired.
         *      Takes care of validation and propagating the new value of the Entry to the associated <Property>. If the
         *      new value is not valid it will display an appropriate error message.  Valid values will be propagated to
         *      the <Property> after a short timeout to prevent propagation while changing the value too often.
         *
         * Parameters:
         *      See jQuery event callbacks.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
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

        /**
         * Method: _abortChange
         *      Abort the currently running value propagation timeout to prevent the propagation of the value to the
         *      <Property>.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _abortChange: function() {
            window.clearTimeout(this._timer);

            return this;
        },

        /**
         * Method: _sendChange
         *      Propagate the currently set value to the <Property> object after a short timeout (to prevent in-to-deep-
         *      propagation). If there is already a timeout running it will cancel that timeout and start a new one.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _sendChange: function() {
            // discard old timeout
            window.clearTimeout(this._timer);
            var value = this._value();
            // create a new one
            this._timer = window.setTimeout(function() {
                this.property.setValue(value, this);
            }.bind(this), Factory.getModule('Config').Menus.PROPERTIES_MENU_TIMEOUT);

            return this;
        },

        /**
         *  Section: Validation
         */

        /**
         * Method: fix
         *      This method allows for "fixing" the value in the menu entries visual input before passing it to the
         *      properties validate method. This allows for example neat user interface convenience features like
         *      raising the upper boundary of an interval input when the lower boundary gets larger.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        fix: function(event, ui) {
            return this;
        },

        /**
         *  Section: Visuals
         */

        /**
         * Method: appendTo
         *      Adds this Entry to the container in the properties menu.
         *
         * Parameters:
         *      {jQuery Selector} on - The element this Entry should be appended to.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        appendTo: function(on) {
            on.append(this.container);
            this._setupCallbacks();

            return this;
        },

        /**
         * Method: insertAfter
         *      Adds this Entry after another element to the properties menu.
         *
         * Parameters:
         *      {jQuery Selector} element - The element this Entry should be inserted after.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        insertAfter: function(element) {
            element.after(this.container);
            this._setupCallbacks();

            return this;
        },

        /**
         * Method: remove
         *      Removes this Entry to the container in the properties menu.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        remove: function() {
            this.container.remove();

            return this;
        },

        /**
         * Method: setReadonly
         *      Marks the menu entry as readonly. Cannot be modified but any longer. However, visualization and copying
         *      of the value is still legal.
         *
         * Parameters:
         *      {Boolean} readonly - The new readonly state to set for this entry.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        setReadonly: function(readonly) {
            this.inputs
                .attr('readonly', readonly ? 'readonly' : null)
                .toggleClass('disabled', readonly);

            return this;
        },

        /**
         * Method: setHidden
         *      Sets the hidden state of this menu entry. Hidden entries do not appear in the property menu.
         *
         * Parameters:
         *      {Boolean} hidden - The new hidden state to set for this entry.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        setHidden: function(hidden) {
            this.container.toggle(!hidden);

            return this;
        },

        /**
         * Method: warn
         *      Highlight the corresponding form elements (error state) and show a popup containing an error message.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        warn: function(text) {
            if (this.container.hasClass(Factory.getModule('Config').Classes.PROPERTY_WARNING) &&
                this.container.attr('data-original-title') === text)
                return this;

            this.container
                .addClass(Factory.getModule('Config').Classes.PROPERTY_WARNING)
                .attr('data-original-title', text)
                .tooltip('show');

            return this;
        },

        /**
         * Method: unwarn
         *      Restores the normal state of all form elements and hides warning popups.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        unwarn: function() {
            this.container.removeClass(Factory.getModule('Config').Classes.PROPERTY_WARNING).tooltip('hide');

            return this;
        },

        /**
         *  Section: Setup
         */

        /**
         * Method: _setupVisualRepresentation
         *      Sets up all visuals (container and inputs).
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();
            this.container.find('.inputs').prepend(this.inputs);

            this.setReadonly(this.property.readonly);
            this.setHidden(this.property.hidden);

            return this;
        },

        /**
         * Method: _setupContainer
         *      Sets up the container element.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _setupContainer: function() {
            this.container = jQuery(
                '<div class="form-group" data-toggle="tooltip" data-trigger="manual" data-placement="left">\
                    <label class="col-4 control-label" for="' + this.id + '">' + (this.property.displayName || '') + '</label>\
                    <div class="inputs col-8"></div>\
                </div>'
            );

            return this;
        },

        /**
         *  Abstract Method: _setupInput
         *      Sets up all needed input (form) elements. Could be e.g. a text input, checkbox, ... Must be implemented
         *      by a subclass.
         */
        _setupInput: function() {
            throw SubclassResponsibility();
        },

        /**
         * Method: _setupCallbacks
         *      Sets up the callbacks for change and blur events on input elements.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _setupCallbacks: function() {
            _.each(this.blurEvents(), function(event) {
                this.inputs.on(event, this.blurred.bind(this));
            }.bind(this));

            _.each(this.changeEvents(), function(event) {
                this.inputs.on(event, this.changed.bind(this));
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupEvents
         *      Register for changes of the associated <Property> object.
         *
         * Returns:
         *      This {Entry} for chaining.
         */
        _setupEvents: function() {
            jQuery(this.property).on([
                Factory.getModule('Config').Events.NODE_PROPERTY_CHANGED,
                Factory.getModule('Config').Events.EDGE_PROPERTY_CHANGED,
                Factory.getModule('Config').Events.NODEGROUP_PROPERTY_CHANGED
            ].join(' '), function(event, newValue, text, issuer) {
                // ignore changes issued by us in order to prevent race conditions with the user
                if (issuer === this) return;
                this._value(newValue);
            }.bind(this));


            jQuery(this.property).on(Factory.getModule('Config').Events.PROPERTY_READONLY_CHANGED, function(event, newReadonly) {
                this.setReadonly(newReadonly);
            }.bind(this));

            jQuery(this.property).on(Factory.getModule('Config').Events.PROPERTY_HIDDEN_CHANGED, function(event, newHidden) {
                this.setHidden(newHidden);
            }.bind(this));

            return this;
        },

        /**
         *  Section: Accessors
         */

        /**
         * Method: _value
         *      Method used for retrieving the current property value from the inputs.
         */
        _value: function(newValue) {
            throw SubclassResponsibility();
        }
    });

    /**
     * Class: BoolEntry
     *      Concrete <Entry> implementation that represents a bool property. Visual representation used is a checkbox.
     */
    var BoolEntry = Entry.extend({
        /**
         * Method: blurEvents
         *      Override, checkboxes do not fire blur events.
         *
         * Returns:
         *      {Array[String]} - List of change event names.
         */
        blurEvents: function() { return ['change']; },

        /**
         * Method: setReadonly
         *      Override due to the fact that checkbox require different HTML attribute to be set.
         *
         * Returns:
         *      This {BoolEntry} for chaining.
         */
        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        /**
         * Method: _setupInput
         *      Concrete implementation of the method. Returns HTML markup for a checkbox.
         *
         * Returns:
         *      This {BoolEntry} for chaining.
         */
        _setupInput: function() {
            this.inputs = jQuery('<input type="checkbox">')
                .attr('id', this.id);

            return this;
        },

        /**
         * Method: _value
         *      Concrete implementation of _value. Returns the checked attribute state of the checkbox as value.
         *
         * Returns:
         *      {BoolEntry} this    - For chaining when used as setter.
         *      {Boolean}   checked - The entries value when used as a getter.
         *
         */
        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.is(':checked');
            this.inputs.attr('checked', newValue ? 'checked' : null);

            return this;
        }
    });

    /**
     * Class: ChoiceEntry
     *      An Entry allowing to select a value from a list of values defined by a <Property::Choice>. Visualized by an
     *      HTML select element.
     */
    var ChoiceEntry = Entry.extend({
        /**
         * Method: blurEvents
         *      Overrides standard collection of blur events. Additionally contains the change event that is specific
         *      for select elements
         *
         * Returns:
         *      {Array[String]} changeEvents - The blur events.
         */
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        /**
         * Method: setReadonly
         *      Overrides standard readonly setter. Select elements need to set the HTML disabled attribute in order to
         *      be readonly. Setting the readonly attribute is not sufficient.
         *
         * Parameters:
         *      {Boolean} readonly - the readonly state as boolean.
         *
         * Returns:
         *      This {ChoiceEntry} for chaining.
         */
        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        /**
         * Method: _setupInput
         *      The choice input element is represented by an HTML select element. This method constructs it and stores
         *      it in the _input member. The preselected option of the select is either given in the notation as default
         *      value or is none.
         *
         * Returns:
         *      This {ChoiceEntry} for chaining.
         */
        _setupInput: function() {
            var value    = this.property.value;
            this.inputs  = jQuery('<select class="form-control input-small">').attr('id', this.id);

            var selected = this.property.choices[this._indexForValue(value)];

            _.each(this.property.choices, function(choice, index) {
                this.inputs.append(jQuery('<option>')
                    .text(choice)
                    .val(index)
                    .attr('selected', choice === selected ? 'selected' : null)
                )
            }.bind(this));

            return this;
        },

        /**
         * Method: _indexForValue
         *      Reverse search of a index belonging to a given value.
         *
         * Parameters:
         *      {Object} value - The value of an entry.
         *
         * Returns:
         *      The {Number} index of the given value. -1 if the lookup failed.
         */
        _indexForValue: function(value) {
            for (var i = this.property.values.length -1; i >= 0; i--) {
                if (_.isEqual(this.property.values[i], value)) {
                    return i;
                }
            }

            return -1;
        },

        /**
         * Method: _value
         *      Concrete implementation of the _value method. Returns the value of the currently selected option of the
         *      select element if the method's parameter is unset. Otherwise the passed will be set. The lookup of the
         *      value is done as in <_indexForValue>.
         *
         * Parameters:
         *      {String} newValue - [optional] optional new value of the choice entry.
         *
         * Returns:
         *      This {ChoiceEntry} for chaining.
         */
        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                return this.property.values[this.inputs.val()];
            }
            this.inputs.val(this._indexForValue(newValue));

            return this;
        }
    });

    /**
     *  Class: CompoundEntry
     *      A container entry containing multiple other Entries. This is the graphical equivalent to a <Compound>
     *      <Property>. The active child Property can be chosen with radio buttons. The CompoundEntry ensures the
     *      consistency of updates with the backend.
     */
    var CompoundEntry = Entry.extend({
        blurEvents: function() {
            return ['click'];
        },

        appendTo: function(on) {
            this._super(on);
            _.each(this.property.parts, function(part, index) {
                part.menuEntry.insertAfter(this.container);
                // child entries should not update on remove because only visible entries should be allowed
                // to propagate their value which is ensured by the parent compound (on remove)
                part.menuEntry.inputs.off('remove');
                part.menuEntry.setHidden(this.property.value !== index);
            }.bind(this));

            return this;
        },

        remove: function() {
            _.each(this.property.parts, function(part, index) {
                part.menuEntry.remove();
            });

            return this._super();
        },

        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        _setupInput: function() {
            this.inputs = jQuery('<div class="btn-group" data-toggle="buttons">');

            _.each(this.property.parts, function(part, index) {
                var buttonLabel = jQuery('<label class="btn btn-default btn-small"></label>')
                var button = jQuery('<input type="radio">');
                buttonLabel.text(part.partName);
                button.attr('active', index === this.property.value ? 'active' : '');
                buttonLabel.append(button);
                this.inputs.append(buttonLabel);
            }.bind(this));
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                return this.inputs.find('.active').index();
            }

            this.inputs.find('.btn:nth-child(' + (newValue + 1) + ')').button('toggle');
            this._showPartAtIndex(newValue);
        },

        fix: function(event, ui) {
            // we try to read the button state before bootstraps event handling is finished, so we
            // force bootstrap to manually toggle the button state before we read it
            jQuery(event.target).button('toggle');
        },

        /**
         *  Method: _showPartAtIndex
         *      Make the child Entry with the given index visible and hide all others.
         *
         *  Parameters:
         *      {Integer} index - The index of the child Entry that should be displayed.
         *
         *  Returns:
         *      This Entry instance for chaining.
         */
        _showPartAtIndex: function(index) {
            _.each(this.property.parts, function(part, iterIndex) {
                part.setHidden(iterIndex !== index);
            });

            return this;
        }
    });

    /**
     * Class: NumericEntry
     *      Input field for a <Property::Numeric>. It ensures that only number-typed values are allowed and provides
     *      convenience functions like stepping with spinners. It is concrete implementation of <PropertyMenuEntry>.
     */
    var NumericEntry = Entry.extend({
        /**
         * Method: blurEvents
         *      Overrides the standard list of blur events. Additionally contains change in order to support HTML 5
         *      spinners.
         *
         * Returns:
         *      {Array[String]} blurEvents - The blur events.
         */
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        /**
         * Method: changeEvents
         *      Overrides the standard list of change events. Number input fields behave like normal text fields and
         *      therefore need to support changes on key presses, cuts and pasts.
         *
         * Returns:
         *      {Array[String]} changeEvent - the change events.
         */
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        /**
         * Method: _setupInput
         *      Concrete implementation of the _setupInput method. Returns a HTML 5 number input field. The method sets
         *      the respective attributes for min/max/step of the number field. If a browser does not support HTML 5 it
         *      will be interpreted as a text input instead.
         *
         * Returns:
         *      This {NumberEntry} for chaining.
         */
        _setupInput: function() {
            this.inputs = jQuery('<input type="number" class="form-control input-small">')
                .attr('id',   this.id)
                .attr('min',  this.property.min)
                .attr('max',  this.property.max)
                .attr('step', this.property.step);

            return this;
        },

        /**
         * Method: _value
         *      Concrete implementation of this method. Functions as getter and setter. If no new value is set, the
         *      current number of the entry is returned. Elsewise, the value is set unchecked.
         *
         * Parameters:
         *      {Number} newValue - [optional] if set the new value of the number entry.
         *
         * Returns:
         *      This {NumberEntry} for chaining.
         */
        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                var val = this.inputs.val();
                if (!NUMBER_REGEX.test(val)) return window.NaN;
                return window.parseFloat(val);
            }
            this.inputs.val(newValue);

            return this;
        }
    });

    /**
     * Class: RangeEntry
     *      Entry for modifying values of a <Property::Range> consisting of two numbers inputs that bound the number
     *      range. This class is a concrete implementation of an <Entry>.
     */
    var RangeEntry = Entry.extend({
        /**
         * Method: blurEvents
         *      Overrides the default blur events. Since range entries consist of two number entries we need the exact
         *      same blur events here - meaning change is added due to HTML 5.
         *
         * Returns:
         *      {Array[String]} blurEvents - the blur events.
         */
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        /**
         * Method: changeEvents
         *      Overrides the default change events. Same goes here as in blur events. We need the number input events
         *      here additionally. Therefore, keyup, cut and paste are added.
         *
         * Returns:
         *      {Array[String]} change Events - the change events.
         */
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        /**
         * Method: fix
         *      Override of the empty default fix implementation. The behaviour here implements a usability convenience
         *      feature. Given that both inputs contain numbers, the value of the not modified value is always adjusted
         *      in a way that the two number frame a legal range, with the left value being the lower and right value to
         *      be the upper bound. Example: The left value contains the number 12 and the right as well. Now, the left
         *      value is increased by one. The value range is not legal anymore, being [13, 12]. So the right value is
         *      automatically adjusted to [13, 13].
         *
         * Parameters:
         *      {Event}      event - jQuery event object (see their documentation for specifics)
         *      {DOMElement} ui    - jQuery DOM element set that refer to the event handling element.
         *
         * Returns:
         *      This {RangeEntry} for chaining.
         */
        fix: function(event, ui) {
            var val = this._value();
            var lower = val[0];
            var upper = val[1];

            if (_.isNaN(lower) || _.isNaN(upper)) return this;

            var inputs = this.inputs.filter('input');

            var target = jQuery(event.target);
            if (target.is(inputs.eq(0)) && lower > upper) {
                this._value([lower, lower]);
            } else if (target.is(inputs.eq(1)) && upper < lower) {
                this._value([upper, upper]);
            }

            return this;
        },

        /**
         * Method: _setupVisualRepresentation
         *      Overrides the standard setup for visual representation container. The two number fields need a wrapping
         *      inline container.
         *
         * Returns:
         *      This {RangeEntry} for chaining.
         */
        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();

            jQuery('<form class="form-inline">')
                .append(this.inputs)
                .appendTo(this.container.find('.inputs'));

            this.setReadonly(this.property.readonly);
            this.setHidden(this.property.hidden);

            return this;
        },

        /**
         * Method:_setupInput
         *      Creates two numeric input fields as inline form fields as input. Also renders statically a small hyphen
         *      between them.
         *
         * Returns:
         *      This {RangeEntry} for chaining.
         */
        _setupInput: function() {
            var value = this.property.value;
            var min   = this.property.min;
            var max   = this.property.max;
            var step  = this.property.step;

            this.inputs = this._setupMiniNumeric(min, max, step, value[0]).css('width', '45%')
                .attr('id', this.id) // clicking the label should focus the first input
                .add(jQuery('<label> – </label>').css('width', '10%').css('text-align', 'center'))
                .add(this._setupMiniNumeric(min, max, step, value[1]).css('width', '45%'));

            return this;
        },

        /**
         * Method: _setupMiniNumeric
         *      Constructs and returns a number field with the given attributes.
         *
         * Parameters:
         *      {Number} min   - The minimum number that should be allowed.
         *      {Number} max   - The maximum number that should be allowed.
         *      {Number} step  - The step width the value should fit in.
         *      {Number} value - The currently set value.
         *
         *  Returns:
         *      The newly constructed mini number input {DOMElement}.
         */
        _setupMiniNumeric: function(min, max, step, value) {
            return jQuery('<input type="number" class="form-control input-small">')
                .attr('min',  this.property.min)
                .attr('max',  this.property.max)
                .attr('step', this.property.step)
                .val(value);
        },

        /**
         * Method: _value
         *      Concrete implementation of the _value getter/setter. If now new value is passed as parameter, the method
         *      functions as a getter and returns the current value as two-tuple/array of numbers. However, if a value
         *      is given, the method works as a setter. The value is set in the numeric input in order of the tuple.
         *
         * Parameters:
         *      {Array[Number]} newValue - [optional] the value to be set, if present.
         *
         * Returns:
         *      This {RangeEntry} for chaining.
         */
        _value: function(newValue) {
            var input = this.inputs.filter('input');
            var lower = input.eq(0);
            var upper = input.eq(1);

            if (typeof newValue === 'undefined') {
                var lowerVal = (!NUMBER_REGEX.test(lower.val()))
                    ? window.NaN : window.parseFloat(lower.val());
                var upperVal = (!NUMBER_REGEX.test(upper.val()))
                    ? window.NaN : window.parseFloat(upper.val());
                return [lowerVal, upperVal];
            }
            lower.val(newValue[0]);
            upper.val(newValue[1]);

            return this;
        }
    });

    /**
     * Class: EpsilonEntry
     *      Is a subclass of <RangeEntry> and also models an interval. However, the semantic is changed. The second
     *      number specifies an epsilon range around the first number and thereby creating the interval.
     */
    var EpsilonEntry = RangeEntry.extend({
        /**
         * Method: fix
         *      Overrides <RangeEntries> fix' method. The behaviour is altered in a manner that the epsilon range may
         *      never leave the possible minimum and maximum of the whole interval. Example: min/max of the whole
         *      interval is 0/1. You epsilon center is 0.75 and your epsilon value is 0.25. You now increase the center
         *      to 0.85, leaving the epsilon range to [0.6, 1.1]. The upper value exceeds the boundaries of the whole
         *      interval. So, the epsilon value is reduced down to 0.15, leaving its range as [0.7, 1].
         *
         * Parameters:
         *   {Event}      event - jQuery event object, refer to their documentation for specifics
         *   {DOMElement} ui    - The dom element that had the event handler registered.
         *
         * Returns:
         *      This {EpsilonEntry} for chaining.
         */
        fix: function(event, ui) {
            var val     = this._value();
            var center  = val[0];
            var epsilon = val[1];

            // early out, if one of the numbers is NaN we cannot fix anything, leave it to the property
            if (_.isNaN(center) || _.isNaN(epsilon)) return this;

            var pMin   = this.property.min;
            var pMax   = this.property.max;
            var target = jQuery(event.target);

            // early out, nothing to fix here
            if (pMin.gt(center) || pMax.lt(center) || pMax.lt(epsilon) || epsilon < 0) return this;

            var epsBounded = Math.min(Math.abs(pMin.toFloat() - center), epsilon, pMax.toFloat() - center);
            var cenBounded = Math.max(pMin.plus(epsilon), Math.min(center, pMax.minus(epsilon).toFloat()));

            if (epsilon == epsBounded && cenBounded == center) return this;

            if (target.is(this.inputs.eq(0))) {
                this._value([center, epsBounded]);
            } else if (target.is(this.inputs.eq(1))) {
                this._value([cenBounded, epsilon]);
            }

            return this;
        },

        /**
         * Method: _setupInput
         *      Overrides the parents behaviour by exchanging the label between the two input fields with a '±' sign.
         *
         * Returns:
         *      This {EpsilonEntry} for chaining.
         */
        _setupInput: function() {
            var value = this.property.value;
            var min   = this.property.min;
            var max   = this.property.max;

            this.inputs = this._setupMiniNumeric(min, max, this.property.step, value[0]).css('width', '45%')
                .attr('id', this.id) // clicking the label should focus the first input
                .add(jQuery('<label> ± </label>').css('width', '10%').css('text-align', 'center'))
                .add(this._setupMiniNumeric(0, max, this.property.epsilonStep, value[1]).css('width', '45%'));

            return this;
        }
    });

    /**
     * Class: TextEntry
     *      Simple input field for a <Property::Text> and concrete implementation of <Entry>.
     */
    var TextEntry = Entry.extend({
        /**
         * Method: changeEvents
         *      Overrides the default change events. Needs keyup, cut and paste events additionally.
         *
         * Returns:
         *      {Array[String]} changeEvents - The change events.
         */
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        /**
         * Method: _setupInput
         *      Creates the input element for a text entry - a text input box.
         *
         * Returns:
         *      This {TextEntry} for chaining.
         */
        _setupInput: function() {
            this.inputs = jQuery('<input type="text" class="form-control input-small">').attr('id', this.id);
            return this;
        },

        /**
         * Method: _value
         *      Getter/setter for the menu entry. If the optional parameter is not given, it works as a getter,
         *      returning the inputs value as string. Otherwise, sets the passed value unchecked.
         *
         * Parameters:
         *      {String} newValue - [optional] If present, the new value of the entry.
         *
         * Returns:
         *   This {TextEntry} for chaining reasons, if used as setter.
         *   The value as {String} otherwise.
         */
        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.val();
            this.inputs.val(newValue);

            return this;
        }
    });
	
	/**
	 * Class: InlineTextArea
     *      Special kind of text area property, that does NOT appear inside the properties TextArea for editing inside a
     *      shape on the canvas. So far only used for editing inside a sticky note.
	 */
    var InlineTextArea = Entry.extend({
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },
		
        blurEvents: function() {
            return ['blur'];
        },

        /**
         * Method: _setupInput
         *      Implements the input setup by producing an HTML textarea. It is initially hidden.
         *
         * Returns:
         *      This <InlineTextArea> for chaining.
         */
        _setupInput: function() {
            this.inputs = jQuery('<textarea type="text" class="form-control">').attr('id', this.id);
			//hide textarea at the beginning
			this.inputs.toggle(false);

            return this;
        },
		
        appendTo: function() {
			this._setupCallbacks();
            return this;
        },

        /**
         * Method
         * @param event
         * @param ui
         */
        blurred: function(event, ui) {
			 this._super(event, ui);
			 // hide textarea
			 this.inputs.toggle(false);
			 // show paragraph and set value
			 this.inputs.siblings('p').html(
				 escape(this.inputs.val())
			 ).toggle(true);
		},
		
        remove: function() {},
		
        _setupContainer: function() {
			this.property.owner._nodeImage.append(
				jQuery('<p align="center">').html(escape(this.property.value))
			);
			this.container = this.property.owner.container;
			
			return this;
        },
		
        _setupVisualRepresentation: function() {
            this._setupInput();
			this._setupContainer();
			this.container.find('.' + Factory.getModule('Config').Classes.EDITABLE).append(this.inputs);

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.val();
            this.inputs.val(newValue);

            return this;
        }
    });
	
    /**
     * Class: TransferEntry
     *      Allows to link to other entities in the database. Looks like a normal <ChoiceEntry>, but actually fetches
     *      the available values from the backend using Ajax.
     */
    var TransferEntry = Entry.extend({
        _progressIndicator: undefined,
        _openButton: undefined,
        _unlinked: undefined,

        init: function(property) {
            this._super(property);

            jQuery(window).on('focus', this._refetchEntries.bind(this));
            jQuery(this.property).on(Factory.getModule('Config').Events.PROPERTY_SYNCHRONIZED, this._refreshEntries.bind(this));
        },

        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        fix: function(event, ui) {
            if (this._value() !== this.property.UNLINK_VALUE) {
                this._unlinked.remove();
            }

            return this;
        },

        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        _setupInput: function() {
            this.inputs = jQuery('<select class="form-control input-small">')
                .attr('id', this.id)
                .css('display', 'none');

            // add placeholder entry
            this._unlinked = jQuery('<option>')
                .text(this.property.UNLINK_TEXT)
                .attr('selected', 'selected')
                .attr('value', this.property.UNLINK_VALUE);

            this._openButton = jQuery('<button type="button">')
                .addClass('btn btn-default btn-small col-12')
                .addClass(Factory.getModule('Config').Classes.PROPERTY_OPEN_BUTTON)
                .text('Open in new tab')
                .appendTo(this.container.children('.inputs'))
                .css('display', 'none');

            return this._setupProgressIndicator();
        },

        /**
         *  Method: _setupOptions
         *      Reconstructs the HTML option elements from the list of transfer graphs. It will also select
         *      the currently active value or reset to default if the current value is no longer available.
         *
         *  Returns:
         *      This {<TransferEntry>} instance for chaining.
         */
        _setupOptions: function() {
            // remove old values
            this.inputs.empty();

            var found = false;

            _.each(this.property.transferGraphs, function(graphName, graphID) {
                var optionSelected = this.property.value == graphID;

                this.inputs.append(jQuery('<option>')
                    .text(graphName)
                    .attr('value', graphID)
                    .attr('selected', optionSelected ? 'selected': null)
                );
                found |= optionSelected;
            }.bind(this));

            // if the value was not found we need to reset to the default 'unlinked' value
            if (!found) {
                this.inputs.prepend(this._unlinked.attr('selected', 'selected'));
                this.property.setValue(this.property.UNLINK_VALUE);
            }

            return this;
        },

        _setupCallbacks: function() {
            this._openButton.click(function() {
                var value = this._value();

                if (value != this.property.UNLINK_VALUE) {
                    window.open(Factory.getModule('Config').Backend.EDITOR_URL + '/' + value, '_blank');
                }
            }.bind(this));

            return this._super();
        },

        /**
         *  Method: _setupProgressIndicator
         *      Constructs the progress indicator that is displayed as long as the list is fetched with AJAX.
         *
         *  Returns:
         *      This {<TransferEntry>} instance for chaining.
         */
        _setupProgressIndicator: function() {
            this._progressIndicator = jQuery('<div class="progress progress-striped active">\
                <div class="bar" style="width: 100%;"></div>\
            </div>').appendTo(this.container.children('.inputs'));

            return this;
        },

        /**
         *  Method: _refetchEntries
         *      Triggers a refetch of the available list values from the backend and displays the progress indicator.
         *
         *  Returns:
         *      This {<TransferEntry>} instance for chaining.
         */
        _refetchEntries: function() {
            this.property.fetchTransferGraphs();
            this._progressIndicator.css('display', '');
            this._openButton.css('display', 'none');
            this.inputs.css('display', 'none');

            return this;
        },

        /**
         *  Method: _refreshEntries
         *      Reconstructs the select list and hides the progress indicator.
         *
         *  Returns:
         *      This {<TransferEntry>} instance for chaining.
         */
        _refreshEntries: function() {
            this._setupOptions();
            this._progressIndicator.css('display', 'none');
            this._openButton.css('display', '');
            this.inputs.css('display', '');

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                return window.parseInt(this.inputs.val());
            }
            this.inputs.val(newValue);

            return this;
        }
    });

    return {
        'BoolEntry':     	BoolEntry,
        'ChoiceEntry':   	ChoiceEntry,
        'CompoundEntry': 	CompoundEntry,
        'EpsilonEntry':  	EpsilonEntry,
        'NumericEntry':  	NumericEntry,
        'RangeEntry':    	RangeEntry,
        'TextEntry':     	TextEntry,
		'InlineTextArea':   InlineTextArea, 
        'TransferEntry': 	TransferEntry,
    }
});
