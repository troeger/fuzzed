require.config({
    waitSeconds : 5,
    paths       : {
        JQUERY_HOME : "lib/jquery-ui",
        JIT_HOME    : "lib/jit/"
    }
})

require(["JQUERY_HOME/require-jquery", "JIT_HOME/require-jit"], function(jQuery, $jit) {
    var $ = jQuery;

    jQuery(document).ready(function() {
        var jqxhr = jQuery.getJSON("/api/json/", function(data) {
            var st = new $jit.ST({
                injectInto: 'editor',
                duration: 800,
                transition: $jit.Trans.Quart.easeInOut,
                levelDistance: 50,
                Node: {
                    height: 20,
                    width: 60,
                    type: 'rectangle',
                    color: 'yellow',
                    overridable: true
                },
                Edge: {
                    type: 'bezier',
                    overridable: true
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
            st.loadJSON(data);
            st.compute();
            st.geom.translate(new $jit.Complex(-200, 0), "current");
            st.onClick(st.root);
        }).error(function(xhr, status) { /*alert("Error"); alert(xhr.status);*/ alert(status) })
    });
});