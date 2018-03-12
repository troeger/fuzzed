define(['factory', 'config', 'jquery'], function(Factory, Config) {
    /**
     * Package: DFD
     */

    /**
     * Structure: DFDConfig
     *      Changes the default rectangular tree style of edges to the slight half moons of DFDs.
     *
     *      Extends: <Base::Config>
     */
    return jQuery.extend(true, Config, {
        JSPlumb: {
            CONNECTOR_STYLE:     'Bezier',
            CONNECTOR_OPTIONS:   { curviness: 10},
            
            CONNECTION_OVERLAYS: [[ 'Arrow', { width:10, length:10, location:1, id:'arrow' } ]],
        
            OUTLINE_COLOR:       'white',
            OUTLINE_WIDTH:       2
        },

        IDs: {
            ACTION_GROUP:        'FuzzEdActionGroup',
            ACTION_UNGROUP:      'FuzzEdActionUngroup'
        }
    });
});
