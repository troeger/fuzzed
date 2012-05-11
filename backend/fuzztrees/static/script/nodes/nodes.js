define(["JQUERY_HOME/require-jquery", "JIT_HOME/require-jit"], function(jQuery, $jit) {
    Nodes.TYPE   = "fuzzed";
    Nodes.WIDTH  = 120;
    Nodes.HEIGHT = 50;
    Nodes.COLOR  = "transparent";

    $jit.ST.Plot.NodeTypes.implement({
        fuzzed : {
            render : function(node, canvas) {
                var context = canvas.canvases[0].canvas.getContext('2d');
                context.fillStyle = "#f00";
                context.fillRect(-1 * Nodes.WIDTH / 2 + node.pos.x, -1 * Nodes.HEIGHT / 2 + node.pos.y, Nodes.WIDTH, Nodes.HEIGHT);
            }
        }
    })

    function Nodes() {}

    return Nodes;
});