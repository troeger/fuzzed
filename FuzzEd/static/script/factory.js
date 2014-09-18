define(['class', 'json!notations/dfd.json', 'json!notations/faulttree.json', 'json!notations/fuzztree.json',
    'json!notations/rbd.json'],
function(Class, DFDNotation, FaulttreeNotation, FuzztreeNotation, RBDNotation) {
    /**
     *  Package: Base
     */

    /**
     *  Class: Factory
     *
     * The factory class acts as an object factory for almost all classes. It is based on the desired class layout of
     * the whole client side JavaScript code, which dynamically replaces abstract classes with its concrete children
     * when possible. An abstract Editor for example uses the factory to create a concrete graph instead of the abstract
     * graph (every concrete graph inherits from). To achieve this, you generally have to call
     *     Factory.create('MyAbstractClass', arg1, arg2, ...);
     * instead of calling the constructor on your own. This allows the factory to determine the right subclass and
     * its constructor. It will then call the constructor with the given arguments and return the object to you. The
     * only thing you have to take care of is importing the desired require-modules for a specific graph type into its
     * editor (by define([..., 'foo/bar', ...]))
     */
    var Factory = Class.extend({
        kind: undefined,
        // create's first argument is either the name of the base class or a constructor, we want to create an instance of
        //  all other arguments are passed directly into the  constructor
        create: function(baseCls) {
            // arguments is just an "array-like" object, not an actual array, so we have to convert it into an actual array
            var args = Array.prototype.slice.call(arguments);

            // if baseCls already is a constructor and not a string describing the desired class
            if (typeof baseCls === 'function') {
                //console.log('[-] Creating a ' + baseCls + ' directly from given constructor.')
                creation = this._construct(baseCls, args.slice(1));
            } else {
            // if baseCls is a string describing the desired class (most common case)
                var resolveObj = this._resolveClassName(baseCls);
                var path = resolveObj.path;
                var clsModule = require(path);

                var creation = undefined;

                // our first try is based on the assumption, that the class module only returns the class constructor
                if (typeof clsModule           !== 'undefined'
                 && typeof clsModule.prototype !== 'undefined') {
                    creation = this._construct(clsModule, args.slice(1));

                // our second try supposes that the constructor is a member of the return object and is called the same
                //  as the concrete class we are looking for (e.g. FaulttreeNodeGroup)
                } else if (typeof clsModule[resolveObj.fullClassName]           !== 'undefined'
                        && typeof clsModule[resolveObj.fullClassName].prototype !== 'undefined') {
                    creation = this._construct(clsModule[resolveObj.fullClassName], args.slice(1));

                // our third try is to find the wanted class inside the found package, but this time named as the
                //  baseCls (e.g. NodeGroup)
                } else if (typeof clsModule[resolveObj.cls]           !== 'undefined'
                        && typeof clsModule[resolveObj.cls].prototype !== 'undefined') {
                    creation = this._construct(clsModule[resolveObj.cls], args.slice(1));
                }
            }

            if (typeof creation !== 'undefined') {
                //console.log('Sucessfully created a ' + baseCls);
                return creation;
            } else {
                throw new ClassResolveError("Could not resolve class '" + baseCls + "' for kind '" + this.kind + "'");
            }
        },

        // getModule's purpose is to just find the right module and return it, instead of looking for the constructor
        //  and creating an instance
        getModule: function(baseCls) {
            var resolveObj = this._resolveClassName(baseCls);
            //console.log('Successfully resolved class module for ' + baseCls + ' from ' + resolveObj.path);
            return require(resolveObj.path);
        },

        // returns the kind-specific notation object parsed from the notation json-files
        getNotation: function() {
            return require('json!notations/' + this.kind + '.json');
        },

        // constructs and returns an instance out of the given constructor and args
        _construct: function(constructor, args) {
            function Creation() {
                return constructor.apply(this, args);
            }
            Creation.prototype = constructor.prototype;
            return new Creation();
        },

        // resolves the right module by going through the graph kind's inheritance (bottom-up)
        _resolveClassName: function(cls, kind) {
            kind = kind || this.kind;

            // e.g. (NodeGroup, faulttree) becomes FaulttreeNodeGroup
            var fullClassName = kind[0].toUpperCase() + kind.slice(1) + cls;
            // e.g. (NodeGroup, faulttree) becomes faulttree/node
            var path = kind + '/' + this._fromClassToPath(cls);

            retObj = {
                cls: cls,
                kind: kind,
                path: path,
                fullClassName: fullClassName
            };

            // precondition: to subclass any class, one has to subclass an Editor (directly or indirectly) and require
            //  all classes in the XYEditor's module, that shall replace base classes in general.
            //  e.g. if you want to have a FooEditor that only differs from a FaulttreeEditor in its Nodes, you have to
            //  subclass a FaulttreeEditor in 'foo/editor.js', beginning with
            //      define(['class', 'editor', 'foo/node'], function(Class, Editor, FooNode) { ...
            //  and off course I also have to implement
            //      getFactory: function() {
            //          return new Factory('foo');
            //      },

            if (require.defined(path)) {                                  // if a kind-specific class exists and is an
                return retObj;                                            // already loaded require-module, return its path
            } else if (this._baseKind(kind)) {                            // else if our kind inherits from a base kind
                return this._resolveClassName(cls, this._baseKind(kind)); // resolve the class name from that base
            } else {
                retObj.path = this._fromClassToPath(cls);                 // else use the abstract class, e.g. Node
                return retObj;
            }
        },

        // converts every upper case letter into a '_' and a lowercase letter, so that NodeGroup becomes node_group
        _fromClassToPath: function(cls) {
            return cls.replace(/[A-Z]/g, function(t) {
                return t.slice(0, -1) + '_' + t.slice(-1).toLowerCase();
            }).slice(1);
        },

        // returns either false, if kind inherits from the base classes, or the parent kind
        _baseKind: function(kind) {
            // retrieve the baseKind from the "inherits" attribute in the notations file
            var inherits = require('json!notations/' + kind + '.json').inherits;

            if (inherits === '' || typeof inherits === 'undefined') {
                return false;
            } else {
                return inherits;
            }
        }
    });

    return new Factory();
});