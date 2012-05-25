define(['require-config', 'require-nodes'], function(Config, Nodes) {

    function Editor(graph) {
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
        for (var y = Config.GRID_SIZE / 2; y < height; y += Config.GRID_SIZE) {
            this._background.line(0, y, width, y, {
                stroke:          Config.GRID_STROKE,
                strokeWidth:     Config.GRID_STROKE_WIDTH,
                strokeDashArray: Config.GRID_STROKE_STYLE
            });
        }

        // vertical lines
        for (var x = Config.GRID_SIZE / 2; x < width; x += Config.GRID_SIZE) {
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
        var node = uiObject.draggable.data(Config.DATA_CONSTRUCTOR);
        var position   = this._canvas.position();
        // calculate the position where to drop the element
        // we have to take into account here the offset of the container (position.left/.top)
        // as well as the grid snapping (rounding and Config.GRID_SIZE magic)
        var x = Math.round((uiEvent.pageX - position.left - uiEvent.offsetX) / Config.GRID_SIZE) * Config.GRID_SIZE;
        var y = Math.round((uiEvent.pageY - position.top  - uiEvent.offsetY) / Config.GRID_SIZE) * Config.GRID_SIZE;

        new node().appendTo(this._canvas, x, y);
    }

    return Editor;
});