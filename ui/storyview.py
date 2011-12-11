import urwid
import random
import Reddit

up = urwid.Button(u'\u21d1')
down = urwid.Button(u'\u21d3')

class FooterEdit (urwid.Edit):
    """The widget that lets footer input be taken for commands"""

    __metaclass__ = urwid.signals.MetaSignals
    signals = ['entered']

    def keypress (self, size, key):
        if key == 'enter':
            urwid.emit_signal(self, 'entered', self.get_edit_text())
            return
        elif key == 'esc':
            urwid.emit_signal(self, 'entered', None)
            return
        else:
            urwid.Edit.keypress(self, size, key)        

class VotesWidget (urwid.WidgetWrap):
    """A widget that deals with voting information on the left of a story.

    This widget is constructed with a pile widget with an up arrow button,
    the number of points that the story has gained, and a down arrow button.
    """

    def __init__ (self, points):
        self.up_wid = urwid.Padding(urwid.AttrWrap(up,
                              'body', 'focus'), 'center', 5)
        self.down_wid = urwid.Padding(urwid.AttrWrap(down, 
                             'body', 'focus'), 'center', 5)
        point_element = urwid.Padding(urwid.Text(str(points)), 'center',
                                      'pack', len(str(points)), 1, 1)
        self.widget = urwid.Pile([self.up_wid, point_element, self.down_wid])
        self.__super.__init__(self.widget)
   
    def selectable (self):
        return True


class LinkText (urwid.Text):
    """Extends the Text widget in order to make it selectable and clickable"""
    
    def __init__ (self, markup, align='left', wrap='space', layout=None):
        self.__super.__init__(markup, align, wrap, layout)

    def selectable (self):
        return True

    def keypress (self, size, key):
        return key #TODO make this send a signal or something when clicked


class StoryWidget (urwid.WidgetWrap):
    """Combines the LinkText widget and Votes widget in two columns."""

    def __init__ (self, points, title):
    	self.opened = False
    	self.linktext = LinkText(title, wrap="space")
        story_text = urwid.AttrWrap(self.linktext,
                                    'point_focus', 'focus')
        story = urwid.Padding(story_text,
                              'left', width=('relative',100), left=3)
        point_widget = VotesWidget(points)
        #internal variable so it can be kept track of for focus reasons
        self._both = urwid.AttrWrap(urwid.Columns(
                                        [point_widget, 
                                        ('weight', 5, story)]),
                                    'point body',
                                    'point focus')

        widget = urwid.Pile([urwid.Divider('-'),
                             self._both,
                             urwid.Divider('-')])
        self.__super.__init__(widget)

    def selectable (self):
        return True


class StoryView (object):

    def __init__(self):
        self.palette = [
                ('body', 'dark cyan', '', 'standout', '#f96', ''),
                ('focus', 'white', 'dark blue', 'standout,underline',
                    '#f96', '#063'),
                ('point body', 'dark cyan', '', ''),
                ('point focus', 'dark cyan', '', 'bold')
                ]

        self.r = Reddit.Reddit()
        self.storyList = self.r.load_stories("opensource")

        self.items = []
        for i in range(0,len(self.storyList.stories)):
            self.items.append(StoryWidget(i+1, self.storyList.stories[i].text))
    	
    	urwid.connect_signal(up, 'click', self.on_click_up)
    	urwid.connect_signal(down, 'click', self.on_click_down)

        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
        self.loop = urwid.MainLoop(self.view, self.palette, 
                             unhandled_input=self.keystroke)
        self.loop.run()
        
    def keystroke (self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif input in ['esc', ':']:
            self.set_command()
        elif input in ["enter"]:
        	self.focus = self.listbox.get_focus()
        	if isinstance(self.focus[0], StoryWidget):
        		if self.focus[0].opened:
        			story = self.storyList.stories[self.focus[1]]
        			self.focus[0].linktext.set_text(story.text)
        			self.focus[0].opened = False
		       	else:
		       		self.showComment(self.focus[1])
		       		self.focus[0].opened = True
		

    def set_command(self):
        self.footer = FooterEdit(':> ')
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self.command)
        
    def on_click_up(self, button):
		self.focus = self.listbox.get_focus()
		story = self.storyList.stories[self.focus[1]]
		storyID = story.storyID
		result = self.r.vote(storyID, None, True)
		self.view.set_footer(urwid.Text(result))	

    def command(self, command):
        urwid.disconnect_signal(self, self.footer, 'entered', self.command)
        if command in ['quit', 'exit', ':q', 'q']:
            raise urwid.ExitMainLoop()
        elif command == "login":
            self.login()
        else :
            self.view.set_focus('body')
            
    def on_click_down(self, button):
		self.focus = self.listbox.get_focus()
		story = self.storyList.stories[self.focus[1]]
		storyID = story.storyID
		result = self.r.vote(storyID, None, False)
		self.view.set_footer(urwid.Text(result))	

    def login(self):
        self.footer = FooterEdit(u'username: ')
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self._user)

    def _user(self, name):
        urwid.disconnect_signal(self.footer, 'entered', self._user)
        self.username = name
        self.footer = FooterEdit(u"password: ")
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self._password)

    def _password(self, password):
        urwid.disconnect_signal(self.footer, 'entered', self._password)
        self.password = password
        if self.r.login(self.username, self.password):
        	self.logged_in = "Login Successfull!"
        self.view.set_focus('body')
        self.view.set_footer(urwid.Text(self.logged_in))       
    
    def compose(self, comment_list, i):
		result = ""
		for a in range(i):
			result = result + "    "
		for com in comment_list:
   			if len(com.subcomments) > 0:
   				result += "--" + com.text + "\n" + self.compose(com.subcomments, i+1)
   			else:
   				for a in range(i):
					result = result + "    "
   				result += "--" + com.text + "\n"
   		return result
        
    def showComment(self, i):
    	story = self.storyList.stories[i]
    	storyID = story.storyID
    	comment_list = self.r.load_comments(storyID).comment_list
    	content = story.text + "\nComment:\n"
    	content += self.compose(comment_list, 0)
    	self.focus[0].linktext.set_text(content)
    
	

if __name__ == '__main__':
    StoryView()
