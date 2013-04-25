define(['class'], function(Class) {

    var Entry = Class.extend({
        id: undefined,
        property: undefined,
        container: undefined,
        input: undefined,

        init: function(property) {
            this.id = _.uniqueId('property');
            this.property = property;

            this._setupVisualRepresentation();
        },

        show: function(on) {
            on.append(this.container);

            return this;
        },

        hide: function() {
            this.container.remove();

            return this;
        },

        _setupVisualRepresentation: function() {
            this._setupContainer()
                ._setupInput();
            this.container.find('.controls').append(this.input);

            return this;
        },

        _setupContainer: function() {
            this.container = jQuery(
                '<div class="control-group">\
                    <label class="control-label" for="' + this.id + '">' + (this.property.displayName || '') + '</label>\
                    <div class="controls"></div>\
                </div>'
            );

            return this;
        },

        _setupInput: function() {
            throw '[ABSTRACT] subclass responsibility';
        }
    });

    var TextEntry = Entry.extend({

        _setupInput: function() {
            this.input = jQuery('<input type="text" class="input-medium">')
                .attr('id', this.id)
                //TODO
                //.attr('disabled', this.options.disabled ? 'disabled' : null)
                .val(this.property.value);

            return this;
        }
    });


    return {
        'TextEntry': TextEntry
    }
});
