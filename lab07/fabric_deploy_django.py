from fabric import Connection

def setup_virtual_environment(c):
    print("Setting up Python 3 virtual environment...")
    c.sudo('apt-get update')
    c.sudo('apt-get upgrade -y')
    c.sudo('apt-get install -y python3-venv')
    c.sudo('mkdir -p /opt/wwc/mysites')
    c.sudo('chown ubuntu:ubuntu /opt/wwc/mysites')
    with c.cd('/opt/wwc/mysites'):
        c.run('python3 -m venv myvenv')
        c.run('source myvenv/bin/activate && pip install django')

def setup_nginx(c):
    print("Setting up and configuring nginx...")
    c.sudo('apt install -y nginx')
    
    # 上传本地 nginx 配置文件
    c.put('nginx.conf', '/tmp/nginx.conf')
    c.sudo('mv /tmp/nginx.conf /etc/nginx/sites-enabled/default')
    
    # 检查 nginx 配置
    result = c.sudo('nginx -t', warn=True)
    if result.failed:
        print("Nginx configuration test failed. Here's the output:")
        print(result.stdout)
        print(result.stderr)
        return
    
    # 如果配置正确，尝试重启 nginx
    c.sudo('systemctl restart nginx')

def setup_django_app(c):
    print("Setting up Django application...")
    with c.cd('/opt/wwc/mysites'):
        # 检查项目是否已存在
        if c.run('test -d lab', warn=True).failed:
            c.run('source myvenv/bin/activate && django-admin startproject lab')
            print("Django project 'lab' created.")
        else:
            print("Django project 'lab' already exists. Skipping project creation.")
        
        # 检查 polls 应用是否已存在
        with c.cd('lab'):
            if c.run('test -d polls', warn=True).failed:
                c.run('source ../myvenv/bin/activate && python3 manage.py startapp polls')
                print("Django app 'polls' created.")
            else:
                print("Django app 'polls' already exists. Skipping app creation.")

    # 更新 views.py
    views_content = """
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, world.')
    """
    c.run(f'echo "{views_content}" > /opt/wwc/mysites/lab/polls/views.py')

    # 更新 polls/urls.py
    urls_content = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
    """
    c.run(f'echo "{urls_content}" > /opt/wwc/mysites/lab/polls/urls.py')

    # 更新 main urls.py
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