define(['class', 'config', 'jquery.svgdom', 'jquery.ui/jquery.ui.droppable', 'jquery.ui/jquery.ui.selectable'],
function(Class, Config) {
    /**
     * Package: Base
     */

    /**
     *  Class: {Singleton} Canvas
     *
     *  This singleton class models the canvas entity. It is mainly responsible for two things: painting the background
     *  grid and providing coordinate conversion functions (pixel to grid coordinates and vice versa). The canvas is a
     *  the drop and selectable target for <Nodes>.
     *
     *  Events:
     *      Config.Events.CANVAS_SHAPE_DROPPED - An SVG element was dropped onto the canvas.
     */
    return new (Class.extend({
        /**
         * Group: Members
         *
         * {DOMElement} container   - The canvas container element - i.e. DOM element with id <Config::IDs::CANVAS>.
         * {Number}     gridSize    - Size in pixels of one canvas grid cell (default: <Config::Grid::SIZE>.
         *
         * {DOMElement} _background - SVG DOM element where the dashed grid lines are drawn on.
         */
        container:   undefined,
        gridSize:    Config.Grid.SIZE,

        _background: undefined,

        /**
         * Constructor: init
         *
         * Creates a new instance of the <Canvas> class. Invokes permanent side effects on the DOM and should therefore
         * only be called once.
         */
        init: function() {
            // locate predefined DOM elements and bind Editor instance to canvas
            this.container = jQuery('#' + Config.IDs.CANVAS);

            this._setupBackground()
                ._setupCanvas();
        },

        /**
         * Section: Coordinate conversion
         */

        /**
         * Method: toGrid
         *
         * Converts the passed pixel coordinates to their respective grid coordinates. This method will look for the
         * closest grid coordinate, if the pixel coordinates do not represent a "grid crossing".
         *
         * Parameters:
         *   {Object|Number} first  - Either an object of the form {'x': ..., 'y': ...} representing the complete pixel
         *                            coordinates or a single number standing for the pixel x coordinate.
         *   {Number}        second - If first is not an object, a number standing for the pixel y coordinate or assumed
         *                            to be undefined.
         *
         * Returns:
         *   An {Object} containing the 'x' and 'y' grid coordinates of the passed pixel coordinates.
         */
        toGrid: function(first, second) {
            var x = window.Number.NaN;
            var y = window.Number.NaN;

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
                x: window.Math.round(x / this.gridSize),
                y: window.Math.round(y / this.gridSize)
            }
        },

        /**
         * Method: toPixel
         *
         * Converts the passed grid coordinates to their pixel equivalent. Does NOT implement snap behaviour to the
         * closest grid crossing.
         *
         * Parameters:
         *   {Object|Number} first  - Either an object of the form {'x': ..., 'y': ...} representing the complete grid
         *                            coordinates or a single number standing for the grid's x coordinate.
         *   {Number}        second - If the parameter first is an object assumed to be undefined, otherwise a number
         *                            standing for the grid's y coordinate.
         *
         * Returns:
         *   An {Object} containing the 'x' and 'y' pixel coordinates of the passed grid coordinates.
         */
        toPixel: function(first, second) {
            var x = window.Number.NaN;
            var y = window.Number.NaN;

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

        /**
         *  Section: Initialization
         */

        /**
         * Methid: _drawGrid
         *
         * Draws the dashed grid line on the <Canvas::_background> DOM element. Clears any previous lines from the
         * background first (needed in case of window resizing). The lines are drawn from top to bottom and left to
         * right, using SVG lines.
         *
         * Returns:
         *   This {<Canvas>} instance for chaining.
         */
        _drawGrid: function() {
            var height = this.container.height();
            var width  = this.container.width();

            // clear old background and resize svg container to current canvas size
            // important when window was resized in the mean time
            this._background.clear();
            this._background.configure({
                height: height,
                width:  width,
                class:  Config.Classes.NO_PRINT
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

        /**
         * Method: _setupBackground
         *
         * Creates the _background SVG DOM element, draws the grid initially for the first time and ensures that the
         * grid is refreshed on window resizing.
         *
         * Returns:
         *   This {<Canvas>} instance for chaining.
         */
        _setupBackground: function() {
            this._background = this.container.svg().svg('get');
            this._drawGrid();
            // on window resize, redraw grid
            jQuery(window).resize(this._drawGrid.bind(this));

            return this;
        },

        /**
         * Method: _setupCanvas
         *
         * This method sets the canvas up to be a drop and select target. The first allows that shapes from the shapes
         * menu can be dragged and dropped onto the canvas. Whereas the latter is responsible to allow the user to make
         * rectangular boxes for multi selects. While setting up the two targets, this method also registers callbacks
         * to handle un- and highlighting on selection and to re-trigger the custom events stated below.
         *
         * Returns:
         *   This {<Canvas>} instance for chaining.
         *
         * Triggers:
         *   <Config::Events::CANVAS_SHAPE_DROPPED>
         *   <Config::Events::CANVAS_EDGE_SELECTED>
         *   <Config::Events::CANVAS_EDGE_UNSELECTED>
         *   <Config::Events::CANVAS_SELECTION_STOPPED>
         */
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
                    // highlight nodes...
                    var selection = jQuery(ui.selecting);
                    if (selection.hasClass(Config.Classes.NODE)) {
                        selection.data(Config.Keys.NODE).select();
                    }

                    // ... and edges that are part of the new selection
                    if (selection.hasClass(Config.Classes.JSPLUMB_CONNECTOR)) {
                        var edgeId = selection.attr(Config.Attributes.CONNECTION_ID);
                        jQuery(document).trigger(Config.Events.CANVAS_EDGE_SELECTED, edgeId);
                    }
                },
                unselecting: function(event, ui) {
                    // unhighlight nodes...
                    var unselection = jQuery(ui.unselecting);
                    if (unselection.hasClass(Config.Classes.NODE)) {
                        unselection.data(Config.Keys.NODE).deselect();
                    }

                    // ... and edges when the selection is cleared
                    if (unselection.hasClass(Config.Classes.JSPLUMB_CONNECTOR)) {
                        var edgeId = unselection.attr(Config.Attributes.CONNECTION_ID);
                        jQuery(document).trigger(Config.Events.CANVAS_EDGE_UNSELECTED, edgeId);
                    }
                },
                stop: function() {
                    // tell other (e.g. <PropertyMenu>) that selection is done and react to the new selection
                    jQuery(document).trigger(Config.Events.CANVAS_SELECTION_STOPPED);
                }
            });

            return this;
        }
    }));
});
