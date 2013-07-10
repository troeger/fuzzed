import beanstalkc
from FuzzEd.middleware import HttpResponseServerErrorAnswer
from django.core.mail import mail_admins

wait_for = 5 #seconds

def latex2eps(text):
    try:
        b=beanstalkc.Connection()
        b.use('renderEps')
        b.watch('renderEpsResult')
        jobid = b.put(str(text.encode('utf-8')))
        # Wait for result ...
        answer = b.reserve(timeout=wait_for)
    except Exception as e:
        mail_admins("Error in EPS Rendering (beanstalk client)",str(e))
        raise HttpResponseServerErrorAnswer("Sorry, we have a temporary issue with the EPS rendering. Please try again later. Our admins are notified.")
    if answer:
        result = answer.body
        answer.delete()
        return result
    else:
        mail_admins("Error in EPS Rendering - Timeout while waiting for result",str(text))
        raise HttpResponseServerErrorAnswer("Sorry, we have a temporary issue with the EPS rendering. Please try again later. Our admins are notified.")            

def latex2pdf(text):
    try:
        b=beanstalkc.Connection()
        b.use('renderPdf')
        b.watch('renderPdfResult')
        jobid = b.put(str(text.encode('utf-8')))
        # Wait for result ...
        answer = b.reserve(timeout=wait_for)
    except Exception as e:
        mail_admins("Error in PDF Rendering (beanstalk client)",str(e))       
        raise HttpResponseServerErrorAnswer("Sorry, we have a temporary issue with the PDF rendering. Please try again later. Our admins are notified.")
    if answer:
        result = answer.body
        answer.delete()
        return result
    else:
        mail_admins("Error in PDF Rendering - Timeout while waiting for result",str(text))
        raise HttpResponseServerErrorAnswer("Sorry, we have a temporary issue with the PDF rendering. Please try again later. Our admins are notified.")                        
