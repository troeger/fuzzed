define(['mirror', 'config', 'canvas', 'class', 'jquery', 'underscore'], function(Mirror, Config, Canvas, Class) {
    /**
     * Package: Base
     */

    /**
     * Class: SVGMirror
     *
     * Blah
     */
    return Mirror.extend({
        _setupVisualRepresentation: function() {
            this.container    = jQuery('<text>')//.addClass(Config.Classes.MIRROR)
                .attr('x', this._containment.offset().left)
                .attr('y', this._containment.offset().top)
                .attr('width', '200')
                .attr('height', '30')
                .attr('fill', 'black');
        },
        _appendContainerToContainment: function(position) {
            this._containment.parent().append(this.container);
        }

    });
});