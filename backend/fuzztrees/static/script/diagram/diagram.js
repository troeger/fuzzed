define(["JQUERY_HOME/require-jquery", "JIT_HOME/require-jit", "FUZZED_HOME/nodes/nodes"], function(jQuery, $jit, Nodes) {
    // Static diagram properties
    Diagram.BACKEND_URL    = "/api/json";
    Diagram.CONTAINER      = "fuzzed-editor";
    Diagram.HEIGHT         = jQuery(window).height() - jQuery("#fuzzed-toolbar").height();
    Diagram.WIDTH          = jQuery(window).width();

    Diagram.ORIENTATION    = "top";
    Diagram.SUBTREE_OFFSET = 10;
    Diagram.SIBLING_OFFSET = 10;
    Diagram.ANIMATION_MSEC = 500;
    Diagram.TRANSITION     = $jit.Trans.Expo.easeOut;

    // Static edge properties of the diagram
    Diagram.EDGE           = {};
    Diagram.EDGE.TYPE      = "line";
    Diagram.EDGE.COLOR     = "#000";
    Diagram.EDGE.WIDTH     = 1;

    function Diagram() {
        this._spaceTree = null;
        this._loadDiagram();
    }

    Diagram.prototype._loadDiagram = function() {
        jQuery.ajax(Diagram.BACKEND_URL, {
            type     : "GET",
            dataType : "json",
            success  : this._drawDiagram,
            error    : this._loadFailed
        });
    }

    Diagram.prototype._loadFailed = function(xhr, status, error) {
        console.log("Could not connect to", Diagram.BACKEND_URL, "reason is:", status, typeof(error) !== "undefined" ? error : "");
        throw "Failed to load model";
    }

    Diagram.prototype._drawDiagram = function(tree) {
        this._spaceTree = new $jit.ST({
            // canvas
            injectInto          : Diagram.CONTAINER,
            width               : Diagram.WIDTH,
            height              : Diagram.HEIGHT,

            // tree
            orientation         : Diagram.ORIENTATION,
            subtreeOffset       : Diagram.SUBTREE_OFFSET,
            siblingOffset       : Diagram.SIBLING_OFFSET,

            // animation
            duration            : Diagram.ANIMATION_MSEC,
            transition          : Diagram.TRANSITION,

            // node
            Node                : {
                type            : Nodes.TYPE,
                width           : Nodes.WIDTH,
                height          : Nodes.HEIGHT,
                color           : Nodes.COLOR,
                overridable     : true
            },

            // edge
            Edge                : {
                type            : Diagram.EDGE.TYPE,
                color           : Diagram.EDGE.COLOR,
                lineWidth       : Diagram.EDGE.WIDTH,
                overridable     : true
            },

            // navigation
            Navigation          : {
                enable          : true,
                panning         : true,
                zooming         : true
            },

            onCreateLabel: function(domElement, node) {
                var element = jQuery(domElement);

                element.width(Nodes.WIDTH);
                element.height(Nodes.HEIGHT);
                element.html(node.name);
            }
        });
        tree = {
            id   : 1,
            name : "TOP",
            data : {
                type : "event"
            },
            children : [{
                id   : 2,
                name : "CPU",
                data : {
                    type : "other"
                }
            }, {
                id   : 3,
                name : "FAN",
                data : {
                    type : "rofl"
                }
            }]
        };

        with (this._spaceTree) {
            loadJSON(tree);
            compute();
            onClick(this._spaceTree.root);
        }
    }

    return Diagram;
});