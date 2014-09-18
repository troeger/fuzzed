define(['factory', 'node'], function(Factory, AbstractNode) {
    /**
     * Package: RBD
     */

    /**
     * Class: RBDNode
     *      RBD-specific node implementation of the basic node. Mainly need to change the modeling direction here from a
     *      top/bottom manner to left/right.
     *
     * Extends: <Base::Node>.
     */
    return AbstractNode.extend({
        _connectorOffset: function() {
            var topOffset = this._nodeImage.outerHeight(true) / 2;
            var width     = this._nodeImage.outerWidth(true);

            return {
                'in': {
                    'x': Factory.getModule('Config').JSPlumb.STROKE_WIDTH + (this.connector.offset.left || 0),
                    'y': topOffset
                },
                'out': {
                    'x': width - Factory.getModule('Config').JSPlumb.STROKE_WIDTH + (this.connector.offset.right || 0),
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
                var leftOffset = -Factory.getModule('Config').JSPlumb.STROKE_WIDTH + (this.connector.offset.right || 0);

                this._connectionHandle = jQuery('<i class="fa fa-plus"></i>')
                    .addClass(Factory.getModule('Config').Classes.NODE_HALO_CONNECT)
                    .css({
                        top:  this._nodeImageContainer.position().top  + this._nodeImage.outerHeight(true) / 2,
                        left: this._nodeImageContainer.position().left + this._nodeImage.outerWidth() + leftOffset
                    })
                    .appendTo(this.container);
            }

            return this;
        }
    });
});
