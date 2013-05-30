import subprocess
import stat
import os

class Task(object):
	def __init__(self, name, configuration, data={}):
		self.name = name
		self.script_path = os.path.abspath(os.path.join(configuration.base_dir, 'tasks', name, 'script.py'))
		self.configuration = configuration

	def update_script(self, script):
		# Make sure folder exists first
		if not os.path.exists(os.path.dirname(self.script_path)):
			os.makedirs(os.path.dirname(self.script_path))
		with open(self.script_path, 'w') as fle:
			# Write to file, but use native line sep!
			for line in script.split('\n'):
				fle.write(line.rstrip())
				fle.write(os.linesep)
		os.chmod(self.script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

	@property
	def script(self):
		if self.script_path and os.path.exists(self.script_path):
			return open(self.script_path, 'rU').read()
		return None

	def as_json(self):
		return  { 'name': self.name
				, 'script_path': self.script_path
				}

	def run(self, log_file, workspace):
		process = subprocess.Popen([os.path.abspath(self.script_path)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.abspath(workspace))
		log_file.write(process.communicate()[0])
		return process.returncode == 0