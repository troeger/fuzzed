define(['config', 'jquery'], function(Config) {

    function _showAlert(type, message, description, timeout) {
        var typeClass = type == 'warning' ? '' : 'alert-' + type;
        var dom = jQuery('<div class="fade in alert ' + typeClass + '"> \
                              <a class="close" data-dismiss="alert" href="#">&times;</a> \
                              <strong>' + message + '</strong> ' + description +
                         '</div>');
        jQuery('#' + Config.IDs.ALERT_CONTAINER).append(dom);

        if (typeof timeout !== 'undefined') {
            function fadeOut() {
                dom.alert('close');
            }
            var activeTimeout = setTimeout(fadeOut, timeout);

            // prevent alert from vanishing when hovering with mouse
            dom.hover(
                // in
                function() {
                    clearTimeout(activeTimeout);
                },
                // out
                function() {
                    activeTimeout = setTimeout(fadeOut, timeout)
                }
            );
        }
    }

    return {
        showAlert: _showAlert,
        showWarningAlert: function(message, description, timeout) {
            _showAlert('warning', message, description, timeout);
        },
        showErrorAlert: function(message, description, timeout) {
            _showAlert('danger', message, description, timeout);
        },
        showSuccessAlert: function(message, description, timeout) {
            _showAlert('success', message, description, timeout);
        },
        showInfoAlert: function(message, description, timeout) {
            _showAlert('info', message, description, timeout);
        }
    };
});
