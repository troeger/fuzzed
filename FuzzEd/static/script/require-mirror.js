define(['require-config', 'require-oop'], function(Config, Class) {
    var Mirror = Class.extend({
        _container: undefined,
        _mirror:    undefined,
        _prefix:    undefined,
        _suffix:    undefined,

        init: function(container, properties) {
            this._container = container;
            this._mirror    = jQuery('<span>')
                .addClass(Config.Classes.MIRROR)
                .css('width', Config.Grid.DOUBLE_SIZE)
                .css('margin-left', -Config.Grid.HALF_SIZE);
            this._prefix    = properties.prefix || '';
            this._suffix    = properties.suffix || '';

            // set style of the mirror (bold or italic)
            _.each(properties.style, function(style) {
                if (style === 'italic') {
                    this._mirror.addClass(Config.Classes.MIRROR_ITALIC);
                } else if (style === 'bold') {
                    this._mirror.addClass(Config.Classes.MIRROR_BOLD);
                } else if (style === 'large') {
                    this._mirror.addClass(Config.Classes.MIRROR_LARGE);
                }
            }.bind(this))

            // add the mirror to the container at specified location (bottom or top)
            if (properties.position === 'bottom') {
                this._container.append(this._mirror);

            } else if (properties.position === 'top') {
                this._container.prepend(this._mirror);

            } else {
                throw 'Unknown position for mirror ' + properties.position;
            }

            this.show('test');
        },

        show: function(text) {
            this._mirror.html(this._prefix + text + this._suffix);
        }
    })

    return Mirror;
})