define(['config', 'jquery'], function(Config) {
    /**
     *  Package: DFD
     */

    /**
     *  Structure: DFDConfig
     *    Nothing special yet.
     *
     *  Extends: <Base::Config>
     */
    return jQuery.extend(true, Config, {
        JSPlumb: {
            CONNECTOR_STYLE:        'Bezier',
            CONNECTOR_OPTIONS:      { curviness: 10},
            
            CONNECTION_OVERLAYS:    [[ "Arrow", { width:10, length:10, location:1, id:"arrow" } ]],
        
            OUTLINE_COLOR:          'white',
            OUTLINE_WIDTH:          2,
        }
    });
});
