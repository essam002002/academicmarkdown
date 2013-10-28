# -*- coding: utf-8 -*-

"""
This file is part of zoteromarkdown.

zoteromarkdown is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

zoteromarkdown is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with zoteromarkdown.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
import os
from academicmarkdown import BaseParser

class Pandoc(BaseParser):
	
	def __init__(self, css=None, csl=None, template=None, standalone=True, \
		verbose=False):
		
		"""
		Constructor.
		
		Keyword arguments:
		css			--	A path to a `.css` file or None for no stylesheet.
						(default=None)
		csl			--	A path to a `.csl` file to specify a citation format
						or None for a default citation format. (default=None)
		template	--	The HTML template to be used. (default=None)
		standalone	--	Indicates whether the --standalone and --self-contained
						arguments should be passed to pandoc. (default=True)
		verbose		--	Indicates whether verbose output should be generated.
							(default=False)
		"""
		
		self.css = css
		self.csl = csl
		self.template = template
		self.standalone = standalone
		super(Pandoc, self).__init__(verbose=verbose)
		
	def docx(self, md, output):
		
		"""
		Generates a .docx document.
		
		Argument:
		md		--	A Markdown string.
		output	--	The name of the output file.
		"""
		
		self.odt(md, output)
		
	def epub(self, md, output):
		
		"""
		Generates an .epub document.
		
		Argument:
		md		--	A Markdown string.
		output	--	The name of the output file.
		"""		
		
		self.msg(u'Invoking pandoc')		
		cmd = u'pandoc --smart -t epub --toc -o %s' % output
		if os.path.exists(u'.bibliography.json'):			
			cmd += u' --bibliography .bibliography.json'
			if self.csl != None:
				cmd += u' --csl %s' % self.csl
		ps = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, \
			stdout=subprocess.PIPE)
		print ps.communicate(md.encode(u'utf-8'))[0].decode(u'utf-8')
		
	def html(self, md, output):
		
		"""
		Generates an .html document.
		
		Argument:
		md		--	A Markdown string.
		output	--	The name of the output file.
		"""		
		
		open(output, 'w').write(self.parse(md).encode(u'utf-8'))
		
	def odt(self, md, output):
		
		"""
		Generates an .odt document.
		
		Argument:
		md		--	A Markdown string.
		output	--	The name of the output file.
		"""		
		
		self.msg(u'Invoking pandoc')		
		cmd = u'pandoc --standalone --smart'
		if os.path.exists(u'.bibliography.json'):			
			cmd += u' --bibliography .bibliography.json'
			if self.csl != None:
				cmd += u' --csl %s' % self.csl
		cmd += ' -o'
		ps = subprocess.Popen(cmd.split() + [output], stdin=subprocess.PIPE, \
			stdout=subprocess.PIPE)
		print ps.communicate(md.encode(u'utf-8'))[0].decode(u'utf-8')
		
	def parse(self, md):
		
		"""See BaseParser.parse()."""
		
		self.msg(u'Invoking pandoc')		
		cmd = u'pandoc -f markdown -t html5 --smart'
		if self.standalone:
			cmd += u' --standalone --self-contained'
		if self.css != None:
			cmd += u' --css %s' % self.css
		if self.template != None:
			cmd += u' --template %s' % self.template
		if os.path.exists(u'.bibliography.json'):			
			cmd += u' --bibliography .bibliography.json'
			if self.csl != None:
				cmd += u' --csl %s' % self.csl
		ps = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, \
			stdout=subprocess.PIPE)
		return ps.communicate(md.encode(u'utf-8'))[0].decode(u'utf-8')		