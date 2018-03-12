define(['job', 'jquery'],
function(Job) {
    describe('Job',function(){        
        
        var server   = undefined;
        var job      = undefined;
        var job_mock = undefined;
        var clock    = undefined;
        
    
        describe('_query', function(){
            
            beforeEach(function(){
                job      = new Job('/job_url');
                job_mock = sinon.mock(job)
                server   = sinon.fakeServer.create();
                clock    = sinon.useFakeTimers();
            });
            
            afterEach(function () {
                server.restore();
                clock.restore();
            });
                
            it('should trigger the "errorCallback" in case of an internal server error', function(){
                
                server.respondWith(
                    'GET',
                    /\/job_url/,
                    [500, {},'internal server error']
                );
                                
                job_mock.expects('errorCallback').once();
                job.start();
                
                server.respond();         
                
                job_mock.verify();
            });
            
            
            it('should trigger the "notFoundCallback" if the server responded with the status code 404', function(){
                
                server.respondWith(
                    'GET',
                    /\/job_url/,
                    [404, {}, 'no results found for job url']
                );
                
                job_mock.expects('notFoundCallback').once();
            
                job.start();
                
                server.respond();         
                
                job_mock.verify();
            });
            
            
            it('should trigger the "successCallback" if the server responded successfully with a job result', function(){
                
                var job_result_data = JSON.stringify({'data' : 'job_result'});               
                var job_result_url  = '/job_result_url';
                
                server.respondWith(
                    'GET',
                    /\/job_url/,
                    [200, {"Location" : job_result_url},
                     job_result_data]
                );
                
                job_mock.expects('successCallback').withArgs(job_result_data, job_result_url);
                
                job.start();
                
                server.respond();         
                
                job_mock.verify();
            });
            
            it('should repeat requesting for a job result if the server responded with the status code 202 and timeout duration has expired', function(){
                
                server.respondWith(
                    'GET',
                    /\/job_url/,
                    [202, {}, 'job not yet completed']
                );
                 
                var _query_spy = sinon.spy(job, '_query');
                
                job.start();
                
                server.respond();
                
                clock.tick(job.queryInterval);   
                
                _query_spy.calledTwice.should.be.true;
            });
            
        
        });
    });    
});