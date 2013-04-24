define(['class', 'decimal', 'underscore'], function(Class, Decimal) {

    var Property = Class.extend({
        node:  undefined,
        value: undefined,

        init: function(node, definition) {
            jQuery.extend(this, definition);
            this.node  = node;
            this.value = typeof this.value === 'undefined' ? this.default: this.value;
            this._sanityCheck();
        },

        validate: function(value, validationResult) {
            throw '[ABSTRACT] subclass responsibility';
        },

        setValue: function(newValue) {
            var validationResult = {};
            if (!this.validate(newValue, validationResult)) {
                throw '[VALUE ERROR] ' + validationResult;
            }
            this.value = newValue;
            // TODO: backend

            return this;
        },

        _sanityCheck: function() {
            var validationResult = {};
            if (!this.validate(this.value, validationResult)) {
                throw validationResult.message;
            }

            return this;
        }
    });

    var Bool = Property.extend({
        validate: function(value, validationResult) {
            if (typeof value === 'boolean') {
                validationResult.message = '[TYPE ERROR] value must be boolean';
                return false;
            }
            return true;
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
            if (_.indexOf(this.values, value) < 0) {
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

        _sanityCheck: function() {
            this._super();

            if (typeof this.choices !== 'undefined' || this.choices.length === 0) {
                throw '[VALUE ERROR] there must be at least one choice';
            } else if (this.choices.length != this.values.length) {
                throw '[VALUE ERROR] there must be a value for each choice';
            } else if (_.indexOf(this.values, this.value) < 0) {
                throw '[VALUE ERROR] unknown value ' + this.value;
            }
            return this;
        }
    });

    var Epsilon = Property.extend({
        min:        -Decimal.MAX_VALUE,
        max:         Decimal.MAX_VALUE,
        step:        undefined,
        epsilonStep: undefined,

        validate: function(value, validationResult) {
            if (typeof value !== 'array' || value.length != 2) {
                validationResult.message('[TYPE ERROR] value must be a tuple');
                return false;
            }

            var center  = value[0];
            var epsilon = value[1];

            if (typeof center  !== 'number' || window.isNaN(center) ||
                typeof epsilon !== 'number' || window.isNaN(epsilon)) {
                validationResult.message('[TYPE ERROR] center and epsilon must be numbers');
                return false;
            } else if (epsilon < 0) {
                validationResult.message('[VALUE ERROR] epsilon must not be negative');
                return false;
            } else if (this.min.gt(center - epsilon) || this.max.lt(center + epsilon)) {
                validationResult.message('[VALUE ERROR] value out of bounds');
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default[0].minus(center).mod(this.step).eq(0)) {
                validationResult.message('[VALUE ERROR] center not in value range (step)');
                return false;
            } else if (typeof this.epsilonStep !== 'undefined' &&
                       !this.default[1].minus(epsilon).mod(this.epsilonStep).eq(0)) {
                validationResult.message('[VALUE ERROR] epsilon not in value range (step)');
                return false;
            }
            return true;
        }
    });

    var Numeric = Property.extend({
        min:    -Decimal.MAX_VALUE,
        max:     Decimal.MAX_VALUE,
        step:    undefined,

        validate: function(value, validationResult) {
            if (typeof value !== 'number' || window.isNaN(value)) {
                validationResult.message('[TYPE ERROR] value is not a number');
                return false;
            } else if (this.min.gt(value) || this.max.lt(value)) {
                validationResult.message('[VALUE ERROR] value out of bounds');
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default.minus(value).mod(this.step).eq(0)) {
                validationResult.message('[VALUE ERROR] value not in value range (step)');
                return false;
            }
            return true;
        },

        _sanityCheck: function() {
            if (this.min.gt(this.max)) {
                throw '[VALUE ERROR] bounds violation min/max: ' + this.min + '/' + this.max;
            } else if (this.step && this.step < 0) {
                throw '[VALUE ERROR] step must be positive: ' + this.step;
            }
            return this;
        }
    });

    var Range = Property.extend({
        min: -Decimal.MAX_VALUE,
        max:  Decimal.MAX_VALUE,
        step: undefined,

        validate: function(value, validationResult) {
            if (typeof this.value !== 'array' || this.value.length != 2) {
                validationResult.message = '[TYPE ERROR] value must be a tuple';
                return false;
            }

            var lower = value[0];
            var upper = value[1];
            if (typeof lower !== 'number' || typeof upper !== 'number' || window.isNaN(lower) || window.isNaN(upper)) {
                validationResult.message = '[VALUE ERROR] lower and upper bound must be numbers';
                return false;
            } else if (lower > upper) {
                validationResult.message = '[VALUE ERROR] lower bound must be less or equal upper bound';
                return false;
            } else if (typeof this.step !== 'undefined' && !this.default[0].minus(lower).mod(this.step).eq(0) ||
                                                           !this.default[1].minus(upper).mod(this.step).eq(0)) {
                validationResult.message('[VALUE ERROR] value not in value range (step)');
                return false;
            }
            return true;
        }
    });

    var Text = Property.extend({
        notEmpty: false,

        validate: function(value, validationResult) {
            if (typeof value !== 'string') {
                validationResult.message = '[TYPE ERROR] value must be string';
                return false;
            } else if (this.notEmpty && value === '') {
                validationResult.message = '[VALUE ERROR] must not be empty';
                return false;
            }
            return true;
        }
    });

    var from = function(node, definition) {
        switch (definition.kind) {
            case 'bool':    return new Bool(node, definition);
            case 'choice':  return new Choice(node, definition);
            case 'numeric': return new Numeric(node, definition);
            case 'range':   return new Range(node, definition);
            case 'text':    return new Text(node, definition);

            default: throw '[VALUE ERROR] unknown property kind ' + definition.kind;
        }
    };

    return {
        Bool:     Bool,
        Choice:   Choice,
        Epsilon:  Epsilon,
        Numeric:  Numeric,
        Property: Property,
        Range:    Range,

        from: from
    };
});
