define(['config', 'jquery'], function(Config) {

    var _progressIndicatorTimeout;
    var _progressIndicator = jQuery('#' + Config.IDs.PROGRESS_INDICATOR);
    var _progressMessage   = jQuery('#' + Config.IDs.PROGRESS_MESSAGE);

    /**
     *  Function: showProgressIndicator
     *    Display the progress indicator.
     */
    function showProgressIndicator() {
        // show indicator only if it takes longer then 500 ms
        _progressIndicatorTimeout = setTimeout(function() {
            _progressIndicator.show();
        }, 500);
    }

    /**
     *  Function: hideProgressIndicator
     *    Hides the progress indicator.
     */
    function hideProgressIndicator() {
        // prevent indicator from showing before 500 ms are passed
        clearTimeout(_progressIndicatorTimeout);
        _progressIndicator.hide();
    }

    /**
     *  Function: flashSuccessMessage
     *    Flash the success message to show that some background activity was successful.
     *
     *  Parameters:
     *    {String} message - The text that should be displayed in the progress indicator.
     */
    function flashSuccessMessage(message) {
        // only flash if not already visible and if there is a message
        if (_progressMessage.is(':hidden')) {
            _progressMessage.find('span').text(message);
            _progressMessage.find('i').removeClass().addClass('icon-ok');

            _progressMessage.fadeIn(200).delay(600).fadeOut(200);
        }
    }

    /**
     *  Function: flashAjaxSuccessMessage
     *    Flash the success message to show that the current AJAX request was successful.
     *    Use this message for binding to the jQuery ajaxSuccess event.
     *
     *  Parameters:
     *    {Event}      event - The event object for the AJAX callback (unused).
     *    {jQuery XHR} xhr   - The jQuery AJAX request object that triggered this request.
     */
    function flashAjaxSuccessMessage(event, xhr) {
        if (xhr.successMessage) {
            flashSuccessMessage(xhr.successMessage);
        }
    }

    /**
     *  Function: flashErrorMessage
     *    Flash the error message to show that the current AJAX request was unsuccessful.
     *
     *  Parameters:
     *    {String} message - The text that should be displayed in the progress indicator.
     */
    function flashErrorMessage(message) {
        _progressMessage.find('span').text(message);
        _progressMessage.find('i').removeClass().addClass('icon-warning-sign');

        _progressMessage.fadeIn(200).delay(5000).fadeOut(200);
    }

    /**
     *  Function: flashAjaxErrorMessage
     *    Flash the error message to show that the current AJAX request was unsuccessful.
     *    Use this message for binding to the jQuery ajaxError event.
     *
     *  Parameters:
     *    {Event}      event - The event object for the AJAX callback (unused).
     *    {jQuery XHR} xhr   - The jQuery AJAX request object that triggered this request.
     */
    function flashAjaxErrorMessage(event, xhr) {
        if (xhr.errorMessage) {
            flashErrorMessage(xhr.errorMessage);
        }
    }

    return {
        'showProgressIndicator': showProgressIndicator,
        'hideProgressIndicator': hideProgressIndicator,
        'flashSuccessMessage': flashSuccessMessage,
        'flashAjaxSuccessMessage': flashAjaxSuccessMessage,
        'flashErrorMessage': flashErrorMessage,
        'flashAjaxErrorMessage': flashAjaxErrorMessage
    };
});
