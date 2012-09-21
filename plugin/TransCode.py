import sublime, sublime_plugin  
  
class TransCodeCommand(sublime_plugin.TextCommand):  
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				line = self.view.line(region)
				line_contents = self.view.substr(line) + '\n'
				self.view.insert(edit, line.begin(), line_contents)
			else:
				codes =  self.view.substr(region)
				codes =  codes.replace('<','&lt;')
				codes =  codes.replace('>','&gt;')
				codes_contents = codes + '\n'
				self.view.insert(edit, region.begin(), codes_contents)
