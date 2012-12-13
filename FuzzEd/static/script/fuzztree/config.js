define(['faulttree/config'], function(FaulttreeConfig) {
    return jQuery.extend(true, FaulttreeConfig, {
        Classes: {
            NODE_OPTIONAL_INDICATOR: 'fuzzed-node-optional-indicator'
        },

        Node: {
            OPTIONAL_INDICATOR_FILL:   '#FFF',
            OPTIONAL_INDICATOR_RADIUS: Math.round(FaulttreeConfig.Grid.SIZE / 10),
            OPTIONAL_INDICATOR_STROKE: 2
        }
    });
});
