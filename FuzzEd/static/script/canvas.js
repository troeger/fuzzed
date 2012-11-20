define(['singleton', 'config'], function(Singleton, Config) {

    /**
     *  Class: Canvas
     *      TODO
     *  Events:
     *      Config.Events.CANVAS_CLICKED        - The canvas itself was clicked.
     *      Config.Events.CANVAS_SHAPE_DROPPED - An SVG element was dropped onto the canvas.
     */
    return new Singleton.extend({
        container: undefined,

        _background: undefined,

        init: function() {
            // locate predefined DOM elements and bind Editor instance to canvas
            this.container = jQuery('#' + Config.IDs.CANVAS);

            this._setupBackground()
                ._setupCanvas();
        },

        /* Section: Coordinate conversion */

        toGrid: function(first, second) {
            var x = Number.NaN;
            var y = Number.NaN;

            // if both parameter are numbers we can take them as they are
            if (_.isNumber(first) && _.isNumber(second)) {
                x = first;
                y = second;

            // however the first parameter could also be an object
            // of the form {x: NUMBER, y: NUMBER} (convenience reasons)
            } else if (_.isObject(first)) {
                x = first.x;
                y = first.y;
            }

            return {
                x: Math.round(x / Config.Grid.SIZE),
                y: Math.round(y / Config.Grid.SIZE)
            }
        },

        toPixel: function(first, second) {
            var x = Number.NaN;
            var y = Number.NaN;

            if (_.isNumber(first) && _.isNumber(second)) {
                x = first;
                y = second;

            } else if (_.isObject(first)) {
                x = first.x;
                y = first.y;
            }

            return {
                x: x * Config.Grid.SIZE,
                y: y * Config.Grid.SIZE
            }
        },

        /* Section: Internals */

        _drawGrid: function() {
            var height = this.canvas.height();
            var width  = this.canvas.width();

            // clear old background and resize svg container to current canvas size
            // important when window was resized in the mean time
            this._background.clear();
            this._background.configure({
                height: height,
                width:  width
            });

            // horizontal lines
            for (var y = Config.Grid.SIZE; y < height; y += Config.Grid.SIZE) {
                this._background.line(0, y, width, y, {
                    stroke:          Config.Grid.STROKE,
                    strokeWidth:     Config.Grid.STROKE_WIDTH,
                    strokeDashArray: Config.Grid.STROKE_STYLE
                });
            }

            // vertical lines
            for (var x = Config.Grid.SIZE; x < width; x += Config.Grid.SIZE) {
                this._background.line(x, 0, x, height, {
                    stroke:          Config.Grid.STROKE,
                    strokeWidth:     Config.Grid.STROKE_WIDTH,
                    strokeDashArray: Config.Grid.STROKE_STYLE
                });
            }

            return this;
        },

        _setupBackground: function() {
            this._background = this.container.svg().svg('get');
            this._drawGrid();
            // clicks on the canvas clears the selection
            this.canvas.click(function() {jQuery(document).trigger(Config.Events.CANVAS_CLICKED);}.bind(this));
            // redraw the background grid when the window is being resized
            jQuery(window).resize(this._drawGrid.bind(this));

            return this;
        },

        _setupCanvas: function() {
            // make canvas droppable for shapes from the shape menu
            this.canvas.droppable({
                accept:    'svg',
                tolerance: 'fit',
                drop:      function(uiEvent, uiObject) {
                    var kind     = uiObject.draggable.attr('id');
                    var offset   = this.container.offset();
                    var position = {x: uiEvent.pageX - offset.left, y: uiEvent.pageY - offset.top};
                    jQuery(document).trigger(Config.Events.CANVAS_SHAPE_DROPPED, kind, position);
                }.bind(this)
            });

            return this;
        }
    });
});
