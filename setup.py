from setuptools import setup, find_packages

setup(
	  name = 'taskpy'
	, version = 0.1
	, packages = find_packages()

	, package_data = {
		'taskpy': [ 'templates/*.html'
				  , 'static/favicon.ico'
				  , 'static/site.css'
				  ]
		}
	, install_requires =
		[ 'flask'
		, 'flask-admin>=1.0.6'
		, 'iso8601'
		, 'celery'
		, 'flask-sqlalchemy'
		]

	 , entry_points =
		{ 'console_scripts':
			[ 'taskpy = taskpy.main:main'
			]
		}
	)