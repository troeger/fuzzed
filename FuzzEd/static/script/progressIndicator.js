define(['config', 'jquery', 'underscore'], function(Config) {

    var _progressIndicatorSingle   = jQuery('#' + Config.IDs.PROGRESS_INDICATOR_SINGLE);
    var _progressIndicatorDropdown = jQuery('#' + Config.IDs.PROGRESS_INDICATOR_DROPDOWN);
    var _progressIndicatorEntry    = jQuery(_progressIndicatorSingle.html()); // copy an entry form template

    var _progressList = {};


    /**
     *  Section: API
     */

    function showProgress(progressID, message) {
        if (_progressList[progressID]) return; //TODO: What happens with repeating requests?

        // create a new progress entry
        var entry = _progressIndicatorEntry.clone();
        entry.find('i').removeClass().addClass(Config.Classes.ICON_PROGRESS);
        entry.find('span').text(message);
        entry.hide();
        var timeout = setTimeout(function() {
            entry.show();
        }, Config.ProgressIndicator.PROGRESS_APPEARANCE_DELAY);

        if (_.size(_progressList) == 0) {
            // this is the first active job
            _progressIndicatorSingle.empty().append(entry);
            _progressIndicatorSingle.show();
        } else if (_.size(_progressList) == 1) {
            // this is the second job, so we need to put both in the dropdown
            var prevEntry = _progressIndicatorSingle.children().detach();
            _progressIndicatorSingle.hide();

            _progressIndicatorDropdown.find('.dropdown-menu').append(jQuery('<li>').append(prevEntry));
            _progressIndicatorDropdown.find('.dropdown-menu').append(jQuery('<li>').append(entry));
            _progressIndicatorDropdown.find('.badge').text('2');
            _progressIndicatorDropdown.show();
        } else {
            // there is already a list in the dropdown, so append this indicator
            _progressIndicatorDropdown.find('.dropdown-menu').append(jQuery('<li>').append(entry));
            _progressIndicatorDropdown.find('.badge').text(_.size(_progressList) + 1);
        }

        // remember the new entry for later reference
        _progressList[progressID] = {
            'timeout': timeout,
            'entry': entry
        }
    }

    function flashSuccessMessage(progressID, message) {
        _flashMessage(progressID, message, Config.Classes.ICON_SUCCESS, Config.ProgressIndicator.SUCCESS_FLASH_DELAY);
    }

    function flashErrorMessage(progressID, message) {
        _flashMessage(progressID, message, Config.Classes.ICON_ERROR, Config.ProgressIndicator.ERROR_FLASH_DELAY);
        // if the erroneous entry is in the dropdown, show the dropdown menu
        if (!_progressIndicatorDropdown.is(':hidden')) {
            _progressIndicatorDropdown.find('.dropdown-menu').show();
        }
    }

    /**
     *  Section: AJAX
     */

    function showAjaxProgress(event, xhr) {
        // assign an ID for later reference
        xhr.progressID = _.uniqueId('progress_');

        showProgress(xhr.progressID, xhr.progressMessage || Config.ProgressIndicator.DEFAULT_PROGRESS_MESSAGE);
    }

    function flashAjaxSuccessMessage(event, xhr) {
        flashSuccessMessage(xhr.progressID, xhr.progressSuccessMessage || Config.ProgressIndicator.DEFAULT_SUCCESS_MESSAGE);
    }

    function flashAjaxErrorMessage(event, xhr) {
        flashErrorMessage(xhr.progressID, xhr.progressErrorMessage || Config.ProgressIndicator.DEFAULT_ERROR_MESSAGE);
    }


    /**
     *  Section: Internal
     */

    function _flashMessage(progressID, message, iconClass, delay) {
        if (!_progressList[progressID]) return; // there is not such active progress indicator

        // prevent the progress indicator (spinner) from showing if it's finished shortly after spawning
        clearTimeout(_progressList[progressID].timeout);

        var entry = _progressList[progressID].entry;
        // update UI
        entry.find('i').removeClass().addClass(iconClass);
        entry.find('span').text(message);
        if (entry.is(':hidden')) entry.fadeIn(200);

        entry.delay(delay).fadeOut(200, function() {
            _removeEntry(progressID);
        });
    }

    function _removeEntry(progressID) {
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
            var listNode = remainingEntry.parent();

            _progressIndicatorSingle.append(remainingEntry.detach());
            listNode.remove();

            _progressIndicatorDropdown.hide();
            _progressIndicatorSingle.show();
        }
    }


    return {
        'showProgress': showProgress,
        'flashSuccessMessage': flashSuccessMessage,
        'flashErrorMessage': flashErrorMessage,
        'showAjaxProgress': showAjaxProgress,
        'flashAjaxSuccessMessage': flashAjaxSuccessMessage,
        'flashAjaxErrorMessage': flashAjaxErrorMessage
    };
});
