import ConfigParser

conf = ConfigParser.ConfigParser()
conf.optionxform = str   # preserve case in keys    
conf.read('./settings.ini')
version=dict(conf.items('all'))['VERSION']
