import beanstalkc

def latex2eps(text):
    b=beanstalkc.Connection()
    b.use('renderEps')
    b.watch('renderEpsResult')
    jobid = b.put(str(text.encode('utf-8')))
    # Wait for result ...
    answer = b.reserve()
    result = answer.body
    answer.delete()
    return result

def latex2pdf(text):
    b=beanstalkc.Connection()
    b.use('renderPdf')
    b.watch('renderPdfResult')
    jobid = b.put(str(text.encode('utf-8')))
    # Wait for result ...
    answer = b.reserve()
    result = answer.body
    answer.delete()
    return result
