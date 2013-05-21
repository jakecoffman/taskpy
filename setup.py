from setuptools import setup, find_packages

setup(
	  name = 'taskpy'
	, version = 0.1
	, packages = find_packages()

	, package_data = {
		'taskpy': [ 'templates/*.html'
				  , 'static/favicon.ico'
				  , 'static/*.png'
				  , 'static/*.jpg'
				  , 'static/*.js'
				  , 'static/*.css'
				  , 'static/bootstrap/css/*.css'
				  , 'static/bootstrap/js/*.js'
				  , 'static/bootstrap/img/*.png'
				  ]
		}
	, install_requires =
		[ 'flask'
		, 'flask-admin>=1.0.6'
		, 'iso8601'
		]

	 , entry_points =
		{ 'console_scripts':
			[ 'taskpy = taskpy.task:main'
			, 'taskpy-clear = taskpy.clear:main'
			]
		}
	)