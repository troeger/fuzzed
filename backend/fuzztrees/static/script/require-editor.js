define(['require-config', 'require-nodes'], function(Config, Nodes) {

    function Editor(graph) {
		console.log("Hello");
        this._initializeMember(graph);
        this._initializeJsPlumb();

        this._drawGrid();
        this._enableShapeMenu();
    }

    Editor.prototype.graphId = function() {
        return this._graphId;
    }

    Editor.prototype._initializeMember = function(graph) {
        this._graphId    = graph;
        this._body       = jQuery('body');
        this._shapes     = this._body.find(Config.SHAPES_MENU);
        this._canvas     = this._body.find(Config.CANVAS);
        this._background = this._canvas.svg().svg('get');
    }

    Editor.prototype._initializeJsPlumb = function() {
        jsPlumb.importDefaults({
            EndpointStyle: {
                fillStyle:   Config.JSPLUMB_ENDPOINT_FILL
            },
            Endpoint:        [Config.JSPLUMB_ENDPOINT_STYLE, {radius: Config.JSPLUMB_ENDPOINT_RADIUS}],
            PaintStyle: {
                strokeStyle: Config.JSPLUMB_LINE_STROKE,
                lineWidth:   Config.JSPLUMB_LINE_STROKE_WIDTH
            },
            Connector:       Config.JSPLUMB_LINE_STYLE,
            Anchors:         ['BottomMiddle', 'TopMiddle']
        });
    }

    Editor.prototype._drawGrid = function() {
        var height = this._canvas.height();
        var width  = this._canvas.width();

        // horizontal lines
        for (var y = Config.GRID_SIZE >> 1; y < height; y += Config.GRID_SIZE) {
            this._background.line(0, y, width, y, {
                stroke:          Config.GRID_STROKE,
                strokeWidth:     Config.GRID_STROKE_WIDTH,
                strokeDashArray: Config.GRID_STROKE_STYLE
            });
        }

        // vertical lines
        for (var x = Config.GRID_SIZE >> 1; x < width; x += Config.GRID_SIZE) {
            this._background.line(x, 0, x, height, {
                stroke:          Config.GRID_STROKE,
                strokeWidth:     Config.GRID_STROKE_WIDTH,
                strokeDashArray: Config.GRID_STROKE_STYLE
            });
        }
    }

    Editor.prototype._enableShapeMenu = function() {
        var _this = this;

        this._canvas.droppable({
            accept:    Config.NODE_THUMBNAIL_CLASS,
            tolerance: 'fit',
            drop:      function(uiEvent, uiObject) {
                _this._handleShapeDrop(uiEvent, uiObject);
            }
        });

        this._shapes.find(Config.NODE_THUMBNAIL_CLASS).draggable({
            helper:   'clone',
            opacity:  Config.DRAGGING_OPACITY,
            cursor:   Config.DRAGGING_CURSOR,
            appendTo: this._body,
            revert:   'invalid'
        });
    }

    Editor.prototype._handleShapeDrop = function(uiEvent, uiObject) {
        var nodeType    = uiObject.draggable.data(Config.DATA_CONSTRUCTOR);
        var offset      = this._canvas.offset();
        var coordinates = this._toGridCoordinates(uiEvent.pageX - offset.left, uiEvent.pageY - offset.top);
        var halfGrid    = Config.GRID_SIZE >> 1;
        var node        = new nodeType();

        with (node) {
            appendTo(this._canvas);
            moveTo(coordinates.x * Config.GRID_SIZE + halfGrid, coordinates.y * Config.GRID_SIZE + halfGrid);
        }
    }

    Editor.prototype._toGridCoordinates = function(first, second) {
        var halfGrid = Config.GRID_SIZE >> 1;
        var x        = Number.NaN;
        var y        = Number.NaN;

        if (jQuery.isNumeric(first) && jQuery.isNumeric(second)) {
            x = first;
            y = second;

        } else if (typeof first === 'object') {
            x = first.x;
            y = first.y;
        }

        return {
            x: Math.round((first  - halfGrid) / Config.GRID_SIZE),
            y: Math.round((second - halfGrid) / Config.GRID_SIZE)
        }
    }

    return Editor;
});