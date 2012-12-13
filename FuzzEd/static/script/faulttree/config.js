define(['config'], function(Config) {
    return jQuery.extend(true, Config, {
        Events: {
            EDITOR_CALCULATE_CUTSETS: 'editor-calculate-cutsets'
        },

        IDs: {
            CUTSETS_MENU:          'FuzzEdCutsets',
            NAVBAR_ACTION_CUTSETS: 'FuzzEdNavbarActionCutsets'
        }
    });
});
