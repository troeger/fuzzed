define(['faulttree/config', 'node'], function(Config, AbstractNode) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNode
     *
     * Tiny class introduced for clearer typing and to adjust config to <Faultree::Config>.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        getConfig: function() {
            return Config;
        }
    });
});
