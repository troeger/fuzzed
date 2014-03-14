define(['dfd/config', 'node'], function(Config, AbstractNode) {
    /**
     * Package: DFD
     */

    /**
     * Class: DfdNode
     *
     * Tiny class introduced for clearer typing and to adjust config to <DFD::Config>.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        getConfig: function() {
            return Config;
        },

        _connectorAnchors: function() {
            return {
                'in':  [0.5, 0, 0, 0],
                'out': [0.5, 0, 0, 0]
            }
        },

        _connectorOffset: function() {
            var topOffset = this._nodeImageContainer.outerWidth(true) / 2;

            return {
                'in': {
                    'x': 0,
                    'y': topOffset
                },
                'out': {
                    'x': 0,
                    'y': topOffset
                }
            }
        },

        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnection == 0) return this;

            var position = this._nodeImageContainer.position();
            var stroke   = this.config.JSPlumb.STROKE_WIDTH;

            this._connectionHandle = jQuery('<i class="fa fa-plus"></i>')
                .addClass(this.config.Classes.NODE_HALO_CONNECT)
                .css({
                    'top':  position.top  + this._nodeImage.outerHeight(true) / 2 + stroke * 1.5,
                    'left': position.left + this._nodeImage.outerWidth(true)  / 2
                })
                .appendTo(this.container);

            return this;
        }
    });
});