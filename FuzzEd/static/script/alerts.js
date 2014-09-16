define(['factory', 'config', 'jquery'], function(Factory, Config) {
    /**
     * Package: Base
     */

    /**
     * Function: _showAlert
     *
     * Parameters:
     *      {str} type        - The message kind identifier string. Styles the message accordingly. Should equal to one
     *                          of Bootstrap's predefined CSS classes for styling alert messages (see: Components)
     *      {str} message     - The title of the alert message. Should be a brief one liner.
     *      {str} description - Details of the given message.
     *      {int} timeout     - The time in milliseconds after which the alert shall fade out. If no timeout is given
     *                          the alert will remain active until explicitly closed by the user. A hover over the alert
     *                          box resets the timeout. This mean there is no guaranteed fade after the given time.
     */
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

    /**
     * Group: Members
     *      {Function} showAlert        - Forwarding of _showAlert. No type identifier is set.
     *      {Function} showInfoAlert    - Convenience forward of _showAlert with type set to 'danger'
     *      {Function} showErrorAlert   - Convenience forward of _showAlert with type set to 'info'
     *      {Function} showSuccessAlert - Convenience forward of _showAlert with type set to 'success'
     *      {Function} showWarningAlert - Convenience forward of _showAlert with type set to 'warning'
     */
    return {
        showAlert: _showAlert,

        showErrorAlert: function(message, description, timeout) {
            _showAlert('danger', message, description, timeout);
        },
        showInfoAlert: function(message, description, timeout) {
            _showAlert('info', message, description, timeout);
        },
        showSuccessAlert: function(message, description, timeout) {
            _showAlert('success', message, description, timeout);
        },
        showWarningAlert: function(message, description, timeout) {
            _showAlert('warning', message, description, timeout);
        }
    };
});
