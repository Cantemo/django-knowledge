from distutils.core import setup # setuptools breaks

# Dynamically calculate the version based on knowledge.VERSION
version_tuple = __import__('knowledge').VERSION
version = '.'.join([str(v) for v in version_tuple])

setup(
    name = 'django-knowledge',
    description = '''A simple frontend and admin interface for dealing with help
        knowledge tickets and issues, including public and private responses and searching.''',
    version = version,
    author = 'Tim Child',
    author_email = 'tim@cantemo.com',
    url = 'http://github.com/Cantemo/django-knowledge',
    install_requires=['Django>=1.7.0', 'django-ckeditor-updated==4.4.4'],
    packages=['knowledge'],
    package_data={'knowledge': [
      'migrations/*.py',
      'static/knowledge/css/*',
      'templates/django_knowledge/*.html',
      'templates/django_knowledge/emails/*.html',
      'templatetags/*.py']},
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
