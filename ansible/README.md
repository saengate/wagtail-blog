# Rol Ansible para instalar Django
 * Versión `Ansible 2.9`
 * Este documento busca introducir lo necesario en `Ansible` para que encaso de necesitar realizar algún cambio dejar las herramientas necesarias para hacerlo.

 Antes que nada, la documentación y la página en la que se basa el proyecto es la siguiente:

 * [Ansible](https://www.ansible.com/)
 * [Documentación Ansible](https://docs.ansible.com/?extIdCarryOver=true&sc_cid=701f2000001OH7YAAW)
 * [Comandos generales](https://docs.ansible.com/ansible/latest/collections/index.html)
 * [Comandos comunes en consola](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugins-in-ansible-builtin)

 El árbol del directorio de este proyecto en especifico es el siguiente:

 <pre>
 ansible
 +-- group_vars
 |   +-- all
 |   |   +-- vars.yml
 |   +-- develop
 |   |   +-- vars.yml
 +-- host_vars
 |   +-- localhost
 +-- _roles
 |   +-- ansible-role-django
 |   |   +-- handlers
 |   |   |   +-- main.yml
 |   |   +-- tasks
 |   |   |   +-- main.yml
 |   |   +-- templates
 |   |   |   +-- cmdp.j2
 |   |   |   +-- django-migrate.j2
 |   |   |   +-- django_start.j2
 |   |   |   +-- runsupervisor.j2
 |   |   |   +-- timeout.conf.j2
 |   |   |   +-- wait-for-it.j2
 |   |   |   +-- django-messages.j2
 |   |   |   +-- django.supervisor.conf.j2
 |   |   |   +-- nginx.conf.j2
 |   |   |   +-- supervisord.conf.j2
 |   |   |   +-- venv.j2
 +-- ansible.cfg
 +-- config-django.yml
 +-- inventory
 </pre>

 Respecto al contenido de que conseguiras en cada carpeta, este es el detalle:

 - `ansible`: nombre del proyecto, en este caso es ansible.
     - `ansible.cfg`: archivo de configuraciones generales de ansible.
     - `config-django.yml`: archivo de playbook que define los host y los roles que se instalan en este proyecto.
     - `inventory`: archivo de inventario de host donde se instalan los roles.
     - `group_vars`: grupo de variables generales, se pueden separar por ambientes.
         - `all`: variables globales para todo el proyecto.
             - `vars.yml`: archivo yml con las variables definidas.
         - `develop`: variables para SOLO el entorno de desarrollo, el nombre puede cambiar.
             - `vars.yml`: archivo yml con las variables definidas.
     - `host_vars`: variables especificas para un host, se define indicando el nombre del host.
         - `localhost`: archivo sin extensión con el nombre del host con variables definidas en formato yml.
     - `roles`: directorio de roles complejos para la instalación de playbooks o proyectos ansible.
         - `ansible-role-django`: directorio rol ansible que instala el proyecto django.
             - `handlers`: normalmente usados para reiniciar servicios al completar configuraciones.
                 - `main.yml`: grupo de servicios en yml a reiniciar.
             - `tasks`: carpeta principal del proyecto, contiene el grupo de instrucciones a realizar.
                 - `main.yml`: archivo principal del role con instrucciones a ejecutar en el host.
             - `templates`: directorio de plantillas que se usaran en la configuración del host.
                 - `cmdp.j2`: scripts con alias de comandos de uso frecuente en el proyecto, detallados en el readme del proyecto.
                 - `django-migrate.j2`: scripts con las todas las intrucciones para ejecutar las migraciones y archivos estaticos en django.
                 - `django_start.j2`: script que inicia un programa de gunicorn para el proyecto.
                 - `runsupervisor.j2`: scripts para reiniciar supervisor, recargar y actualizar todos sus programas.
                 - `timeout.conf.j2`: configuraciones de timeout de nginx.
                 - `wait-for-it.j2`: libreria externa para docker-compose espere la base de datos antes de iniciar el proyecto.
                 - `django-messages.j2`: scripts para compilar los mensajes y sus traducciones en el proyecto.
                 - `django.supervisor.conf.j2`: archivo de configuraciones de programas a usar en supervisor.
                 - `nginx.conf.j2`: configuraciones del servidor nginx.
                 - `supervisord.conf.j2`: archivo de configuraciones de supervisor.
                 - `venv.j2`: archivo para facilitar el acceso al entorno virtual de python.


 # ¿Cómo funciona?

 La mayoria de los comandos se agregan dentro de la carpeta `roles` en `tasks` y se estan usando los `Comandos comunes en consola`, al inicio se encuentra el link a la documentación de ansible.

 Agrego una lista con los comando usandos y su función:

 * `stat`: Es una especie de variable que entrega el estado de un directorio, ¿existe? true/false, para ser usado posteriormente con la condicional `when` y ejecutar otro comando. 
 * `service`: Permite acceder a un servicio y realizar acciones como iniciar, detener o reiniciar.
 * `group`: Administra grupos en el sistema operativo, crear, eliminar o actualizar.
 * `user`: Administra usuarios en el sistema operativo, crear, eliminar o actualizar.
 * `lineinfile`: Accede a la linea de un archivo para realizar acciones sobre esta.
 * `file`: Accede a un archivo para realizar acciones sobre este.
 * `command`: Ejecuta comandos de consola, usado cuando ansible no tiene un comando propio para acceder al recurso.
 * `pip`: Instala paquetes python.
 * `template`: mueve los archivos de la carpeta `template` al directorio especificado remplazando las variables contenidas en estos por las declaradas en los archivos dentro de `group_vars`.

 Las variables que se declaran en los archivos dentro de `group_vars` se acceden de forma diferente desde `jinja2`y desde los archivos `yml`, se explica el formato:
 * `archivos.yml`: siempre entre comillas dobles.
     Ejemplo:
         - "{{ variable }}"
 * `template.j2`: solo entre parentesis.
     Ejemplo:
         - {{ variable }}