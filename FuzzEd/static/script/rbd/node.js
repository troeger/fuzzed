define(['node', 'rbd/config'], function(AbstractNode, Config) {

    /**
     *  Concrete rbd implementation
     */
    return AbstractNode.extend({
        _connectorOffset: function() {
            var topOffset = this._nodeImage.outerHeight(true) / 2;
            var width     = this._nodeImage.outerWidth(true);

            return {
                'in': {
                    'x': Config.JSPlumb.STROKE_WIDTH,
                    'y': topOffset
                },
                'out': {
                    'x': width - Config.JSPlumb.STROKE_WIDTH,
                    'y': topOffset
                }
            }
        },

        _connectorAnchors: function() {
            return {
                'in':  [0, 0, -1, 0],
                'out': [0, 0,  1, 0]
            }
        },

        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnections != 0) {
                this._connectionHandle = jQuery('<i class="icon-plus icon-white"></i>')
                    .addClass(Config.Classes.NODE_HALO_CONNECT)
                    .css({
                        'top':  this._nodeImage.position().top  + this._nodeImage.outerHeight(true) / 2,
                        'left': this._nodeImage.position().left + this._nodeImage.outerWidth() - Config.JSPlumb.STROKE_WIDTH
                    })
                    .appendTo(this.container);
            }

            return this;
        }
    });
});
