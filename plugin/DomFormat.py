import commands, re
import sublime, sublime_plugin

class DomFormatCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		for region in self.view.sel():
			codes =  self.view.substr(region)

			#step 1 to line
			strinfo = re.compile('\s{2,}')
			codes   = strinfo.sub(' ',codes)
			strinfo = re.compile('(^\s)|\s+$|((?<=")\s(?=\>))')  #remove space
			codes   = strinfo.sub('',codes)
			strinfo = re.compile('(^\s)|\s(?=\{)|\n(?=\})|(?=\})\s+')  #remove space
			codes   = strinfo.sub('',codes)
			codes   = codes.replace('>\n<','> <') #replace \n


			#step 2 do tab
			blockDom  = 'div|h4|p|body|table|ul|ol|li|dl|dd|head|html|link'

			blockDomEnd = ''
			domlist   = blockDom.split('|')
			for dom in domlist:
				blockDomEnd += '|' + '/' + dom

			dropDoms = blockDom + blockDomEnd
			dropDoms = '\<' + dropDoms.replace('|','|\<')
			print dropDoms

			p = re.compile(dropDoms)
			m = p.finditer(codes)

			tabE = 0
			tabC = -1
			F_close = False
			print 'dom ========= start'
			for match in m:
				g = match.group()
				t = match.span()[0] + tabE

				print g
				print t

				if F_close:
					if g[1:2] =='/':
						F_close = True
						tabC -= 1
					else:
						F_close = False
				else:
					if g[1:2] =='/':
						F_close = True
					else:
						tabC += 1
						F_close = False


				codes = codes[0:t] + '\n' + '	' * tabC + codes[t:]

				tabE = tabE + tabC + 1

				#add tab after dom
				if F_close:
					pass
				else:
					print 'after dom ' + g


			print 'dom ========= end'
			codes   = codes.replace(' \n','\n') #replace spance\n
			codes  += '\n'


			codes = self.step_3(codes,blockDom)

			print 'haha'

			self.view.replace(edit, region, codes)

	def step_3(self,codes, blockDom):

		#step 3 fix tab
		# dropDoms = '\<' + blockDom.replace('|','|\<')

		blockDomEnd = ''
		domlist   = blockDom.split('|')
		for dom in domlist:
			blockDomEnd += '|' + '/' + dom

		dropDoms = blockDom + blockDomEnd
		dropDoms = '\<' + dropDoms.replace('|','|\<')
		print dropDoms

		# codes = codes.replace('	','-#&-')
		p = re.compile( '((' + dropDoms + ')(\>))|(' + dropDoms + ')()(.+"\>)')
		m = p.finditer(codes)

		tabE = 0
		tabC = 0
		F_close = False
		print 'dom ========= start'
		for match in m:
			g = match.group()
			t = match.span()[1] + tabE
			temp = codes[t:t+1]
			print g
			print t

			if F_close:
				if g[1:2] =='/':
					F_close = True
					tabC -= 1
				else:
					F_close = False
			else:
				if g[1:2] =='/':
					F_close = True
				else:
					tabC += 1
					F_close = False

			if temp != '\n':
				codes = codes[0:t] + '\n' + '	' * tabC + codes[t:]
				tabE = tabE + tabC + 1
				pass

		print 'dom ========= end'
		codes   = codes.replace('	 ','	') #replace spance\n
		return codes