import commands, re
import sublime, sublime_plugin

class CssFormatCommand(sublime_plugin.TextCommand):
	flag = True

	def run(self, edit):
		for region in self.view.sel():
			codes =  self.view.substr(region)
			strinfo = re.compile('\s{2,}')
			flag = strinfo.search(codes)
			if flag:
				self.flag = True
			else:
				self.flag = False

			if self.flag:
				codes   = codes.replace('{','{ ')
				codes   = codes.replace('}',' }')
				strinfo = re.compile('\s{2,}')
				codes   = strinfo.sub(' ',codes)
				strinfo = re.compile('(^\s)|\s(?=\{)|\n(?=\})|(?=\})\s+')
				codes   = strinfo.sub('',codes)
				strinfo = re.compile('(?<=\})\s+|(?<=,)\s+')
				codes   = strinfo.sub('\n',codes)
			else:
				strinfo = re.compile('((?<={)\s+)|((?<=;)\s+)')
				codes   = strinfo.sub('\n	',codes)
				codes   = codes.replace('	}','}')
			self.view.erase(edit, region)
			self.view.insert(edit, region.begin(), codes)
			self.view.sel().add(region)
			pt = self.view.text_point(rc[0], rc[1])
			self.view.sel().add(region(pt))