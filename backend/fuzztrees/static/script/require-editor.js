define(['require-config', 'require-nodes'], function(Config, Nodes) {

    function Editor(graph) {
        this._initializeMember(graph);
        this._initializeJsPlumb();
        this._initializeBackground();
        this._initializeShapeMenu();
        this._initializePropertiesMenu();
    }

    Editor.prototype.graphId = function() {
        return this._graphId;
    }

    Editor.prototype._initializeMember = function(graph) {
        this._graphId    = graph;
        this._body       = jQuery('body');
        this._shapes     = this._body.find('#'+Config.IDs.SHAPES_MENU);
        this._canvas     = this._body.find('#'+Config.IDs.CANVAS);
        this._background = this._canvas.svg().svg('get');
    }

    Editor.prototype._initializeJsPlumb = function() {
        jsPlumb.importDefaults({
            EndpointStyle: {
                fillStyle:   Config.JSPlumb.ENDPOINT_FILL
            },
            Endpoint:        [Config.JSPlumb.ENDPOINT_STYLE, {radius: Config.JSPlumb.ENDPOINT_RADIUS}],
            PaintStyle: {
                strokeStyle: Config.JSPlumb.STROKE,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            },
            Connector:       Config.JSPlumb.STROKE_STYLE,
            Anchors:         ['BottomMiddle', 'TopMiddle']
        });
    }

    Editor.prototype._initializeBackground = function() {
        var _this = this;

        _this._drawGrid();
        jQuery(window).resize(function() {
            _this._drawGrid();
        });
    }

    Editor.prototype._drawGrid = function() {
        var height = this._canvas.height();
        var width  = this._canvas.width();

        // clear old background and resize svg container to current canvas size - needed for resize callback
        this._background.clear();
        this._background.configure({
            height: height,
            width:  width
        });

        // horizontal lines
        for (var y = Config.Grid.HALF_SIZE; y < height; y += Config.Grid.SIZE) {
            this._background.line(0, y, width, y, {
                stroke:          Config.Grid.STROKE,
                strokeWidth:     Config.Grid.STROKE_WIDTH,
                strokeDashArray: Config.Grid.STROKE_STYLE
            });
        }

        // vertical lines
        for (var x = Config.Grid.HALF_SIZE; x < width; x += Config.Grid.SIZE) {
            this._background.line(x, 0, x, height, {
                stroke:          Config.Grid.STROKE,
                strokeWidth:     Config.Grid.STROKE_WIDTH,
                strokeDashArray: Config.Grid.STROKE_STYLE
            });
        }
    }

    Editor.prototype._initializeShapeMenu = function() {
        var _this = this;

        // make shape menu itself draggable
        jQuery('#'+Config.IDs.SHAPES_MENU).draggable({
            containment:   '#'+Config.IDs.CONTENT,
            stack:         '.'+Config.Classes.NODE,
            cursor:        Config.Dragging.CURSOR,
            scroll:        false,
            snap:          '#'+Config.IDs.CONTENT,
            snapMode:      'inner',
            snapTolerance: Config.Dragging.SNAP_TOLERANCE
        });

        // make shapes in the menu draggable
        this._shapes.find('.'+Config.Classes.NODE_THUMBNAIL).draggable({
            helper:   'clone',
            opacity:  Config.Dragging.OPACITY,
            cursor:   Config.Dragging.CURSOR,
            appendTo: this._body,
            revert:   'invalid',
            zIndex:  200
        });

        // make canvas droppable for shapes in the menu
        this._canvas.droppable({
            accept:    '.'+Config.Classes.NODE_THUMBNAIL,
            tolerance: 'fit',
            drop:      function(uiEvent, uiObject) {
                _this._handleShapeDrop(uiEvent, uiObject);
            }
        });
    }

    Editor.prototype._initializePropertiesMenu = function() {
        jQuery('#'+Config.IDs.PROPERTIES_MENU).draggable({
            containment:   '#'+Config.IDs.CONTENT,
            stack:         '.'+Config.Classes.NODE,
            cursor:        Config.Dragging.CURSOR,
            scroll:        false,
            snap:          '#'+Config.IDs.CONTENT,
            snapMode:      'inner',
            snapTolerance: Config.Dragging.SNAP_TOLERANCE
        });
    }

    Editor.prototype._handleShapeDrop = function(uiEvent, uiObject) {
        var node        = new (uiObject.draggable.data(Config.Keys.CONSTRUCTOR))();
        var offset      = this._canvas.offset();
        var coordinates = this._toGridCoordinates(uiEvent.pageX - offset.left, uiEvent.pageY - offset.top);

        node
            .moveTo(coordinates.x * Config.Grid.SIZE, coordinates.y * Config.Grid.SIZE)
            .appendTo(this._canvas);
    }

    Editor.prototype._toGridCoordinates = function(first, second) {
        var x = Number.NaN;
        var y = Number.NaN;

        if (jQuery.isNumeric(first) && jQuery.isNumeric(second)) {
            x = first;
            y = second;

        } else if (typeof first === 'object') {
            x = first.x;
            y = first.y;
        }

        return {
            x: Math.round((first  - Config.Grid.HALF_SIZE) / Config.Grid.SIZE),
            y: Math.round((second - Config.Grid.HALF_SIZE) / Config.Grid.SIZE)
        }
    }

    return Editor;
});