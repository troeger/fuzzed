define(['require-config', 'require-oop'], function(Config) {

    /*
     *  Abstract Property
     */
    function Property(node, options) {
        // skip inheritance call
        if (this.constructor === Property) return;

        this._node   = node;
        this._name   = options.name   || '';
        this._value  = options.value  || '';
        this._label  = options.label  || false;
        this._modify = options.modify || true;
    }

    Property.prototype.show = function() {
        throw 'Abstract Method - overwrite in subclass';
    }

    /*
     *  Text Property
     */
    function Text(node, options) {
        Text.Super.constructor.call(this, node, options);
    }
    Text.Extends(Property);

    Text.prototype.show = function(container) {
        var id             = _.uniqueId('label');
        var fieldcontainer = jQuery('<div data-role="fieldcontain">');
        var label          = jQuery('<label for="' + id + '">' + this._name + '</label>');
        var input          = jQuery('<input id="' + id + '" type="text" value="' + this._value + '" data-mini="true">');

        fieldcontainer
            .append(label, input)
            .appendTo(container)
            .fieldcontain();

        label
            .addClass(Config.Classes.PROPERTY_LABEL);

        input
            .addClass(Config.Classes.PROPERTY_TEXT)
            .textinput();
    }

    return {
        Text: Text
    };
});