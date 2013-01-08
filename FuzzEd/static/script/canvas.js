define(['class', 'config', 'jquery.svgdom', 'jquery.ui/jquery.ui.droppable', 'jquery.ui/jquery.ui.selectable'],
function(Class, Config) {

    /**
     *  Class: Canvas
     *      TODO
     *  Events:
     *      Config.Events.CANVAS_SHAPE_DROPPED - An SVG element was dropped onto the canvas.
     */
    var Canvas = Class.extend({
        container: undefined,
        gridSize:  Config.Grid.SIZE,

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
                x: Math.round(x / this.gridSize),
                y: Math.round(y / this.gridSize)
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
                x: x * this.gridSize,
                y: y * this.gridSize
            }
        },

        /* Section: Internals */

        _drawGrid: function() {
            var height = this.container.height();
            var width  = this.container.width();

            // clear old background and resize svg container to current canvas size
            // important when window was resized in the mean time
            this._background.clear();
            this._background.configure({
                height: height,
                width:  width
            });

            // horizontal lines
            for (var y = this.gridSize; y < height; y += this.gridSize) {
                this._background.line(0, y, width, y, {
                    stroke:          Config.Grid.STROKE,
                    strokeWidth:     Config.Grid.STROKE_WIDTH,
                    strokeDashArray: Config.Grid.STROKE_STYLE
                });
            }

            // vertical lines
            for (var x = this.gridSize; x < width; x += this.gridSize) {
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
            // redraw the background grid when the window is being resized
            jQuery(window).resize(this._drawGrid.bind(this));

            return this;
        },

        _setupCanvas: function() {
            // make canvas droppable for shapes from the shape menu
            this.container.droppable({
                accept:    'svg',
                tolerance: 'fit',
                drop:      function(uiEvent, uiObject) {
                    var kind     = uiObject.draggable.attr('id');
                    var offset   = this.container.offset();
                    var position = {x: uiEvent.pageX - offset.left, y: uiEvent.pageY - offset.top};
                    jQuery(document).trigger(Config.Events.CANVAS_SHAPE_DROPPED, [kind, position]);
                }.bind(this)
            });

            this.container.selectable({
                filter: '.' + Config.Classes.NODE + ', .' + Config.Classes.JSPLUMB_CONNECTOR,
                selecting: function(event, ui) {
                    var selection = jQuery(ui.selecting);
                    if (selection.hasClass(Config.Classes.NODE)) {
                        selection.data(Config.Keys.NODE).select();
                    }

                    if (selection.hasClass(Config.Classes.JSPLUMB_CONNECTOR)) {
                        var edgeId = selection.attr(Config.Attributes.CONNECTION_ID);
                        jQuery(document).trigger(Config.Events.CANVAS_EDGE_SELECTED, edgeId);
                    }
                },
                unselecting: function(event, ui) {
                    var unselection = jQuery(ui.unselecting);
                    if (unselection.hasClass(Config.Classes.NODE)) {
                        unselection.data(Config.Keys.NODE).deselect();
                    }

                    if (unselection.hasClass(Config.Classes.JSPLUMB_CONNECTOR)) {
                        var edgeId = unselection.attr(Config.Attributes.CONNECTION_ID);
                        jQuery(document).trigger(Config.Events.CANVAS_EDGE_UNSELECTED, edgeId);
                    }
                },
                stop: function(event, ui) {
                    jQuery(document).trigger(Config.Events.CANVAS_SELECTION_STOPPED);
                }
            });

            return this;
        }
    });

    return new Canvas();
});
