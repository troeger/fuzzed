require.config({
    waitSeconds : 5,
    paths       : {
        JQUERY_HOME : "lib/jquery-ui/",
        JIT_HOME    : "lib/jit/",
        FUZZED_HOME : "script/"
    }
})

require(["JQUERY_HOME/require-jquery", "FUZZED_HOME/require-fuzzed"], function(jQuery, FuzzEd) {
    jQuery(document).ready(function() {
        var Diagram = new FuzzEd.Diagram();
    });
});