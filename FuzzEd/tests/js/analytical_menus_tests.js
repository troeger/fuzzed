define(['faulttree/analytical_menus'],
function(AnalyticalMenus) {
    
    describe('Analytical Menus',function(){    
        describe('Analytical Probability Menu', function(){
            
            var editor = undefined
            var apMenu = new AnalyticalMenus.AnalyticalProbabilityMenu(editor);
            
            describe('init()', function(){
                it('should have set up all required containers after initialization', function(){
                   assert(apMenu._chartContainer.is('div'), 'missing chart container') 
                });
            });
        });
    });
});