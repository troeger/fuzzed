define(['bignumber'], function(BigNumber) {
    BigNumber.MAX_VALUE = 999999999999999;
    BigNumber.MIN_VALUE = window.Number.MIN_VALUE;

    BigNumber.prototype.toFloat = function() {
        return window.parseFloat(this);
    };

    BigNumber.prototype.toInt = function() {
        return window.parseInt(this);
    };

    return BigNumber;
});
