import sublime
import sublime_plugin
import datetime
import re


class MakeMyBranchCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())
		lines = self.view.lines(allcontent)

		ticketNumberRegex = r'CAP\w*-\d+'
		ticketBranchRegex = r'[^\w]+'
		ticketNameRegex = r'\[\w+\]\s*'
		ticketTypeRegex = r'Type:\s*([a-zA-z\-]+)'

		ticketNumber = ''
		ticketName = ''
		ticketType = ''

		for i in range(0, len(lines)):
			textLine = self.view.substr(lines[i]).strip()

			ticketNumberMatch = re.findall(ticketNumberRegex, textLine)

			if ticketNumberMatch:
			    if "Previous Issue" in textLine or "Next Issue" in textLine:
			    	continue

			    ticketNumber = ticketNumberMatch[-1]
			    ticketName = self.view.substr(lines[i + 1]).strip()

			ticketTypeMatch = re.search(ticketTypeRegex, textLine)

			if ticketTypeMatch:
				ticketType = ticketTypeMatch.group(1).lower().replace('sub-', '')

		weekNumber = 'w' + datetime.date.today().strftime("%V")
		ticketName = re.sub(ticketNameRegex, '', ticketName)
		generatedBranchName = weekNumber + '/' + ticketType + '/' + ticketNumber + '_' + re.sub(ticketBranchRegex, '_', ticketName).strip('_')

		self.view.replace(edit, allcontent, generatedBranchName + '\n' + '\n' +
			ticketNumber + ': ' + ticketName)
