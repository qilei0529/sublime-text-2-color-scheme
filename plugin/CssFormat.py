import commands, re
import sublime, sublime_plugin

class CssFormatCommand(sublime_plugin.TextCommand):
	flag = True

	def run(self, edit):
		for region in self.view.sel():
			codes =  self.view.substr(region)

			if self.flag :
				self.flag = False
			else:
				self.flag = True

			#to line
			if self.flag:
				codes   = codes.replace(';','; ')
				codes   = codes.replace('{','{ ')
				codes   = codes.replace('}',' }')
				strinfo = re.compile('\s{2,}')
				codes   = strinfo.sub(' ',codes)
				strinfo = re.compile('(^\s)|\s(?=\{)|\n(?=\})|(?=\})\s+')  #remove space
				codes   = strinfo.sub('',codes)
				strinfo = re.compile('(?<=\})\s+') 
				codes   = strinfo.sub('\n',codes)
				codes   = codes.replace('*/ .','*/\n.')
				codes   = codes.replace('{ }','{}')

			else:
				strinfo = re.compile('((?<={)\s+)|((?<=;)\s+)')
				codes   = strinfo.sub('\n	',codes)
				codes   = codes.replace('	}','}')
				codes   = codes.replace(' }','\n}')
				codes   = codes.replace('; ',';')
				codes   = codes.replace('{\n}','{}')

			self.view.replace(edit, region, codes)