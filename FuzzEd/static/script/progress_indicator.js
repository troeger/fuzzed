define(['factory', 'config', 'jquery', 'underscore'], function(Factory, Config) {
    var _progressIndicatorSingle   = jQuery('#' + Config.IDs.PROGRESS_INDICATOR_SINGLE);
    var _progressIndicatorDropdown = jQuery('#' + Config.IDs.PROGRESS_INDICATOR_DROPDOWN);
    var _progressIndicatorEntry    = jQuery(_progressIndicatorSingle.html()); // copy an entry form template
    var _progressList              = {};

    /**
     *  Section: Internal
     */

    /**
     * Function: _removeEntry
     *      Reduces the counter of the progress indicator for the given watched process. If there is no observable
     *      process left, the progress indicator is removed from the list.
     *
     * Parameters:
     *      {Number} progressID - the id of the progress indicator.
     */
    var _removeEntry = function(progressID) {
        var entry = _progressList[progressID].entry;

        // if the entry is in the dropdown, we need to remove the <li> as well
        if (entry.parents('.dropdown-menu').length != 0) {
            entry.parent().remove();
        } else {
            entry.remove();
        }

        delete _progressList[progressID];
        _progressIndicatorDropdown.find('.badge').text(_.size(_progressList));

        // if there is only one entry left, display it in the single progress indicator instead
        if (_.size(_progressList) == 1) {
            var remainingEntry = _.first(_.values(_progressList)).entry;
            var listNode       = remainingEntry.parent();

            _progressIndicatorSingle.append(remainingEntry.detach());
            listNode.remove();

            _progressIndicatorDropdown.hide();
            // close the menu so that it's not open when displaying it again
            _progressIndicatorDropdown.removeClass('open');
            _progressIndicatorSingle.show();
        }
    };

    /**
     * Function: _flashMessage
     *      Flashes (display it shortly with subsequent fade) a new progress indicator for the given process id. The
     *      call can be customized to show a certain icon along with the actual message for a given flash duration.
     *
     * Parameters:
     *      {Number} progressID - the id of the progress indicator.
     *      {String} message    - the message of the progress indicator
     *      {String} iconClass  - [optional] an bootstrap or font awesome CSS class of the progress' icon
     *      {Number} delay      - delay in milliseconds for how long the message is visible
     */
    var _flashMessage = function(progressID, message, iconClass, delay) {
        if (!_progressList[progressID]) return; // there is not such active progress indicator

        // prevent the progress indicator (spinner) from showing if it's finished shortly after spawning
        clearTimeout(_progressList[progressID].timeout);

        var entry = _progressList[progressID].entry;
        // update UI
        //TODO: move the hard coded default fade time to the config
        entry.find('i').removeClass().addClass(iconClass)
            .find('span').text(message);
        if (entry.is(':hidden')) entry.fadeIn(200);

        entry.delay(delay).fadeOut(200, function() {  _removeEntry(progressID); });
    };

    /**
     *  Section: API
     */

    /**
     * Function: showProgress
     *      Creates a message in the progress indicator section of the toolbar for a given process id.
     *
     * Parameters:
     *      {Number} progressID - the id of the progress indicator.
     *      {String} message    - the message of the progress indicator
     */
    var showProgress = function(progressID, message) {
        if (_progressList[progressID]) return; //TODO: What happens with repeating requests?

        // create a new progress entry
        var entry = _progressIndicatorEntry.clone();
        entry.find('i').removeClass().addClass(Config.Classes.ICON_PROGRESS)
            .find('span').text(message)
            .hide();

        var timeout = setTimeout(function() { entry.show(); }, Config.ProgressIndicator.PROGRESS_APPEARANCE_DELAY);
        var listSize = _.size(_progressList);

        if (listSize === 0) {
            // this is the first active job
            _progressIndicatorSingle.empty().append(entry).show();
        } else if (listSize === 1) {
            // this is the second job, so we need to put both in the dropdown
            var prevEntry = _progressIndicatorSingle.children().detach();

            _progressIndicatorSingle.hide()
                .find('.dropdown-menu').append(jQuery('<li>').append(prevEntry))
                .find('.dropdown-menu').append(jQuery('<li>').append(entry))
                .find('.badge').text('2');
            _progressIndicatorDropdown.show();
        } else {
            // there is already a list in the dropdown, so append this indicator
            _progressIndicatorDropdown
                .find('.dropdown-menu').append(jQuery('<li>').append(entry))
                .find('.badge').text(_.size(_progressList) + 1);
        }

        // remember the new entry for later reference
        _progressList[progressID] = {
            timeout: timeout,
            entry:   entry
        }
    };

    /**
     * Function: flashSuccessMessage
     *      Forward to <_flashMessage> with a default success icon and delay.
     *
     * Parameters:
     *      {Number} progressID - the id of the progress indicator.
     *      {String} message    - the message of the progress indicator
     */
    var flashSuccessMessage = function(progressID, message) {
        _flashMessage(progressID, message, Config.Classes.ICON_SUCCESS, Config.ProgressIndicator.SUCCESS_FLASH_DELAY);
    };

    /**
     * Function: flashSuccessMessage
     *      Forward to <_flashMessage> with a default error icon and delay.
     *
     * Parameters:
     *      {Number} progressID - the id of the progress indicator.
     *      {String} message    - the message of the progress indicator
     */
    var flashErrorMessage = function(progressID, message) {
        _flashMessage(progressID, message, Config.Classes.ICON_ERROR, Config.ProgressIndicator.ERROR_FLASH_DELAY);
        // if the erroneous entry is in the dropdown, show the dropdown menu
        if (!_progressIndicatorDropdown.is(':hidden')) {
            _progressIndicatorDropdown.addClass('open');
        }
    };

    /**
     *  Section: AJAX
     */

    /**
     * Function: showAjaxProgress
     *      The AJAX request version of <showProgress> with a setup default progress message.
     *
     * Parameters:
     *      {Event}          event - a jQuery event object originating from the AJAX request
     *      {XMLHTTPRequest} xhr   - the actual XHR object of the browser
     */
    var showAjaxProgress = function(event, xhr) {
        // assign an ID for later reference
        xhr.progressID = _.uniqueId('progress_');
        showProgress(xhr.progressID, xhr.progressMessage || Config.ProgressIndicator.DEFAULT_PROGRESS_MESSAGE);
    };

    /**
     * Function: flashAjaxSuccessMessage
     *      The AJAX request version of <flashSuccessMessage> with a setup default success message.
     *
     * Parameters:
     *      {Event}          event - a jQuery event object originating from the AJAX request
     *      {XMLHTTPRequest} xhr   - the actual XHR object of the browser
     */
    var flashAjaxSuccessMessage = function(event, xhr) {
        flashSuccessMessage(xhr.progressID, xhr.progressSuccessMessage || Config.ProgressIndicator.DEFAULT_SUCCESS_MESSAGE);
    };


    /**
     * Function: flashAjaxErrorMessage
     *      The AJAX request version of <flashErrorMessage> with a setup default error message.
     *
     * Parameters:
     *      {Event}          event - a jQuery event object originating from the AJAX request
     *      {XMLHTTPRequest} xhr   - the actual XHR object of the browser
     */
    var flashAjaxErrorMessage = function(event, xhr) {
        flashErrorMessage(xhr.progressID, xhr.progressErrorMessage || Config.ProgressIndicator.DEFAULT_ERROR_MESSAGE);
    };

    return {
        showProgress:            showProgress,
        flashSuccessMessage:     flashSuccessMessage,
        flashErrorMessage:       flashErrorMessage,

        showAjaxProgress:        showAjaxProgress,
        flashAjaxSuccessMessage: flashAjaxSuccessMessage,
        flashAjaxErrorMessage:   flashAjaxErrorMessage
    };
});
