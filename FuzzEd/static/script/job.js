define(['class', 'config', 'progressIndicator', 'jquery'], function(Class, Config, Progress) {

    /**
     *  Class: Job
     *    Wrapper that simplifies continuous querying of a backend job.
     */
    return Class.extend({

        /**
         *  Group: Members
         *
         *  Properties:
         *    {Function}    successCallback    - Function that is called as soon as the job is finished.
         *    {Function}    updateCallback     - Function that is called each time the job progress is queried and
         *                                       the job progress is reported back as 'not finished'.
         *    {Function}    errorCallback      - Function that is called if the resource was not found.
         *    {Function}    errorCallback      - Function that is called if the job results in an error.
         *    {int}         queryInterval      - The interval (in ms) between job queries.
         *    {String}      _url               - The query URL of this job.
         *    {Timeout)     _timeout           - A reference to the current job query timeout.
         */
        successCallback:  jQuery.noop,
        updateCallback:   jQuery.noop,
        notFoundCallback: jQuery.noop,
        errorCallback:    jQuery.noop,
        queryInterval:    1000,
        progressMessage:          Config.ProgressIndicator.DEFAULT_PROGRESS_MESSAGE,
        progressSuccessMessage:   Config.ProgressIndicator.DEFAULT_SUCCESS_MESSAGE,
        progressErrorMessage:     Config.ProgressIndicator.DEFAULT_ERROR_MESSAGE,
        progressNotFoundMessage:  Config.ProgressIndicator.DEFAULT_NOT_FOUND_MESSAGE,
        progressID:      undefined,

        _url:             undefined,
        _timeout:         undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Constructor for this Job instance.
         *
         *  Parameters:
         *    {String} url - The query URL of this job.
         */
        init: function(url) {
            this._url = url;
            this.progressID = _.uniqueId("job_")
        },

        /**
         *  Group: Actions
         */

        /**
         *  Method: start
         *    Start querying this Job.
         */
        start: function() {
            this._query();
        },

        /**
         *  Method: cancel
         *    Tell the backend to cancel this job. This will result in the error callback getting called the next
         *    time this Job is queried.
         */
        cancel: function() {
            clearTimeout(this._timeout);
            Progress.flashErrorMessage(this.progressID, Config.ProgressIndicator.DEFAULT_CANCELED_MESSAGE);
            //TODO: call backend as soon as the call is available
        },

        /**
         *  Group: Internal
         */

        /**
         *  Method: _query
         *    Fetch the Job's status from the backend using AJAX and call the callback corresponding to the result.
         *    In case the Job is not finished, set a timeout for the next query.
         */
        _query: function() {
            jQuery.ajax({
                url: this._url,
                // we do the progress indication manually so we don't want the global AJAX handlers to trigger here
                global: false,
                beforeSend: function() {
                    Progress.showProgress(this.progressID, this.progressMessage)
                }.bind(this),
                statusCode: {
                    200: function(data) { // success
                        Progress.flashSuccessMessage(this.progressID, this.progressSuccessMessage);
                        this.successCallback(data);
                    }.bind(this),

                    202: function(data) { // not finished
                        //TODO: update progress indicator?
                        this.updateCallback(data);
                        // query again later
                        this._timeout = setTimeout(this._query.bind(this), this.queryInterval);
                    }.bind(this),

                    404: function() { // not found / canceled
                        Progress.flashErrorMessage(this.progressID, this.progressNotFoundMessage);
                        this.notFoundCallback();
                    }.bind(this)
                },
                error: function(xhr) {
                    Progress.flashErrorMessage(this.progressID, this.progressErrorMessage);
                    this.errorCallback(arguments);
                }.bind(this)
            });
        }

    });
});
