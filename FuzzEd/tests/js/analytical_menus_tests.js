define(['faulttree/analytical_menus'],
function(AnalyticalMenus, jquery) {
    
    describe('Analytical Menus',function(){    
        describe('Analytical Probability Menu', function(){
            
            var editor = undefined
            var apMenu = new AnalyticalMenus.AnalyticalProbabilityMenu(editor);
            
            
            beforeEach(function(){
              console.log(jQuery.type(apMenu._chartContainer))
            })
            
            
            describe('init()', function(){
                it('should have set up all required containers after initialization', function(){
                   assert(apMenu._chartContainer.is('div'), "missing chart container" ) 
                });
            });
        });
    });
});