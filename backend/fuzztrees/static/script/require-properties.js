define(['require-config', 'require-oop'], function(Config) {

    function Property(node, options) {
        // skip inheritance call
        if (this.constructor === Property) return;

        this._node  = node;
        this._name  = options.name    || '';
        this._value = options.value   || '';
        this._label = options.label   || false;
        this._modify = options.modify || true;

        this._properties = jQuery('#' + Config.IDs.PROPERTIES_MENU).find('form');
    }

    Property.prototype.show = function() {
        throw 'Abstract Method - overwrite in subclass';
    }

    function Text(node, options) {
        Text.Super.constructor.call(this, node, options);
    }
    Text.Extends(Property);

    Text.prototype.show = function() {
        var id             = _.uniqueId('label');
        var fieldcontainer = jQuery('<div data-role="fieldcontain">');
        var label          = jQuery('<label for="' + id + '">' + this._name + '</label>');
        var input          = jQuery('<input id="' + id + '" type="text" value="' + this._value + '" data-mini="true">');

        fieldcontainer
            .append(label, input)
            .appendTo(this._properties)
            .fieldcontain();

        label
            .addClass(Config.Classes.PROPERTY_LABEL);

        input
            .addClass(Config.Classes.PROPERTY_TEXT)
            .textinput();

        console.log(Config.Classes.PROPERTY_LABEL, Config.Classes.PROPERTY_TEXT)
    }

    return {
        Text: Text
    };
});