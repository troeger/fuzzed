define(['bignumber'], function(BigNumber) {
    /**
     * Group: Members
     *
     * Properties:
     *   {Number} MAX_VALUE - the highest representable number of big decimal
     *   {Number} MIN_VALUE - the smallest representable number of big decimal
     */
    BigNumber.MAX_VALUE = 999999999999999;
    BigNumber.MIN_VALUE = window.Number.MIN_VALUE;

    /**
     * Method: toFloat
     *
     * Converts the big decimal number to a native float.
     *
     * Returns
     *   The float representation of this number.
     */
    BigNumber.prototype.toFloat = function() {
        return window.parseFloat(this);
    };

    /**
     * Method: toInt
     *
     * Converts the big decimal number to a native float; cuts decimal places.
     *
     * Returns:
     *   The integer representation of this number.
     */
    BigNumber.prototype.toInt = function() {
        return window.parseInt(this);
    };

    return BigNumber;
});
