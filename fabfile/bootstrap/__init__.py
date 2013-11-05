from fabric.api import task
import fastfood
import platform, os, urllib

@task 
def dev():
    '''Installs all software needed to make the machine a development machine.'''

    # Install native packages, independent from OS
    print "Checking and installing native packages ..."
    for p in ["cmake"]:
        print "Installing "+p
        fastfood.system.install(p)        

    # Install Python packages, independent from OS
    print "Installing Python packages..."
    for package in ["django", "south", "openid2rp", "django-require", "pyxb", "poster"]:
        print "Installing "+package
        fastfood.python.install(package)        

    # Install native packages, dependent on OS
    if platform.system() != 'Darwin':
        # Install native packages on Linux
        for p in ["nodejs", "postgresql", "texlive", "libxerces-c-dev", "libboost1.48-all-dev", "xsdcxx", "python-psycopg2"]:
            print "Installing "+p
            fastfood.system.install(p)
    else:
        # Installing NPM
        fastfood.system.install("npm")
        # Perform latest GCC installation on Homebrew
        print "Installing latest GCC"
        fastfood.system.tap("homebrew/versions")
        fastfood.system.install("gcc49") # if you mess around with this, you also need to fix the CMAKE configuration
        # Install native packages on Darwin
        print "Installing Postgres"
        fastfood.system.install("postgres")
        # check if Latex is installed
        print "Checking for dvips"
        if not fastfood.system.which('dvips'):
            raise Exception('We need a working Latex for the rendering server. Please install it manually.')
 
    # Installing less via npm: no brew on Darwin, too old in Linux apt
    print "Checking for lessc"
    if not fastfood.system.which('lessc'):
        print "Installing lessc"
        # Install less from NPM
        fastfood.npm.install("less")
        fastfood.system.run("sudo ln -s /usr/local/share/npm/bin/lessc /usr/local/bin/lessc")


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
    print "Performing complete build to get loadable Django project code"
    fastfood.system.run("fab build.all")
    print "Initializing and syncing local database ..."
    fastfood.system.run('./manage.py syncdb --noinput --no-initial-data --migrate')
    
@task 
def web():
    '''Installs all software needed to make the machine a web server machine.'''
    for package in ["django", "south", "openid2rp", "pyxb", "django-less"]:
        cuisine.python_package_ensure(package)        
    cuisine.package_ensure("apache2")
    cuisine.package_ensure("libapache2-mod-wsgi")
    cuisine.package_ensure("postgresql")
    cuisine.package_ensure("python-psycopg2")
    #TODO: Prepare database
    #TODO: Prepare Apache config
    #    Install new release on production web server
    #    --------------------------------------------
    #    > sudo puppet apply install/prod_web.pp
    #    > tar xvfz FuzzEd-x.x.x.tar.gz /var/www/fuzztrees.net/
    #    > ln -s /var/www/fuzztrees.net/FuzzEd-x.x.x /var/www/fuzztrees.net/www
    #    > service apache2 restart


@task 
def backend():
    '''Installs all software needed to make the machine a backend machine.'''
    for package in ["pyxb","poster"]:
        cuisine.python_package_ensure(package)        
    if platform.system() != 'Darwin':
        cuisine.package_ensure("texlive")
    else:
        # check if latex is installed
        if not cmd_exists("latex"):
            raise Exception('We need a working Latex for the rendering server. Please install it manually.')
    #    Installation of production backend server
    #    -----------------------------------------
    #    > sudo puppet apply install/prod_backend.pp
    #    > tar xvfz FuzzEdAnalysis-x.x.x.tar.gz /home/fuzztrees
    #    > ln -s /home/fuzztrees/FuzzEdAnalysis-x.x.x /home/fuzztrees/analysis 
    #    > ln -s /home/fuzztrees/analysis/initscript /etc/init.d/fuzzTreesAnalysis
    #    > tar xvfz FuzzEdRendering-x.x.x.tar.gz /home/fuzztrees
    #    > ln -s /home/fuzztrees/FuzzEdRendering-x.x.x /home/fuzztrees/rendering 
    #    > ln -s /home/fuzztrees/rendering/initscript /etc/init.d/fuzzTreesRendering##
