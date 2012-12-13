define(['config', 'canvas', 'class'], function(Config, Canvas, Class) {
    var Mirror = Class.extend({
        _container: undefined,
        _mirror:    undefined,
        _prefix:    undefined,
        _suffix:    undefined,

        init: function(container, properties) {
            this._container = container;
            this._mirror    = jQuery('<span>')
                .addClass(Config.Classes.MIRROR)
                // The label should be double the grid/node width so that there would be a large 
                // text box below the node. This requires us to offset them by a quarter of its 
                // size (already partially centered below the node). However, we need to fiddle a 
                // little bit with the width and the offset in order to not cover the grid lines 
                // behind the box.
                .css('width', Canvas.gridSize * 2 - Config.Grid.STROKE_WIDTH * 4)
                .css('margin-left', -(Canvas.gridSize / 2) + Config.Grid.STROKE_WIDTH);
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
            }.bind(this));

            // add the mirror to the container at specified location (bottom or top)
            if (properties.position === 'bottom') {
                this._container.append(this._mirror);
            } else if (properties.position === 'top') {
                this._container.prepend(this._mirror);
            } else {
                throw 'Unknown position for mirror ' + properties.position;
            }

            return this;
        },

        show: function(text) {
            if (typeof text === 'undefined' || text === null || text === '') {
                this._mirror.css('display', 'none');
            } else {
                // remove 'display: none' from element to show it again
                // '.show()' won't work because this sets display to 'inline', but we need 'block'
                this._mirror.css('display', '');
                this._mirror.html(this._prefix + text + this._suffix);
            }

            return this;
        }
    });

    return Mirror;
});