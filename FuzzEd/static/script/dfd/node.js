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
        _connectorOffset: function() {
            var topOffset = this._nodeImage.outerHeight(true) / 2;
            var width     = this._nodeImage.outerWidth(true);

            return {
                'in': {
                    'x': this.config.JSPlumb.STROKE_WIDTH + (this.connector.offset.left || 0),
                    'y': topOffset
                },
                'out': {
                    'x': width - this.config.JSPlumb.STROKE_WIDTH + (this.connector.offset.right || 0),
                    'y': topOffset
                }
            }
        },

        _connectorAnchors: function() {
            return {
                'in':  [0, 0, -1, 0],
                'out': [0, 0,  1, 0]
            }
        }
    });
});