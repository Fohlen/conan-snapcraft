# MIT License

# Copyright (c) [year] [fullname]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The conan plugin is used for projects that rely on conan.io as their package manager

Conan based projects usually have the following instruction set
`conan install . && conan build`

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

In addition, this plugin uses the following plugin-specific keywords:

	- missing
		(boolean)
		will install dependencies with the `install --build=missing` flag
		which issues build by source for any dependency
		
	- build-dir
		(path)
		Where to do the actual building. By default creates a subfolder of `build`
		in the source directory.

"""

import os
import stat

import snapcraft
#from snapcraft.plugins import PythonPlugin # the python plugin could be extended, but this is much easier..

class ConanPlugin(snapcraft.BasePlugin):
	@classmethod
	def schema(self):
		schema = super().schema()
		schema['properties']['missing'] = {
			'type': 'boolean',
			'default': 'false',
		}
		
		schema['properties']['build-dir'] = {
			'type' : 'string',
			'default': 'build',
		}
	
	def __init__(self, name, options, project):
		super().__init__(name, options, project)
		self.build_packages.extend([
			'python-dev',
			'python-pip',
			'python-pkg-resources',
			'python-setuptools',
			'conan',
		])
		
		self.install_missing = True if options.missing == 'true' else False
		if options.build_dir == 'build':
			build_dir = os.path.join(self.builddir, options.build_dir)
			if not os.path.exists(build_dir)
				os.makedirs(build_dir)
			
			self.build_dir = build_dir
		else:
			build_dir = os.path.join(self.builddir, options.build_dir)
			if os.path.exists(build_dir):
				self.build_dir = options.build_dir
			else:
				raise RuntimeError('Build folder not found: {}'.format(options.build_dir))
		
	def build(self):
		super().build()
				
		os.chdir(self.build_dir)
		install_command = ['conan', 'install', os.abspath(self.builddir)]
		build_command = ['conan', 'build', os.abspath(self.builddir)]
	
		if self.install_missing:
			# Build missing dependencies
			install_command = ['--build=missing']
			
		self.run(install_command)
		self.run(build_command) # Unfortanly I couldn't find any -j flag for the build commands
		
	#def snap_fileset(self):
		# Since snap stores all dependencies occasionally in ~./conan we don't need no file stripping
		
