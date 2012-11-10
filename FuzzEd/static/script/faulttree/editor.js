define(['editor', 'faulttree/graph', 'menus', 'config', 'backend'],
function(Editor, FaulttreeGraph, Menus, Config, Backend) {
    /**
     * Class: CutsetsMenu
     */
    var CutsetsMenu = Menus.Menu.extend({
        //TODO: this should be 'show(cutsets)'
        displayCutsets: function(cutsets) {
            var listElement = this._container.find('ul');
            listElement.empty();

            _.each(cutsets, function(cutset) {
                var nodeIDs = cutset['nodes'];
                var nodes = _.map(nodeIDs, function(id) {
                    return this._editor.graph().getNodeById(id);
                }.bind(this));
                var nodeNames = _.map(nodes, function(node) {
                    return node.name;
                })

                // create list entry for the menu
                var entry = jQuery('<li><a href="#">' + nodeNames.join(', ') + '</a></li>');

                // highlight the corresponding nodes on hover
                entry.hover(
                    // in
                    function() {
                        var allNodes = this._editor._nodes;
                        _.invoke(allNodes, 'disable');
                        _.invoke(nodes, 'highlight');
                    }.bind(this),

                    // out
                    function() {
                        var allNodes = this._editor._nodes;
                        _.invoke(allNodes, 'enable');
                        _.invoke(nodes, 'highlight', false);
                    }.bind(this)
                );

                listElement.append(entry);
            }.bind(this));
        },

        _setupContainer: function() {
            return jQuery(
                '<div id="' + Config.IDs.CUTSETS_MENU + '" class="menu" header="Cutsets">\
                    <div class="menu-controls">\
                        <span class="menu-minimize"></span>\
                        <span class="menu-close"></span>\
                    </div>\
                    <ul class="nav-list unstyled"></ul>\
                </div>'
            ).appendTo(jQuery('#' + Config.IDs.CONTENT));
        }
    });

    /**
     * Class: FaultTreeEditor
     */
    return Editor.extend({
        cutsets: undefined,

        init: function(graphId) {
            this._super(graphId);

            this.cutsets = new CutsetsMenu();
            this._setupCutsetsActionEntry();
        },

        _graphClass: function() {
            return FaulttreeGraph;
        },

        _setupCutsetsActionEntry: function() {
            var navbarActionsEntry = jQuery(
                '<li>' +
                    '<a id="' + Config.IDs.NAVBAR_ACTION_CUTSETS + '" href="#">Calculate cutsets</a>' +
                '</li>');
            this._navbarActionsGroup.append(navbarActionsEntry);

            // callback that is fired when backend returns cutsets
            function loadCutsetsIntoMenu(cutsets) {
                this.cutsets.displayCutsets(cutsets);
                this.cutsets.show();
            }

            // register for clicks on the corresponding nav action
            navbarActionsEntry.click(function() {
                Backend.calculateCutsets(this.graph(), loadCutsetsIntoMenu.bind(this));
            }.bind(this));

            return this;
        }
    });
});
