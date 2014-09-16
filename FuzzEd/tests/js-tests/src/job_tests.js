define(['job', 'config', 'jquery'],
function(Job, Config) {
    describe('Job',function(){        
        
        var server = undefined;
        var job    = undefined;
        var clock  = undefined;
        
        describe('_query', function(){
            
            beforeEach(function(){
                job    = new Job('/server_url');
                server = sinon.fakeServer.create();
                clock = sinon.useFakeTimers();
            });
            
            afterEach(function () {
                server.restore();
                clock.restore();
            });
                    
            it('should trigger the error callback in case of an internal server error', function(){
                
                server.respondWith(
                    'GET',
                    /\/server_url/,
                    [500, {},'']
                );
                
                var job_mock = sinon.mock(job);
                
                job_mock.expects('errorCallback').once();
                job.start();
                
                server.respond();         
                
                job_mock.verify();
            });
            
            
            it('should trigger the not found callback if the server responded with status code 404', function(){
                
                server.respondWith(
                    'GET',
                    /\/server_url/,
                    [404, {}, '']
                );
                
                var job_mock = sinon.mock(job);
                job_mock.expects('notFoundCallback').once();
                job.start();
                
                server.respond();         
                
                job_mock.verify();
            });
        
        });
    });    
});