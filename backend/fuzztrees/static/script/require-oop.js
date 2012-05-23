define(function() {
    Function.prototype.Extends = function(Super) {
        if (Super.constructor != Function) {
            throw "Cannot inherit from " + Super;
        }

        this.prototype = new Super;
        this.prototype.constructor = this;
        this.prototype.Super = Super.prototype;

        return this;
    }

    return null;
});