define(['factory', 'class', 'config', 'progress_indicator', 'jquery'], function(Factory, Class, Config, Progress) {
    /**
     * Package: Base
     */

    /**
     * Class: Job
     *      Wrapper that simplifies continuous querying of a backend job.
     */
    return Class.extend({
        /**
         * Group: Members
         *      {Function}    successCallback    - Function that is called as soon as the job is finished.
         *      {Function}    updateCallback     - Function that is called each time the job progress is queried and
         *                                         the job progress is reported back as 'not finished'.
         *      {Function}    errorCallback      - Function that is called if the resource was not found.
         *      {Function}    errorCallback      - Function that is called if the job results in an error.
         *      {Number}      queryInterval      - The interval (in ms) between job queries.
         *      {String}      _url               - The query URL of this job.
         *      {Timeout)     _timeout           - A reference to the current job query timeout.
         */
        successCallback:  jQuery.noop,
        updateCallback:   jQuery.noop,
        notFoundCallback: jQuery.noop,
        errorCallback:    jQuery.noop,
        queryInterval:    1000,
        progressMessage:          Factory.getModule('Config').ProgressIndicator.DEFAULT_PROGRESS_MESSAGE,
        progressSuccessMessage:   Factory.getModule('Config').ProgressIndicator.DEFAULT_SUCCESS_MESSAGE,
        progressErrorMessage:     Factory.getModule('Config').ProgressIndicator.DEFAULT_ERROR_MESSAGE,
        progressNotFoundMessage:  Factory.getModule('Config').ProgressIndicator.DEFAULT_NOT_FOUND_MESSAGE,
        progressID:      undefined,

        _url:             undefined,
        _timeout:         undefined,
        _refetch:         true,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         * Parameters:
         *      {String} url - The query URL of this job.
         */
        init: function(url) {
            this._url = url;
            this.progressID = _.uniqueId("job_")
        },

        /**
         * Group: Actions
         */

        /**
         * Method: start
         *      Start querying this Job.
         *
         * Returns:
         *      This {<Job>} instance for chaining.
         */
        start: function() {
            this._query();

            return this;
        },

        /**
         *  Method: cancel
         *      Tell the backend to cancel this job. This will result in the error callback getting called the next
         *      time this Job is queried.
         *
         *  Returns:
         *      This {<Job>} instance for chaining.
         */
        cancel: function() {
            clearTimeout(this._timeout);
            // prevent re-fetches due to race conditions
            this._refetch = false;
            Progress.flashErrorMessage(this.progressID, Factory.getModule('Config').ProgressIndicator.DEFAULT_CANCELED_MESSAGE);
            //TODO: call backend as soon as the call is available (cancel method for backend job not yet )

            return this;
        },

        /**
         * Group: Internal
         */

        /**
         * Method: _query
         *      Fetch the Job's status from the backend using AJAX and call the callback corresponding to the result.
         *      In case the Job is not finished, set a timeout for the next query.
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
                    200: function(data, status, req) { // success
                        Progress.flashSuccessMessage(this.progressID, this.progressSuccessMessage);
                        
                        job_result_url = req.getResponseHeader('location');
                        
                        this.successCallback(data, job_result_url);

                    }.bind(this),

                    202: function(data) { // not finished
                        //TODO: update progress indicator?
                        this.updateCallback(data);
                        // query again later
                        if (this._refetch) {
                            this._timeout = setTimeout(this._query.bind(this), this.queryInterval);
                        }
                    }.bind(this),

                    404: function() { // not found / canceled
                        Progress.flashErrorMessage(this.progressID, this.progressNotFoundMessage);
                        this.notFoundCallback.apply(this, arguments);
                    }.bind(this)
                },
                error: function(xhr) {
                    // 404 is caught separately
                    if (xhr.status == 404) return;
                    
                    Progress.flashErrorMessage(this.progressID, this.progressErrorMessage);
                    this.errorCallback.apply(this, arguments);
                }.bind(this)
            });
        }
    });
});
