define(["JQUERY_HOME/require-jquery", "JIT_HOME/require-jit"], function(jQuery, $jit) {
    var headline = jQuery("#headline");

    // Static diagram properties
    Diagram.BACKEND_URL    = "/api/json";
    Diagram.CONTAINER      = "editor";
    Diagram.HEIGHT         = jQuery(window).height() - headline.offset().top - headline.height();
    Diagram.WIDTH          = jQuery(document).width();
    Diagram.SUBTREE_OFFSET = 10;
    Diagram.SIBLING_OFFSET = 10;
    Diagram.ANIMATION_MSEC = 500;

    // Static node properties of the diagram
    Diagram.NODE           = {};
    Diagram.NODE.TYPE      = "rectangle";
    Diagram.NODE.HEIGHT    = 50;
    Diagram.NODE.WIDTH     = 100;
    Diagram.NODE.COLOR     = "#d00";

    // Static edge properties of the diagram
    Diagram.EDGE           = {};
    Diagram.EDGE.TYPE      = "line";
    Diagram.EDGE.COLOR     = "#000";

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
            injectInto      : Diagram.CONTAINER,
            width           : Diagram.WIDTH,
            height          : Diagram.HEIGHT,

            // tree
            orientation     : "top",
            subtreeOffset   : Diagram.SUBTREE_OFFSET,
            siblingOffset   : Diagram.SIBLING_OFFSET,

            // animation
            duration        : Diagram.ANIMATION_MSEC,
            transition      : $jit.Trans.Expo.easeOut,

            // node
            Node            : {
                type        : Diagram.NODE.TYPE,
                width       : Diagram.NODE.WIDTH,
                height      : Diagram.NODE.HEIGHT,
                color       : Diagram.NODE.COLOR,
                overridable : true
            },

            // edge
            Edge            : {
                type        : Diagram.EDGE.TYPE,
                color       : Diagram.EDGE.COLOR,
                overridable : true
            },

            // navigation
            Navigation      : {
                enable      : true,
                panning     : true,
                zooming     : true
            },

            onCreateLabel: function(label, node){
                label.id = node.id;            
                label.innerHTML = node.name;
                label.onclick = function(){
                    if(normal.checked) {
                      st.onClick(node.id);
                    } else {
                    st.setRoot(node.id, 'animate');
                    }
                };
                //set label styles
                var style = label.style;
                style.width = 60 + 'px';
                style.height = 20 + 'px';            
                style.cursor = 'pointer';
                style.color = 'black';
                style.fontSize = '0.8em';
                style.textAlign= 'center';
                style.paddingTop = '3px';
            }
        });

        with (this._spaceTree) {
            loadJSON(tree);
            compute();
            onClick(this._spaceTree.root);
        }
    }

    return Diagram;
});