conan-plugin
----------------------

The conan plugin is used for projects that rely on conan.io as their package manager

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
