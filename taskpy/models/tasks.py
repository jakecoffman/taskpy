import subprocess
import os

class Task(object):
	def __init__(self, name, configuration, data={}):
		self.name = name
		self.script_path = os.path.join(configuration.base_dir, 'tasks', name, 'script.py')
		self.configuration = configuration

	def update_script(self, script):
		# Make sure folder exists first
		if not os.path.exists(os.path.dirname(self.script_path)):
			os.makedirs(os.path.dirname(self.script_path))
		with open(self.script_path, 'w') as fle:
			fle.write(script)

	@property
	def script(self):
		if self.script_path and os.path.exists(self.script_path):
			return open(self.script_path, 'r').read()
		return None

	def as_json(self):
		return dict()

	def run(self, log_file):
		process = subprocess.Popen(['python', self.script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		log_file.write(process.communicate()[0])
		return process.returncode == 0