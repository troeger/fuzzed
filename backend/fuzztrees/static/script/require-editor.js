define(['require-nodes'], function(Nodes) {

    function Editor(graphId) {
        this._initialize();
        this._layout();
        this._initializeJsPlumb();

        // XXX: test node
        var node = new Nodes.BasicEvent();
        node.appendTo(this._container);
    }

    Editor.prototype._initialize = function() {
        this._body = jQuery('body');
        this._container = this._body.find('.ui-layout-center');
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
            EndpointStyles: [
                { fillStyle: '#225588' }, 
                { fillStyle: '#225566' }
            ],
            Endpoints: [
                ['Dot', {radius: 5}], 
                ['Dot', {radius: 5}]
            ],
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