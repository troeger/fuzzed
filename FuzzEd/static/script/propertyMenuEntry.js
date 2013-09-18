define(['class', 'config', 'jquery'], function(Class, Config) {

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
         *  Method: appendTo
         *      Adds this Entry to the container in the properties menu.
         *
         *  Parameters:
         *      {jQuery Selector} on - The element this Entry should be appended to.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        appendTo: function(on) {
            on.append(this.container);
            this._setupCallbacks();

            return this;
        },

        /**
         *  Method: insertAfter
         *      Adds this Entry after another element to the properties menu.
         *
         *  Parameters:
         *      {jQuery Selector} element - The element this Entry should be inserted after.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        insertAfter: function(element) {
            element.after(this.container);
            this._setupCallbacks();

            return this;
        },

        /**
         *  Method: remove
         *      Removes this Entry to the container in the properties menu.
         *
         *  Returns:
         *      This Entry for chaining.
         */
        remove: function() {
            this.container.remove();

            return this;
        },

        /**
         *  Method: setReadonly
         *      Set the readonly state of this menu entry. Readonly entries can not be edited but (in case of text
         *      fields) be marked and copied from.
         *
         *  Parameters:
         *      {boolean} readonly - The new readonly state to set for this entry.
         *
         *  Returns:
         *      This Entry instance for chaining.
         */
        setReadonly: function(readonly) {
            this.inputs
                .attr('readonly', readonly ? 'readonly' : null)
                .toggleClass('disabled', readonly);

            return this;
        },

        /**
         *  Method: setHidden
         *      Set the hidden state of this menu entry. Hidden entries do not appear in the menu.
         *
         *  Parameters:
         *      {boolean} hidden - The new hidden state to set for this entry.
         *
         *  Returns:
         *      This Entry instance for chaining.
         */
        setHidden: function(hidden) {
            this.container.toggle(!hidden);

            return this;
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
            this.container.find('.inputs').prepend(this.inputs);

            this.setReadonly(this.property.readonly);
            this.setHidden(this.property.hidden);

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
                '<div class="form-group" data-toggle="tooltip" data-trigger="manual" data-placement="left">\
                    <label class="col-4 control-label" for="' + this.id + '">' + (this.property.displayName || '') + '</label>\
                    <div class="inputs col-8"></div>\
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
            throw SubclassResponsibility();
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

            jQuery(this.property).on(Config.Events.PROPERTY_HIDDEN_CHANGED, function(event, newHidden) {
                this.setHidden(newHidden);
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
            throw SubclassResponsibility();
        }
    });

    /**
     *  Class: BoolEntry
     *      Simple checkbox entry that reflects a <Bool> <Property>.
     */
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
            if (typeof newValue === 'undefined') return this.inputs.is(':checked');
            this.inputs.attr('checked', newValue ? 'checked' : null);

            return this;
        }
    });

    /**
     *  Class: ChoiceEntry
     *      An Entry allowing to select a value from a list of values defined by a <Choice> <Property>.
     */
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
            this.inputs  = jQuery('<select class="form-control input-small">').attr('id', this.id);

            var selected = this.property.choices[this._indexForValue(value)];

            _.each(this.property.choices, function(choice, index) {
                this.inputs.append(jQuery('<option>')
                    .text(choice)
                    .val(index)
                    .attr('selected', choice === selected ? 'selected' : null)
                )
            }.bind(this));
        },

        /**
         *  Method: _indexForValue
         *      Reverse search of a index belonging to a given value.
         *
         *  Parameters:
         *      {Object} value - The value of an entry.
         *
         *   Returns:
         *      The index of the given value. Returns -1 in case it was not found.
         */
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

    /**
     *  Class: CompoundEntry
     *      A container entry containing multiple other Entries. This is the graphical equivalent to a <Compound>
     *      <Property>. The active child Property can be chosen with radio buttons. The CompoundEntry ensures
     *      the consistency of updates with the backend.
     */
    var CompoundEntry = Entry.extend({
        blurEvents: function() {
            return ['click', 'remove'];
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
     *  Class: NumericEntry
     *      Input field for a <Numeric> <Property>. It ensures that only number-typed values are allowed and
     *      provides convenience functions like stepping with spinners.
     */
    var NumericEntry = Entry.extend({
        blurEvents: function() {
            return ['blur', 'change', 'remove'];
        },

        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        _setupInput: function() {
            this.inputs = jQuery('<input type="number" class="form-control input-small">')
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

    /**
     *  Class: RangeEntry
     *      Entry for modifying values of a <Range> <Property> consisting of two numbers.
     */
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
                .appendTo(this.container.find('.inputs'));

            this.setReadonly(this.property.readonly);
            this.setHidden(this.property.hidden);

            return this;
        },

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
         *  Method: _setupMiniNumeric
         *      Constructs and returns a number field with the given attributes.
         *
         *  Parameters:
         *      {Number} min   - The minimum number that should be allowed.
         *      {Number} max   - The maximum number that should be allowed.
         *      {Number} step  - The step width the value should fit in.
         *      {Number} value - The currently set value.
         *
         *  Returns:
         *      A jQuery object containing the newly constructed number input.
         */
        _setupMiniNumeric: function(min, max, step, value) {
            return jQuery('<input type="number" class="form-control input-small">')
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

    /**
     *  Class: EpsilonEntry
     *      Similar to <RangeEntry>, but the with different semantic: The second number specifies an epsilon range
     *      around the first number.
     */
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

            this.inputs = this._setupMiniNumeric(min, max, this.property.step, value[0]).css('width', '45%')
                .attr('id', this.id) // clicking the label should focus the first input
                .add(jQuery('<label> ± </label>').css('width', '10%').css('text-align', 'center'))
                .add(this._setupMiniNumeric(0, max, this.property.epsilonStep, value[1]).css('width', '45%'));

            return this;
        }
    });

    /**
     *  Class: TextEntry
     *      Simple input field for a <Text> <Property>.
     */
    var TextEntry = Entry.extend({
        changeEvents: function() {
            return ['keyup', 'cut', 'paste'];
        },

        _setupInput: function() {
            this.inputs = jQuery('<input type="text" class="form-control input-small">').attr('id', this.id);
            return this;
        },

        _value: function(newValue) {
            if (typeof newValue === 'undefined') return this.inputs.val();
            this.inputs.val(newValue);

            return this;
        }
    });

    /**
     *  TransferEntry
     *      Allows to link to other entities in the database. Looks like a normal <ChoiceEntry>,
     *      but actually fetches the available values from the backend using Ajax.
     */
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
                .addClass(Config.Classes.PROPERTY_OPEN_BUTTON)
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
         *      This Entry instance for chaining.
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
                    window.open(Config.Backend.EDITOR_URL + '/' + value, '_blank');
                }
            }.bind(this));

            return this._super();
        },

        /**
         *  Method: _setupProgressIndicator
         *      Constructs the progress indicator that is displayed as long as the list is fetched with Ajax.
         *
         *  Returns:
         *      This Entry instance for chaining.
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
         *      This Entry instance for chaining.
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
         *      This Entry instance for chaining.
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
        'BoolEntry':     BoolEntry,
        'ChoiceEntry':   ChoiceEntry,
        'CompoundEntry': CompoundEntry,
        'EpsilonEntry':  EpsilonEntry,
        'NumericEntry':  NumericEntry,
        'RangeEntry':    RangeEntry,
        'TextEntry':     TextEntry,
        'TransferEntry': TransferEntry
    }
});
