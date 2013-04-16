define(['class', 'decimal'], function(Class, Decimal) {

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

    var Numeric = Property.extend({
        default: 0,
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

    var Text = Class.extend({
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

    function from(node, definition) {
        if (definition.kind === 'numeric') {
            return new Numeric(node, definition);
        } else if (definition.kind === 'text') {
            return new Text(node, definition);
        }
        throw '[VALUE ERROR] unknown property kind ' + definition.kind;
    }

    return {
        Numeric:  Numeric,
        Property: Property,

        from: from
    };
});
