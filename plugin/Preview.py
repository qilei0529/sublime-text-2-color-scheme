import sublime, sublime_plugin
import webbrowser
 
url_map = {
	'/Users/jerry/Sites/test/' : 'http://test/',
}
 
class OpenBrowserCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		window = sublime.active_window()
		window.run_command('save')
		url = self.view.file_name()
		for path, domain in url_map.items():
			if url.startswith(path):
				url = url.replace(path, domain).replace('\\', '\/')
				break
 
		webbrowser.open_new(url)