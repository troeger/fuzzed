define(['faulttree/analytical_menus', 'jquery'],
function(AnalyticalMenus) {
    
    describe('Analytical Menus',function(){    
        describe('Analytical Probability Menu', function(){
            
            var editor = undefined;
            var apMenu = new AnalyticalMenus.AnalyticalProbabilityMenu(editor);  
                  
            describe('init()', function(){
                it('should have set up all required containers after initialization', function(){
                    assert(apMenu._graphIssuesContainer.is('div'), "graph issues container is missing" );
                    assert(apMenu._chartContainer.is('div'),       "chart container is missing" );      
                    assert(apMenu._tableContainer.is('div'),       "table container is missing" );      
                }); 
            });
            
              
        });
    });
});