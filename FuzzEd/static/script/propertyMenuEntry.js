define(['class', 'config'], function(Class, Config) {

    /**
     *  Package: Base
     */

    /**
     *  Constants:
     *      {RegEx} NUMBER_REGEX     - RegEx for matching all kind of number representations with strings.
     *      {RegEx} ERROR_TYPE_REGEX - RegEx for filtering out the '[...ERROR]' part of a warning message.
     */
    var NUMBER_REGEX     = /^[+\-]?(?:0|[1-9]\d*)(?:[.,]\d*)?(?:[eE][+\-]?\d+)?$/;
    var ERROR_TYPE_REGEX = /^\[.+\]\s*(.+)/;

    /**
     *  Function: capitalize
     *      Helper function for capitalizing the first letter of a string.
     */
    var capitalize = function(aString) {
        return aString.charAt(0).toUpperCase() + aString.slice(1);
    };

    /**
     *  Class: Entry
     *      Abstract base class for an entry in the property menu of a node. It's associated with a <Property> object
     *      and handles the synchronization with it.
     */
    var Entry = Class.extend({

        /**
         *  Group: Members
         *
         *  Properties:
         *      {String} id                   - Form element ID for value retrieval.
         *      {<Property>} property         - The associated <Property> object.
         *      {jQuery Selector} container   - The container element in the property dialog.
         *      {jQuery Selector} inputs      - A selector containing all relevant form elements.
         *      {boolean} _editing            - A flag that marks this entry as currently beeing edited.
         *      {Object} _preEditValue        - The last valid value stored before editing this entry.
         *      {jQuery Selector} _editTarget - A selector containing the one form element that is currently being edited.
         *      {Timeout} _timer              - The Timeout object used to prevent updates from firing immediately.
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
         *  Constructor: init
         *      Entry initialization.
         *
         *  Parameters:
         *      {<Property>} property - The associated <Property> object.
         */
        init: function(property) {
            this.id = _.uniqueId('property');
            this.property = property;

            this._setupVisualRepresentation()
                ._setupEvents();
        },

        /**
         *  Section: Event Handling
         */

        /**
         *  Method: blurEvents
         *      Return the blur ('stop editing') events this Entry should react on.
         *
         *  Returns:
         *      An array of event names.
         */
        blurEvents: function() {
            return ['blur', 'remove'];
        },

        /**
         *  Method: blurred
         *      Callback method that gets fired when one of the blur events specified in <blurEvents> was fired.
         *      Cares about validation and propagating the new value of the Entry to the associated <Property>.
         *      If the new value is not valid it will restore the old (valid) value.
         *
         *  Parameters:
         *      See jQuery event handling.
         *
         *  Returns:
         *      This Entry for chaining.
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
         *  Method: changeEvents
         *      Return the change ('currently editing') events this Entry should react on.
         *
         *  Returns:
         *      An array of event names.
         */
        changeEvents: function() {
            return [];
        },

        /**
         *  Method: changed
         *      Callback method that gets fired when one of the change events specified in <changeEvents> was fired.
         *      Cares about validation and propagating the new value of the Entry to the associated <Property>.
         *      If the new value is not valid it will display an appropriate error message.
         *      Valid values will be propagated to the <Property> after a short timeout to prevent propagation
         *      while changing the value too often.
         *
         *  Parameters:
         *      See jQuery event handling.
         *
         *  Returns:
         *      This Entry for chaining.
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
         *  Method: _abortChange
         *      Abort the currently running value propagation timeout to prevent the propagation of the value to
         *      the <Property>.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _abortChange: function() {
            window.clearTimeout(this._timer);

            return this;
        },

        /**
         *  Method: _sendChange
         *      Propagate the currently set value to the <Property> object after a short timeout
         *      (to prevent over-propagation). If there is already a timeout running it will cancel that timeout
         *      and start a new one.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _sendChange: function() {
            // discard old timeout
            window.clearTimeout(this._timer);
            // create a new one
            this._timer = window.setTimeout(function() {
                this.property.setValue(this._value(), this);
            }.bind(this), Config.Menus.PROPERTIES_MENU_TIMEOUT);

            return this;
        },


        /**
         *  Section: Validation
         */

        /**
         *  Method: fix
         *      Fix the currently set value to a value that is allowed for this Entry.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        fix: function(event, ui) {
            return this;
        },


        /**
         *  Section: Visuals
         */

        /**
         *  Method: show
         *      Adds this Entry to the container in the properties menu.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        show: function(on) {
            on.append(this.container);
            this._setupCallbacks();

            return this;
        },

        /**
         *  Method: hide
         *      Removes this Entry to the container in the properties menu.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        hide: function() {
            this.container.remove();

            return this;
        },

        setReadonly: function(readonly) {
            this.inputs
                .attr('readonly', readonly ? 'readonly' : null)
                .toggleClass('disabled', readonly);
        },

        /**
         *  Method: warn
         *      Highlight the corresponding form elements (error state) and show a popup containing an error message.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        warn: function(text) {
            text = capitalize(ERROR_TYPE_REGEX.exec(text)[1]);

            if (this.container.hasClass(Config.Classes.PROPERTY_WARNING) &&
                this.container.attr('data-original-title') === text)
                return this;

            this.container
                .addClass(Config.Classes.PROPERTY_WARNING)
                .attr('data-original-title', text)
                .tooltip('show');

            return this;
        },

        /**
         *  Method: unwarn
         *      Restores normal state of all form elements and hides warning popups.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        unwarn: function() {
            this.container.removeClass(Config.Classes.PROPERTY_WARNING).tooltip('hide');

            return this;
        },


        /**
         *  Section: Setup
         */

        /**
         *  Method: _setupVisualRepresentation
         *      Setup all visuals (container and inputs).
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();
            this.container.find('.controls').prepend(this.inputs);

            this.setReadonly(this.property.readonly);

            return this;
        },

        /**
         *  Method: _setupContainer
         *      Setup the container element.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _setupContainer: function() {
            this.container = jQuery(
                '<div class="control-group" data-toggle="tooltip" data-trigger="manual" data-placement="left">\
                    <label class="control-label" for="' + this.id + '">' + (this.property.displayName || '') + '</label>\
                    <div class="controls"></div>\
                </div>'
            );

            return this;
        },

        /**
         *  Method: _setupInput
         *      Setup all needed input (form) elements.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _setupInput: function() {
            throw '[ABSTRACT] subclass responsibility';
        },

        /**
         *  Method: _setupCallbacks
         *      Setup the callbacks for change and blur events on input elements.
         *
         *  Returns:
         *      This Entry for chaining.
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
         *  Method: _setupEvents
         *      Register for changes of the associated <Property> object.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        _setupEvents: function() {
            jQuery(this.property).on(Config.Events.PROPERTY_CHANGED, function(event, newValue, text, issuer) {
                // ignore changes issued by us in order to prevent race conditions with the user
                if (issuer === this) return;
                this._value(newValue);
            }.bind(this));

            jQuery(this.property).on(Config.Events.PROPERTY_READONLY_CHANGED, function(event, newReadonly) {
                this.setReadonly(newReadonly);
            }.bind(this));

            return this;
        },

        /**
         *  Section: Accessors
         */

        /**
         *  Method: _value
         *      Method used for retrieving the current property value from the inputs.
         *
         *  Returns:
         *      The currently set value.
         */
        _value: function(newValue) {
            throw '[ABSTRACT] subclass responsibility';
        }
    });

    var BoolEntry = Entry.extend({
        blurEvents: function() { return ['change']; },

        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        _setupInput: function() {
            this.inputs = jQuery('<input type="checkbox">')
                .attr('id', this.id);

            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.attr('checked') === 'checked';
            this.inputs.attr('checked', newValue ? 'checked' : null);

            return this;
        }
    });

    var ChoiceEntry = Entry.extend({
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        setReadonly: function(readonly) {
            this.inputs.attr('disabled', readonly ? 'disabled' : null);

            return this._super(readonly);
        },

        _setupInput: function() {
            var value    = this.property.value;
            this.inputs  = jQuery('<select class="input-medium">').attr('id', this.id);

            var selected = this.property.choices[this._indexForValue(value)];

            _.each(this.property.choices, function(choice, index) {
                this.inputs.append(jQuery('<option>')
                    .text(choice)
                    .val(index)
                    .attr('selected', choice === selected ? 'selected' : null)
                )
            }.bind(this));
        },

        _indexForValue: function(value) {
            for (var i = this.property.values.length -1; i >= 0; i--) {
                if (_.isEqual(this.property.values[i], value)) {
                    return i;
                }
            }

            return -1;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') {
                return this.property.values[this.inputs.val()];
            }
            this.inputs.val(this._indexForValue(newValue));

            return this;
        }
    });

    var NumericEntry = Entry.extend({
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
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
            var min   = this.property.min;
            var max   = this.property.max;
            var step  = this.property.step;

            this.inputs = this._setupMiniNumeric(min, max, step, value[0])
                .attr('id', this.id) // clicking the label should focus the first input
                .add(this._setupMiniNumeric(min, max, step, value[1]));

            return this;
        },

        _setupMiniNumeric: function(min, max, step, value) {
            return jQuery('<input type="number" class="input-mini">')
                .attr('min',  this.property.min)
                .attr('max',  this.property.max)
                .attr('step', this.property.step)
                .val(value);
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

    var EpsilonEntry = RangeEntry.extend({

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

            if (target.is(this.inputs.eq(0))) {
                var epsBounded = Math.min(Math.abs(pMin.toFloat() - center), epsilon, pMax.toFloat() - center);
                this._value([center, epsBounded]);

            } else if (target.is(this.inputs.eq(1))) {
                var cenBounded = Math.max(pMin.plus(epsilon), Math.min(center, pMax.minus(epsilon).toFloat()));
                this._value([cenBounded, epsilon]);
            }

            return this;
        },

        _setupInput: function() {
            var value = this.property.value;
            var min   = this.property.min;
            var max   = this.property.max;

            this.inputs = this._setupMiniNumeric(min, max, this.property.step, value[0])
                .attr('id', this.id) // clicking the label should focus the first input
                .add(this._setupMiniNumeric(0, max, this.property.epsilonStep, value[1]));

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

    var TransferEntry = Entry.extend({
        _progressIndicator: undefined,
        _openButton: undefined,
        _unlinked: undefined,

        init: function(property) {
            this._super(property);

            jQuery(window).on('focus', this._refetchEntries.bind(this));
            jQuery(this.property).on(Config.Events.PROPERTY_SYNCHRONIZED, this._refreshEntries.bind(this));
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
            this.inputs = jQuery('<select class="input-medium">')
                .attr('id', this.id)
                .css('display', 'none');

            // add placeholder entry
            this._unlinked = jQuery('<option>')
                .text(this.property.UNLINK_TEXT)
                .attr('selected', 'selected')
                .attr('value', this.property.UNLINK_VALUE);

            this._openButton = jQuery('<button type="button">')
                .addClass('btn')
                .addClass('input-medium')
                .addClass(Config.Classes.PROPERTY_OPEN_BUTTON)
                .text('Open in new tab')
                .appendTo(this.container.children('.controls'))
                .css('display', 'none');

            return this._setupProgressIndicator();
        },

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
        },

        _setupCallbacks: function() {
            this._openButton.click(function() {
                var value = this._value();

                if (value != this.property.UNLINK_VALUE) {
                    window.open(Config.Backend.EDITOR_URL + '/' + value, '_blank');
                }
            }.bind(this));

            return this._super();
        },

        _setupProgressIndicator: function() {
            this._progressIndicator = jQuery('<div class="progress progress-striped active">\
                <div class="bar" style="width: 100%;"></div>\
            </div>').appendTo(this.container.children('.controls'));

            return this;
        },

        _refetchEntries: function() {
            this.property.fetchTransferGraphs();
            this._progressIndicator.css('display', '');
            this._openButton.css('display', 'none');
            this.inputs.css('display', 'none');
        },

        _refreshEntries: function() {
            this._setupOptions();
            this._progressIndicator.css('display', 'none');
            this._openButton.css('display', '');
            this.inputs.css('display', '');
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
        'BoolEntry':     BoolEntry,
        'ChoiceEntry':   ChoiceEntry,
        'EpsilonEntry':  EpsilonEntry,
        'NumericEntry':  NumericEntry,
        'RangeEntry':    RangeEntry,
        'TextEntry':     TextEntry,
        'TransferEntry': TransferEntry
    }
});
