import commands, re
import sublime, sublime_plugin

class DivFormatCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		for region in self.view.sel():
			codes =  self.view.substr(region)

			#step 1 to line
			strinfo = re.compile('\s{2,}')
			codes   = strinfo.sub(' ',codes)


			strinfo = re.compile('(^\s)|\s+$|((?<=")\s(?=\>))')  #remove space
			
			codes   = strinfo.sub('',codes)


			codes   = codes.replace('>\n<','> <') #replace \n

			dropDoms= 'div|html|h4' 
			strlist = dropDoms.split('|')

			p = re.compile(dropDoms)
			m = p.finditer(codes)
			for match in m:
				print match.group()


			tabCount = 0

			for dom in strlist:
				codes   = codes.replace(' <'+ dom,'\n	<'+ dom)
				# print dom

			print 'haha'

			self.view.replace(edit, region, codes)