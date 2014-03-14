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
            CONNECTOR_STYLE: 'StateMachine'
        }
    });
});
