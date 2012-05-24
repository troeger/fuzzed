define(['require-nodes'], function(Nodes) {
    Editor.GRID_STROKE       = '#eee';
    Editor.GRID_STROKE_WIDTH = 1;
    Editor.GRID_STROKE_STYLE = '--';
    Editor.GRID_OFFSET       = 50;

    function Editor(graphId) {
        this._initializeMember();
        this._initializeJsPlumb();
        this._layout();
        this._drawGrid();

        this._enableShapeDragAndDrop();

        // XXX: test node
        // var node = new Nodes.BasicEvent();
        // node.appendTo(this._container);
        // var node2 = new Nodes.UndevelopedEvent();
        // node2.appendTo(this._container);
    }

    Editor.prototype._initializeMember = function() {
        this._body      = jQuery('body');
        this._shapes    = this._body.find('#FuzzedShapes');
        this._container = this._body.find('#FuzzedCanvas');
        this._paper     = Raphael(this._container[0], this._body.width(), this._body.height());
    }

    Editor.prototype._initializeJsPlumb = function() {
        jsPlumb.importDefaults({
            EndpointStyle: {
                fillStyle: '#00D1E0'
            },
            Endpoint: ['Dot', {radius: 7}],
            PaintStyle: {
                lineWidth: 2,
                strokeStyle: 'black'
            },
            Connector: 'Flowchart',
            Anchors: [ 'BottomMiddle', 'TopMiddle' ]
        });
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

    Editor.prototype._drawGrid = function() {
        var height = this._container.height();
        var width  = this._container.width();

        // horizontal lines
        for (var y = Editor.GRID_OFFSET / 2; y < height; y += Editor.GRID_OFFSET) {
            this._paper.path('M0 ' + y + ' L' + width + ' ' + y)
                .attr('stroke', Editor.GRID_STROKE)
                .attr('stroke-width', Editor.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Editor.GRID_STROKE_STYLE);
        }

        // vertical lines
        for (var x = Editor.GRID_OFFSET / 2; x < width; x += Editor.GRID_OFFSET) {
            this._paper.path('M' + x + ' 0 L' + x + ' ' + height)
                .attr('stroke', Editor.GRID_STROKE)
                .attr('stroke-width', Editor.GRID_STROKE_WIDTH)
                .attr('stroke-dasharray', Editor.GRID_STROKE_STYLE);
        }
    }

    Editor.prototype._enableShapeDragAndDrop = function() {
        var _this = this;

        this._container.droppable({
            accept: '.fuzzed-node',
            tolerance: 'fit',
            drop: function(a,b,c) {
                console.log(a,b,c)
            }

        });

        this._shapes.find('.fuzzed-node').draggable({
            helper:   'clone',
            appendTo: 'body',
            revert:   'invalid'
        });
    }

    return Editor;
});