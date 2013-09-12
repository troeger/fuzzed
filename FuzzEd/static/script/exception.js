function NetworkError(message) {
    Error.apply(this, arguments);
    this.name = 'NetworkError';
}
NetworkError.prototype = Error.prototype;

function SubclassResponsibility(message) {
    Error.apply(this, arguments);
    this.name = 'SubclassResponsibility';
}
SubclassResponsibility.prototype = Error.prototype;

var BuiltinTypeError = TypeError;
function TypeError(expectedOrMessage, got) {
    if (typeof got !== 'undefined') {
        BuiltinTypeError.apply(this, ['got "' + expectedOrMessage + '", expected "' + got '"']);
    } else {
        BuiltinTypeError.apply(this, arguments);
    }
}
TypeError.prototype = BuiltinTypeError;

function ValueError(expectedOrMessage, got) {
    if (typeof got !== 'undefined')
        Error.apply(this, ['got "' + expectedOrMessage + '", expected "' + got + '"']);
    else
        Error.apply(this, arguments);
    this.name = 'ValueError';
}
ValueError.prototype = Error.prototype;

function Warning(message) {
    Error.apply(this, arguments);
    this.name = 'Warning';
}
Warning.prototype = Error.Prototype;
