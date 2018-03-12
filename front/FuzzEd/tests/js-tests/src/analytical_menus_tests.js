define(['faulttree/analytical_menus', 'job', 'factory', 'config', 'jquery'],
function(AnalyticalMenus, Job, Factory) {
    
    var Config = Factory.getModule('Config');
    
    var apMenu = undefined;
    var server = undefined;
    
    describe('Analytical Menus',function(){    
        describe('Analytical Probability Menu', function(){
            
            beforeEach(function(){
                var editor = undefined;
                var job    = new Job();
                
                apMenu = new AnalyticalMenus.AnalyticalProbabilityMenu(editor);
                apMenu._job = job;
                
                server = sinon.fakeServer.create();  
            });
            
            afterEach(function () {
              server.restore();
            });
                  
            describe('init()', function(){
                it('should set up a container for graph issues', function(){
                    apMenu._graphIssuesContainer.is('div').should.be.true  
                }); 
                
                it('should set up a container for the chart', function(){
                    apMenu._chartContainer.is('div').should.be.true
                });      
                
                it('should set up a container for the results table', function(){
                    apMenu._tableContainer.is('div').should.be.true   
                });   
            });
            
            describe('_displayResultWithDataTables()', function(){
                
                var columns;
                var analysis_result;
                
                
                before(function(){
                
                    columns = [
                                  {'mData': 'id'                  ,'sTitle': 'Config'},
                                  {'mData': 'timestamp'           ,'sTitle': 'Time'},
                                  {'mData': 'minimum'             ,'sTitle': 'Min'},
                                  {'mData': 'peak'                ,'sTitle': 'Peak'},
                                  {'mData': 'maximum'             ,'sTitle': 'Max'}, 
                                  {'mData': 'configuration__costs','sTitle': 'Costs'}
                              ];        
                
                    analysis_result = {'aaData': 
                                         [
                                              {'timestamp': 1406808168, 'configuration__costs': 1, 'maximum': 0.99, 'choices': {5: {'type': 'RedundancyChoice', 'n': 2}}, 'minimum': 0.99, 'peak': 0.99, 'id': 133, 'points': [[0.99, 0.0], [0.99, 1.0]]},
                                              {'timestamp': 1406808168, 'configuration__costs': 1, 'maximum': 0.972, 'choices': {5: {'type': 'RedundancyChoice', 'n': 3}}, 'minimum': 0.972, 'peak': 0.972, 'id': 134, 'points': [[0.972, 0.0], [0.972, 1.0]]}, 
                                              {'timestamp': 1406808168, 'configuration__costs': 1, 'maximum': 0.9477, 'choices': {5: {'type': 'RedundancyChoice', 'n': 4}}, 'minimum': 0.9477, 'peak': 0.9477, 'id': 135, 'points': [[0.9477, 0.0], [0.9477, 1.0]]}
                                         ],
                                         'iTotalRecords': 3, 
                                         'sEcho': '1',
                                         'iTotalDisplayRecords': 3
                                      };
                });
                                                            
                it('should initialize the results table', function(){
                    
                    sinon.stub(apMenu, "_collectNodesAndEdgesForConfiguration");
                    sinon.stub(apMenu, "_displaySeriesWithHighcharts");
                        
                    server.respondWith(
                        'GET', 
                        /\/sample_job_result\.*/,
                        [200, { "Content-Type": "application/json" },
                        JSON.stringify(analysis_result)]
                    );      
                        
                    apMenu._displayResultWithDataTables(columns, '/sample_job_result');         
                    
                    server.respond();  
                    
                    
                    var dataTable_object_created = jQuery.fn.DataTable.fnIsDataTable(apMenu._table);
                    
                    dataTable_object_created.should.be.true;
                    
                    
                    var number_of_rows_passed    = _.size(analysis_result['aaData']);
                    var number_of_rows_displayed = _.size(apMenu._table.fnGetNodes());
                    
                    number_of_rows_displayed.should.be.equal(number_of_rows_passed);                
                
                });        
            });
            
            describe('_displayGraphIssues()', function(){
                    
                var errors;   
                var warnings; 
                
                before(function(){
                    errors   = [{'message': 'error message 1'}, {'message': 'error message 2'}];
                    warnings = [{'message': 'warning message 1'}, {'message': 'warning message 2'}];
                });
                
                it('should append all graph error/warning messages to the graph issues container', function(){
                    
                    apMenu._displayGraphIssues(errors, warnings);
                    
                    _.each(errors, function(error){
                        apMenu._graphIssuesContainer.should.contain(error.message);    
                    });
                    
                    _.each(warnings, function(warning){
                        apMenu._graphIssuesContainer.should.contain(warning.message);   
                    });
                    
                });        
            });
            
           
            describe('_displayJobError()', function(){
                
                var xhr;
                
                before(function(){
                    xhr = new sinon.FakeXMLHttpRequest();
                    xhr.status = 500;
                    xhr.responseText = 'sample error message';
                });
                
                it('should append received job error messages (via ajax request object) to the alert container', function(){
                    
                    apMenu._displayJobError(xhr);
                    
                    var alert_container = jQuery('#' + Config.IDs.ALERT_CONTAINER);
                    
                    alert_container.should.contain('sample error message');
                });
                
                        
            });
            
        });
    });
});