define(['class', 'config', 'decimal', 'propertyMenuEntry', 'mirror', 'underscore'],
function(Class, Config, Decimal, PropertyMenuEntry, Mirror) {

    var isNumber = function(number) {
        return _.isNumber(number) && !_.isNaN(number);
    };

    var Property = Class.extend({
        node:        undefined,
        value:       undefined,
        displayName: '',
        mirror:      undefined,
        menuEntry:   undefined,

        init: function(node, definition) {
            jQuery.extend(this, definition);
            this.node = node;
            this._sanitize()
                ._setupMirror()
                ._setupMenuEntry();

            jQuery(this).trigger(Config.Events.NODE_PROPERTY_CHANGED, [this.value, this]);
        },

        menuEntryClass: function() {
            throw '[ABSTRACT] subclass responsibility';
        },

        validate: function(value, validationResult) {
            throw '[ABSTRACT] subclass responsibility';
        },

        setValue: function(newValue, issuer, propagate) {
            if (_.isEqual(this.value, newValue)) return this;
            if (typeof propagate === 'undefined') propagate = true;

            var validationResult = {};
            if (!this.validate(newValue, validationResult)) {
                throw '[VALUE ERROR] ' + validationResult.message;
            }

            this.value = newValue;
            jQuery(this).trigger(Config.Events.NODE_PROPERTY_CHANGED, [newValue, issuer]);

            if (propagate) {
                var properties = {};
                properties[this.name] = newValue;
                jQuery(document).trigger(Config.Events.NODE_PROPERTY_CHANGED, [this.node.id, properties]);
            }

            return this;
        },

        _sanitize: function() {
            var validationResult = {};
            if (!this.validate(this.value, validationResult)) {
                throw validationResult.message;
            }

            return this;
        },

        _setupMirror: function() {
            if (typeof this.mirror === 'undefined' || this.mirror === null) return this;
            this.mirror = new Mirror(this, this.node.container, this.mirror);

            return this;
        },

        _setupMenuEntry: function() {
            this.menuEntry = new (this.menuEntryClass())(this);
        }
    });

    var Bool = Property.extend({
        menuEntryClass: function() {
            return PropertyMenuEntry.BoolEntry;
        },

        validate: function(value, validationResult) {
            if (typeof value !== 'boolean') {
                validationResult.message = '[TYPE ERROR] value must be boolean';
                return false;
            }
            return true;
        },

        _sanitize: function() {
            this.value = typeof this.value === 'undefined' ? this.default : this.value;
            return this._super();
        }
    });

    var Choice = Property.extend({
        choices: undefined,
        values:  undefined,

        init: function(node, definition) {
            definition.values = typeof definition.values === 'undefined' ? definition.choices : definition.values;
            this._super(node, definition);
        },

        validate: function(value, validationResult) {
            if (!_.find(this.values, function(val){ return _.isEqual(val, value); }, this)) {
                validationResult.message = '[TYPE ERROR] no such value ' + value;
                return false;
            }
            return true;
        },

        setChoice: function(choice) {
            var choiceIndex = _.indexOf(this.choices, choice);
            if (choiceIndex < 0) {
                throw '[VALUE ERROR] invalid choice ' + choice;
            }
            return this.setValue(this.values[choiceIndex]);
        },

        _sanitize: function() {
            this.value = typeof this.value === 'undefined' ? this.default : this.value;

            if (typeof this.choices === 'undefined' || this.choices.length === 0) {
                throw '[VALUE ERROR] there must be at least one choice';
            } else if (this.choices.length != this.values.length) {
                throw '[VALUE ERROR] there must be a value for each choice';
            } else if (!_.find(this.values, function(value){ return _.isEqual(value, this.value); }, this)) {
                throw '[VALUE ERROR] unknown value ' + this.value;
            }
            return this._super();
        }
    });

    var Compound = Property.extend({
        parts: undefined,

        setValue: function(newValue, propagate) {
            if (typeof propagate === 'undefined') propagate = true;

            var validationResult = {};
            if (!this.validate(newValue, validationResult)) {
                throw '[VALUE ERROR] ' + validationResult;
            }
            this.parts[newValue[0]].setValue(newValue[1], false);

            this.value = newValue;

            if (propagate) {
                // TODO: backend
            }

            return this;
        },

        validate: function(value, validationResult) {
            if (!_.isArray(this.value) || this.value.length != 2) {
                validationResult.message = '[TYPE ERROR] value must be a tuple';
                return false;
            }

            var selection = value[0];
            var partValue = value[1];
            if (!isNumber(selection)) {
                validationResult.message = '[VALUE ERROR] selection must be a number';
                return false;
            }
            if (selection >= 0 || selection < this.parts.length) {
                validationResult.message = '[VALUE ERROR] selection must point to a part';
                return false;
            }

            return this.parts[selection].validate(partValue, validationResult);
        },

        _sanitize: function() {
            this.value = typeof this.value === 'undefined' ? this.default.slice(0) : this.value;

            if (!_.isArray(this.parts) || this.parts.length < 1) {
                throw '[VALUE ERROR] there must be at least one part';
            }
            if (isNumber(this.default[0]) && this.default[0] < 0 && this.default[0] >= this.parts.length) {
                throw '[VALUE ERROR] selection must point to a part';
            }

            return this._setupParts()._super();
        },

        _setupParts: function() {
            var newParts = [];
            _.each(this.parts, function(part) {
                newParts.push(from(this.node, part));
            }.bind(this));
            this.parts = newParts;

            return this;
        }
    });

    var Epsilon = Property.extend({
        min:        -Decimal.MAX_VALUE,
        max:         Decimal.MAX_VALUE,
        step:        undefined,
        epsilonStep: undefined,

        validate: function(value, validationResult) {
            if (!_.isArray(value) || value.length != 2) {
                validationResult.message = '[TYPE ERROR] value must be a tuple';
                return false;
            }

            var center  = value[0];
            var epsilon = value[1];

            if (typeof center  !== 'number' || window.isNaN(center) ||
                typeof epsilon !== 'number' || window.isNaN(epsilon)) {
                validationResult.message = '[TYPE ERROR] center and epsilon must be numbers';
                return false;
            } else if (epsilon < 0) {
                validationResult.message = '[VALUE ERROR] epsilon must not be negative';
                return false;
            } else if (this.min.gt(center - epsilon) || this.max.lt(center + epsilon)) {
                validationResult.message = '[VALUE ERROR] value out of bounds';
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default[0].minus(center).mod(this.step).eq(0)) {
                validationResult.message = '[VALUE ERROR] center not in value range (step)';
                return false;
            } else if (typeof this.epsilonStep !== 'undefined' &&
                       !this.default[1].minus(epsilon).mod(this.epsilonStep).eq(0)) {
                validationResult.message = '[VALUE ERROR] epsilon not in value range (step)';
                return false;
            }
            return true;
        },

        _sanitize: function() {
            if (!_.isArray(this.default) || this.default.length != 2) {
                throw '[TYPE ERROR] default must be a tuple';
            }

            this.value = typeof this.value === 'undefined' ? this.default.slice(0) : this.value;

            if (!(this.default[0] instanceof Decimal) && isNumber(this.default[0])) {
                this.default[0] = new Decimal(this.default[0]);
            } else {
                throw '[VALUE ERROR] default lower bound must be Decimal or number';
            }
            if (!(this.default[1] instanceof Decimal) && isNumber(this.default[1])) {
                this.default[1] = new Decimal(this.default[1]);
            } else {
                throw '[VALUE ERROR] default upper bound must be Decimal or number';
            }

            if (!(this.min instanceof Decimal) && isNumber(this.min)) {
                this.min = new Decimal(this.min);
            } else {
                throw '[VALUE ERROR] min must be Decimal or number';
            }
            if (!(this.max instanceof Decimal) && isNumber(this.max)) {
                this.max = new Decimal(this.max);
            } else {
                throw '[VALUE ERROR] max must be Decimal or number';
            }
            if (typeof this.step !== 'undefined' && !isNumber(this.step)) {
                throw '[VALUE ERROR] step must be a number';
            }
            if (typeof this.epsilonStep !== 'undefined' && !isNumber(this.epsilonStep)) {
                throw '[VALUE ERROR] epsilon step must be a number';
            }

            if (this.min.gt(this.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.min + '/' + this.max;
            } else if (typeof this.step !== 'undefined' && this.step < 0) {
                throw '[VALUE ERROR] step must be positive: ' + this.step;
            }

            return this._super();
        }
    });

    var Link = Property.extend({
        //TODO
    });

    var Numeric = Property.extend({
        min:    -Decimal.MAX_VALUE,
        max:     Decimal.MAX_VALUE,
        step:    undefined,

        menuEntryClass: function() {
            return PropertyMenuEntry.NumericEntry;
        },

        validate: function(value, validationResult) {
            if (!isNumber(value)) {
                validationResult.message = '[TYPE ERROR] value is not a number';
                return false;
            } else if (this.min.gt(value) || this.max.lt(value)) {
                validationResult.message = '[VALUE ERROR] value out of bounds';
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default.minus(value).mod(this.step).eq(0)) {
                validationResult.message = '[VALUE ERROR] value not in value range (step)';
                return false;
            }
            return true;
        },

        _sanitize: function() {
            this.value = typeof this.value === 'undefined' ? this.default : this.value;

            if (isNumber(this.default)) {
                this.default = new Decimal(this.default);
            } else {
                throw '[VALUE ERROR] default must be Decimal or number';
            }
            if (isNumber(this.min)) {
                this.min = new Decimal(this.min);
            } else {
                throw '[VALUE ERROR] min must be Decimal or number';
            }
            if (isNumber(this.max)) {
                this.max = new Decimal(this.max);
            } else {
                throw '[VALUE ERROR] max must be Decimal or number';
            }
            if (typeof this.step !== 'undefined' && !isNumber(this.step)) {
                throw '[VALUE ERROR] step must be a number';
            }

            if (this.min.gt(this.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.min + '/' + this.max;
            } else if (typeof this.step !== 'undefined'  && this.step < 0) {
                throw '[VALUE ERROR] step must be positive: ' + this.step;
            }

            return this._super();
        }
    });

    var Range = Property.extend({
        min: -Decimal.MAX_VALUE,
        max:  Decimal.MAX_VALUE,
        step: undefined,

        menuEntryClass: function() {
            return PropertyMenuEntry.RangeEntry;
        },

        validate: function(value, validationResult) {
            if (!_.isArray(this.value) || this.value.length != 2) {
                validationResult.message = '[TYPE ERROR] value must be a tuple';
                return false;
            }

            var lower = value[0];
            var upper = value[1];
            if (!isNumber(lower) || !isNumber(upper)) {
                validationResult.message = '[VALUE ERROR] lower and upper bound must be numbers';
                return false;
            } else if (lower > upper) {
                validationResult.message = '[VALUE ERROR] lower bound must be less or equal upper bound';
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default[0].minus(lower).mod(this.step).eq(0) ||
                                                           !this.default[1].minus(upper).mod(this.step).eq(0)) {
                validationResult.message = '[VALUE ERROR] value not in value range (step)';
                return false;
            }
            return true;
        },

        _sanitize: function() {

            if (!_.isArray(this.default) || this.default.length != 2) {
                throw '[TYPE ERROR] default must be a tuple';
            }

            this.value = typeof this.value === 'undefined' ? this.default.slice(0) : this.value;

            if (!(this.default[0] instanceof Decimal) && isNumber(this.default[0])) {
                this.default[0] = new Decimal(this.default[0]);
            } else {
                throw '[VALUE ERROR] default lower bound must be Decimal or number';
            }
            if (!(this.default[1] instanceof Decimal) && isNumber(this.default[1])) {
                this.default[1] = new Decimal(this.default[1]);
            } else {
                throw '[VALUE ERROR] default upper bound must be Decimal or number';
            }

            if (!(this.min instanceof Decimal) && isNumber(this.min)) {
                this.min = new Decimal(this.min);
            } else {
                throw '[VALUE ERROR] min must be Decimal or number';
            }
            if (!(this.max instanceof Decimal) && isNumber(this.max)) {
                this.max = new Decimal(this.max);
            } else {
                throw '[VALUE ERROR] max must be Decimal or number';
            }
            if (typeof this.step !== 'undefined' && !isNumber(this.step)) {
                throw '[VALUE ERROR] step must be a number';
            }

            if (this.min.gt(this.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.min + '/' + this.max;
            } else if (typeof this.step !== 'undefined' && this.step < 0) {
                throw '[VALUE ERROR] step must be positive: ' + this.step;
            }

            return this._super();
        }
    });

    var Text = Property.extend({
        notEmpty: false,

        menuEntryClass: function() {
            return PropertyMenuEntry.TextEntry;
        },

        validate: function(value, validationResult) {
            if (typeof value !== 'string') {
                validationResult.message = '[TYPE ERROR] value must be string';
                return false;
            } else if (this.notEmpty && value === '') {
                validationResult.message = '[VALUE ERROR] must not be empty';
                return false;
            }
            return true;
        },

        _sanitize: function() {
            this.value = typeof this.value === 'undefined' ? this.default : this.value;
            return this._super();
        }
    });

    var from = function(node, definition) {
        switch (definition.kind) {
            case 'bool':     return new Bool(node, definition);
            case 'choice':   return new Choice(node, definition);
            case 'compound': return new Compound(node, definition);
            case 'epsilon':  return new Epsilon(node, definition);
            case 'link':     return new Link(node, definition);
            case 'numeric':  return new Numeric(node, definition);
            case 'range':    return new Range(node, definition);
            case 'text':     return new Text(node, definition);

            default: throw '[VALUE ERROR] unknown property kind ' + definition.kind;
        }
    };

    return {
        Bool:     Bool,
        Choice:   Choice,
        Compound: Compound,
        Epsilon:  Epsilon,
        Link:     Link,
        Numeric:  Numeric,
        Property: Property,
        Range:    Range,
        Text:     Text,

        from: from
    };
});
