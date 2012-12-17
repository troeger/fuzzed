define(['faulttree/config', 'node'], function(Config, AbstractNode) {

    /**
     *  Concrete faulttree implementation
     */
    return AbstractNode.extend({
        getConfig: function() {
            return Config;
        }
    });
});
