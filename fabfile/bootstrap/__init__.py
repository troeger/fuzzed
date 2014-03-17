from fabric.api import task
import fastfood
import platform, os, urllib

def install_apache():
    assert(platform.system() != 'Darwin')
    fastfood.system.install("apache2")
    fastfood.system.install("libapache2-mod-wsgi")

def install_django_stuff():
    # Install Django 1.6
    print "Installing Django ..."
    fastfood.python.install('django','>=1.6')

    # Install Python packages, independent from OS
    print "Installing other Python packages..."
    for package in ["south", "openid2rp", "django-require", "django-oauth-toolkit", "django-cors-headers", "django-tastypie"]:
        print "Installing "+package
        fastfood.python.install(package)        

def install_xml_stuff():
    print "Installing XML support..."
    fastfood.python.install("pyxb")
    if platform.system() != 'Darwin':
        fastfood.system.install("libxerces-c-dev")
        fastfood.system.install("xsdcxx")

def install_backend_stuff():
    print "Installing Python packages..."
    for package in ["requests"]:
        print "Installing "+package
        fastfood.python.install(package)        

def install_db_stuff():
    fastfood.system.install("psycopg2")
    if os.system("pg_isready -q") != 0:
        # Install native packages, dependent on OS
        print "Installing Postgres"
        if platform.system() != 'Darwin':
            fastfood.system.install("postgresql")
            fastfood.system.install("python-psycopg2")
        else:
            fastfood.system.install("postgres")        
        # Postgres installation, including database creation
        print "Configuring and starting PostgreSQL ..."
        fastfood.system.run('cp fabfile/bootstrap/sql.txt /tmp/')
        if platform.system() == "Darwin":
            fastfood.system.run('initdb /usr/local/var/postgres -E utf8', print_output=False)                                 # Initialize system database
            fastfood.system.run('ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents', print_output=False)       # Enable autostart  
            fastfood.system.run('launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist', print_output=False)   # Start it now
            fastfood.system.run('/usr/local/bin/psql -f /tmp/sql.txt postgres', print_output=False)
        else:
            fastfood.system.run('sudo su - postgres -c \"rm -f /tmp/sql.txt \"', print_output=False)    
            fastfood.system.run('sudo su - postgres -c \"psql -f /tmp/sql.txt postgres\"', print_output=False)    

def install_rendering_stuff():
    # Install native packages, dependent on OS
    if platform.system() != 'Darwin':
        fastfood.system.install("texlive")
    else:
        # check if Latex is installed
        print "Checking for dvips"
        if not fastfood.system.which('dvips'):
            raise Exception('We need a working Latex for the rendering server. Please install it manually.')

def install_analysis_stuff():
    # Install native packages, independent from OS
    fastfood.system.install("cmake", if_fails="cmake --version")        

    # Install native packages, dependent on OS
    if platform.system() != 'Darwin':
        fastfood.system.install("libboost1.48-all-dev")
        fastfood.system.install("g++", if_fails="g++")        
    else:
        # Perform latest GCC installation on Homebrew
        print "Installing latest GCC"
        fastfood.system.tap("homebrew/versions")
        fastfood.system.install("gcc49") # if you mess around with this, you also need to fix the CMAKE configuration

def install_less_stuff():
    fastfood.system.install("npm", if_fails="npm -v")
    if platform.system() != 'Darwin':
        fastfood.system.install("nodejs")
    # Installing less via npm: no brew on Darwin, too old in Linux apt
    print "Installing lessc"
    # Install less from NPM
    fastfood.js.install("less", if_fails="lessc -v")
    fastfood.system.run("sudo ln -s /usr/local/share/npm/bin/lessc /usr/local/bin/lessc")

def install_oauth_client():
    print "Installing OAuth client library"
    fastfood.python.install('requests_oauthlib')

@task 
def dev():
    '''Installs all software needed to make the machine a development machine.'''
    install_django_stuff()
    install_oauth_client()
    install_xml_stuff()
    install_backend_stuff()
    install_db_stuff()
    install_rendering_stuff()
    install_analysis_stuff()
    install_less_stuff()    

    print "Performing relevant builds for loadable Django project, skipping backend ..."
    fastfood.system.run("fab build.configs")
    fastfood.system.run("fab build.css")
    fastfood.system.run("fab build.notations")
    fastfood.system.run("fab build.xmlschemas")
    print "Initializing and syncing local database ..."
    fastfood.system.run('./manage.py syncdb --noinput --no-initial-data --migrate')
    
@task 
def web():
    '''Installs all software needed to make the machine a web server machine.'''
    install_apache()
    install_django_stuff()
    install_db_stuff()
    install_xml_stuff()

@task 
def backend():
    '''Installs all software needed to make the machine a backend machine.'''
    install_backend_stuff()
    install_xml_stuff()
    install_rendering_stuff()
    install_analysis_stuff()
