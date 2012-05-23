define(['require-nodes'], function(Nodes) {
    Editor.GRID_STROKE       = '#eee';
    Editor.GRID_STROKE_WIDTH = 1;
    Editor.GRID_STROKE_STYLE = '--';
    Editor.GRID_OFFSET       = 50;

    function Editor(graphId) {
        this._initialize();
        this._layout();
        this._drawGrid();
        this._initializeJsPlumb();

        // XXX: test node
        var node = new Nodes.BasicEvent();
        node.appendTo(this._container);
        var node2 = new Nodes.UndevelopedEvent();
        node2.appendTo(this._container);
    }

    Editor.prototype._initialize = function() {
        this._body      = jQuery('body');
        this._container = this._body.find('#canvas');
        this._paper     = Raphael(this._container[0], this._body.width(), this._body.height());
    }

    Editor.prototype._drawGrid = function() {
        var height = this._body.height();
        var width  = this._body.width();

        // horizontal lines
        for (var y = Editor.GRID_OFFSET; y < height; y += Editor.GRID_OFFSET) {
            this._paper.path('M0 ' + y + ' L' + width + ' ' + y)
                .attr('stroke', Editor.GRID_STROKE)
                .attr('stroke-width', Editor.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Editor.GRID_STROKE_STYLE);
        }

        // vertical lines
        for (var x = Editor.GRID_OFFSET; x < width; x += Editor.GRID_OFFSET) {
            this._paper.path('M' + x + ' 0 L' + x + ' ' + height)
                .attr('stroke', Editor.GRID_STROKE)
                .attr('stroke-width', Editor.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Editor.GRID_STROKE_STYLE);
        }
    }

    Editor.prototype._layout = function() {
        var layoutOptions = {
            defaults: {
                applyDefaultStyles: false,
                resizable: false,
                closable: false,
                spacing_open: 0
            },
            north: {
                size: 24
            }
        };

        this._body.layout(layoutOptions);
    }

    Editor.prototype._initializeJsPlumb = function() {
        jsPlumb.importDefaults({
            EndpointStyle: {
                fillStyle: '#00D1E0'
            },
            Endpoint: ['Dot', {radius: 7}],
            PaintStyle: {
                lineWidth: 2,
                strokeStyle: 'rgb(0,0,0)'
            },
            Connector: 'Flowchart',
            Anchors: [ 'BottomMiddle', 'TopMiddle' ]
        });
    }

    return Editor;
});