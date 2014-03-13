define(['dfd/config', 'node'], function(Config, AbstractNode) {
    /**
     * Package: DFD
     */

    /**
     * Class: DfdNode
     *
     * Tiny class introduced for clearer typing and to adjust config to <DFD::Config>.
     *
     * Extends: <Base::Node>
     */
    return AbstractNode.extend({
        getConfig: function() {
            return Config;
        }
    });
});