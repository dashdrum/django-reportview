from setuptools import setup

setup(name='django_reportview',
      version='0.1',
      description='Class-based views for PDF output',
      long_description="A mixin and class-based views, drop-in replacements for DetailView and ListView, that allow easy creation of PDF reports using Report Lab's template language",
      url='http://dashdrum.com/reportview/',
      author='Dan Gentry',
      author_email='dan@dashdrum.com',
      keywords="django, views, PDF, RML",
      license='NCSA',
      packages=['reportview'],
      install_requires=['reportlab',],
      dependency_links=['http://github.com/roadhead/trml2pdf.git'],
      zip_safe=False,
      classifiers=[ "Framework :: Django"],
      )