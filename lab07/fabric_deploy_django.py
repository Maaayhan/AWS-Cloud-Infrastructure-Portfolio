from fabric import Connection

def setup_virtual_environment(c):
    # This function sets up a Python 3 virtual environment on a remote server
    # 'c' is expected to be a Fabric Connection object

    print("Setting up Python 3 virtual environment...")
    
    # 使用sudo权限 Update the package lists for upgrades and new package installations
    c.sudo('apt-get update')
    
    # 使用sudo权限 Upgrade all installed packages to their latest versions
    # The -y flag automatically answers "yes" to all prompts
    c.sudo('apt-get upgrade -y')
    
    # Install the Python 3 venv package, which is required for creating virtual environments
    c.sudo('apt-get install -y python3-venv')
    
    # Create a directory for the project
    # The -p flag creates parent directories as needed
    c.sudo('mkdir -p /opt/wwc/mysites')
    
    # Change the ownership of the project directory to the 'ubuntu' user
    # This allows the 'ubuntu' user to write to this directory
    c.sudo('chown ubuntu:ubuntu /opt/wwc/mysites')
    
    # Change the current working directory to the project directory
    # 在这个语句块内的所有命令都将在这个目录中执行
    with c.cd('/opt/wwc/mysites'):
        # Create a new Python virtual environment named 'myvenv'
        c.run('python3 -m venv myvenv')
        
        # Activate the virtual environment and install Django
        # The '&&' operator allows multiple commands to be chained
        # If the first command succeeds, the second one will be executed
        c.run('source myvenv/bin/activate && pip install django')

def setup_nginx(c):
    # This function sets up and configures Nginx on a remote server
    # 'c' is expected to be a Fabric Connection object

    print("Setting up and configuring nginx...")
    
    # Install Nginx using apt-get
    # The -y flag automatically answers "yes" to all prompts
    c.sudo('apt install -y nginx')
    
    # Upload the local nginx configuration file to the remote server
    # The file is first uploaded to /tmp for security reasons
    c.put('nginx.conf', '/tmp/nginx.conf')
    
    # Move the uploaded configuration file to the Nginx sites-enabled directory
    # This replaces the default Nginx configuration
    c.sudo('mv /tmp/nginx.conf /etc/nginx/sites-enabled/default')
    
    # Test the Nginx configuration
    # The warn=True flag prevents Fabric from stopping execution if the command fails
    result = c.sudo('nginx -t', warn=True)
    
    # Check if the Nginx configuration test failed
    if result.failed:
        print("Nginx configuration test failed. Here's the output:")
        print(result.stdout)
        print(result.stderr)
        return  # Exit the function if the configuration test failed
    
    # If the configuration test passed, restart Nginx to apply the new configuration
    c.sudo('systemctl restart nginx')

def setup_django_app(c):
    # This function sets up a Django application on a remote server
    # 'c' is expected to be a Fabric Connection object

    print("Setting up Django application...")
    
    # Change to the project directory
    with c.cd('/opt/wwc/mysites'):
        # Check if the Django project 'lab' already exists
        # The 'test -d' command checks if a directory exists
        # warn=True prevents Fabric from raising an exception if the command fails
        if c.run('test -d lab', warn=True).failed:
            # If the project doesn't exist, create a new Django project named 'lab'
            # We first activate the virtual environment to ensure we're using the correct Python and Django versions
            c.run('source myvenv/bin/activate && django-admin startproject lab')
            print("Django project 'lab' created.")
        else:
            print("Django project 'lab' already exists. Skipping project creation.")
        
        # Change to the 'lab' project directory
        with c.cd('lab'):
            # Check if the 'polls' app already exists
            if c.run('test -d polls', warn=True).failed:
                # If the app doesn't exist, create a new Django app named 'polls'
                # Again, we activate the virtual environment before running Django commands
                c.run('source ../myvenv/bin/activate && python3 manage.py startapp polls')
                print("Django app 'polls' created.")
            else:
                print("Django app 'polls' already exists. Skipping app creation.")

    # Update the views.py file with a simple view
    # This creates a basic view that returns "Hello, world" when accessed
    views_content = """
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, world.')
    """
    # We use echo to write the content to the file
    c.run(f'echo "{views_content}" > /opt/wwc/mysites/lab/polls/views.py')

    # Create the polls/urls.py file to set up URL routing for the polls app
    # This maps the root URL of the 'polls' app to the index view we just created
    urls_content = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
    """
    c.run(f'echo "{urls_content}" > /opt/wwc/mysites/lab/polls/urls.py')

    # Update the main urls.py file to include the polls app URLs
    # This connects the 'polls' app URLs to the main project URLconf
    # It also keeps the default admin URL
    main_urls_content = """
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
    """
    c.run(f'echo "{main_urls_content}" > /opt/wwc/mysites/lab/lab/urls.py')

    print("Django app setup complete.")

def run_django_server(c):
    print("Starting Django development server...")
    c.run('source /opt/wwc/mysites/myvenv/bin/activate && cd /opt/wwc/mysites/lab && python3 manage.py runserver 8000 &')

def deploy_django():
    c = Connection('23905652-vm')  # 使用您在SSH配置中设置的名称

    setup_virtual_environment(c)
    setup_nginx(c)
    setup_django_app(c)
    run_django_server(c)

    print("Django deployment complete.")

if __name__ == '__main__':
    deploy_django()