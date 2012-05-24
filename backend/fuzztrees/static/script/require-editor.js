define(['require-config', 'require-nodes'], function(Config, Nodes) {

    function Editor(graphId) {
        this._initializeMember(graphId);
        this._initializeJsPlumb();

        this._layout();
        this._drawGrid();

        this._enableShapeMenu();
    }

    Editor.prototype.graphId = function() {
        return this._graphId;
    }

    Editor.prototype._initializeMember = function(graphId) {
        this._graphId   = graphId;
        this._body      = jQuery('body');
        this._shapes    = this._body.find(Config.SHAPES_MENU);
        this._container = this._body.find(Config.CANVAS);
        this._paper     = Raphael(this._container[0], this._body.width(), this._body.height());
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

    Editor.prototype._layout = function() {
        var layoutOptions = {
            defaults: {
                applyDefaultStyles: false,
                resizable:          false,
                closable:           false,
                spacing_open:       Config.LAYOUT_SPACING
            },
            north: {
                size:               Config.LAYOUT_NORTH_SIZE
            }
        };

        this._body.layout(layoutOptions);
    }

    Editor.prototype._drawGrid = function() {
        var height = this._container.height();
        var width  = this._container.width();

        // horizontal lines
        for (var y = Config.GRID_SIZE / 2; y < height; y += Config.GRID_SIZE) {
            this._paper.path('M0 ' + y + ' L' + width + ' ' + y)
                .attr('stroke',           Config.GRID_STROKE)
                .attr('stroke-width',     Config.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Config.GRID_STROKE_STYLE);
        }

        // vertical lines
        for (var x = Config.GRID_SIZE / 2; x < width; x += Config.GRID_SIZE) {
            this._paper.path('M' + x + ' 0 L' + x + ' ' + height)
                .attr('stroke',           Config.GRID_STROKE)
                .attr('stroke-width',     Config.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Config.GRID_STROKE_STYLE);
        }
    }

    Editor.prototype._enableShapeMenu = function() {
        var _this = this;

        this._container.droppable({
            accept:    Config.NODES_CLASS,
            tolerance: 'fit',
            drop:      function(uiEvent, uiObject) {
                _this._handleShapeDrop(uiEvent, uiObject);
            }
        });

        this._shapes.find(Config.NODES_CLASS).draggable({
            helper:   'clone',
            appendTo: this._body,
            revert:   'invalid'
        });
    }

    Editor.prototype._handleShapeDrop = function(uiEvent, uiObject) {
        var offset   = this._container.position();
        offset.left += uiEvent.offsetX;
        offset.top  += uiEvent.offsetY;

        Nodes
            .fromId(uiObject.draggable.attr('id'))
            .appendTo(this._container, event.pageX - offset.left, event.pageY - offset.top);
    }

    return Editor;
});