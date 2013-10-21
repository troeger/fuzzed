define(['config', 'jquery'], function(Config) {

    var _progressIndicatorTimeout;
    var _progressIndicator = jQuery('#' + Config.IDs.PROGRESS_INDICATOR);
    var _progressMessage   = jQuery('#' + Config.IDs.PROGRESS_MESSAGE);

    /**
     *  Function: showProgressIndicator
     *    Display the progress indicator.
     *
     *  Returns:
     *    This Editor instance for chaining.
     */
    function showProgressIndicator() {
        // show indicator only if it takes longer then 500 ms
        _progressIndicatorTimeout = setTimeout(function() {
            _progressIndicator.show();
        }.bind(this), 500);

        return this;
    }

    /**
     *  Function: hideProgressIndicator
     *    Hides the progress indicator.
     *
     *  Returns:
     *    This Editor instance for chaining.
     */
    function hideProgressIndicator() {
        // prevent indicator from showing before 500 ms are passed
        clearTimeout(_progressIndicatorTimeout);
        _progressIndicator.hide();

        return this;
    }

    /**
     *  Function: flashSuccessMessage
     *    Flash the success message to show that the current AJAX request was successful.
     *
     *  Parameters:
     *    {Event}      event - The event object for the AJAX callback (unused).
     *    {jQuery XHR} xhr   - The jQuery AJAX request object that triggered this request.
     *
     *  Returns:
     *    This Editor instance for chaining.
     */
    function flashSuccessMessage(event, xhr) {
        // only flash if not already visible and if there is a message
        if (_progressMessage.is(':hidden') && xhr.successMessage) {
            _progressMessage.find('span').text(xhr.successMessage);
            _progressMessage.find('i').removeClass().addClass('icon-ok');

            _progressMessage.fadeIn(200).delay(600).fadeOut(200);
        }

        return this;
    }

    /**
     *  Function: flashErrorMessage
     *    Flash the error message to show that the current AJAX request was unsuccessful.
     *
     *  Parameters:
     *    {Event}      event - The event object for the AJAX callback (unused).
     *    {jQuery XHR} xhr   - The jQuery AJAX request object that triggered this request.
     *
     *  Returns:
     *    This Editor instance for chaining.
     */
    function flashErrorMessage(event, xhr) {
        // only flash if there is a message
        if (xhr.errorMessage) {
            _progressMessage.find('span').text(xhr.errorMessage);
            _progressMessage.find('i').removeClass().addClass('icon-warning-sign');

            _progressMessage.fadeIn(200).delay(5000).fadeOut(200);
        }

        return this;
    }


    return {
        'showProgressIndicator': showProgressIndicator,
        'hideProgressIndicator': hideProgressIndicator,
        'flashSuccessMessage': flashSuccessMessage,
        'flashErrorMessage': flashErrorMessage
    };
});
