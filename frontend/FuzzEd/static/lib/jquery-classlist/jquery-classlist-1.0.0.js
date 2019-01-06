/**
 *  Found at: https://gist.github.com/raybellis/5115997
 */

/*global jQuery */
;(function($) {

	/*global document */
	"use strict";

	if (typeof document !== 'undefined' && ('classList' in document.createElement('a'))) {

		var $ = jQuery;

		var _addClass = $.fn.addClass;
		var _removeClass = $.fn.removeClass;

		$.fn.hasClass = function(selector) {
			var elem, i, l;
			for (i = 0, l = this.length ; i < l; ++i) {
				elem = this[i];

                // for certain nodes that do not have classList (SVG in Safari -.-)
                if (typeof elem.classList === 'undefined') {
                    var classAttr = elem.getAttribute('class') || '';
                    var regex = new RegExp('(^|\\s+)' + selector + '(\\s+|$)');

                    return classAttr.search(regex) != -1;
                }

				if (elem.nodeType === 1 && elem.classList.contains(selector)) {
					return true;
				}
			}
			return false;
		};

		$.fn.addClass = function(value) {
			var elem, i, l;	
			if (typeof value === 'string' && value && value.indexOf(' ') < 0) {
				for (i = 0, l = this.length ; i < l; ++i) {
					elem = this[i];
					if (elem.nodeType === 1) {

                        // for certain nodes that do not have classList (SVG in Safari -.-)
                        if (typeof elem.classList === 'undefined') {
                            var classAttr = elem.getAttribute('class') || '';
                            var regex = new RegExp('(^|\\s+)' + value + '(\\s+|$)');

                            if (classAttr.search(regex) == -1) {
                                elem.setAttribute('class', (classAttr + ' ' + value).trim());
                            }
                        } else {
						    elem.classList.add(value);
                        }
					}
				}
			} else {
				_addClass.apply(this, arguments);
			}
			return this;
		};

		$.fn.removeClass = function(value) {
			var elem, i, l;	
			if (typeof value === 'string' && value && value.indexOf(' ') < 0) {
				for (i = 0, l = this.length ; i < l; ++i) {
					elem = this[i];
					if (elem.nodeType === 1) {

                        // for certain nodes that do not have classList (SVG in Safari -.-)
                        if (typeof elem.classList === 'undefined') {
                            var classAttr = elem.getAttribute('class') || '';

                            var regex = new RegExp('(^|\\s+)' + value + '(\\s+|$)');
                            elem.setAttribute('class', classAttr.replace(regex, ' ').trim());
                        } else {
						    elem.classList.remove(value);
                        }
					}
				}
			} else {
				_removeClass.apply(this, arguments);
			}
			return this;
		};
	}

})(jQuery);
