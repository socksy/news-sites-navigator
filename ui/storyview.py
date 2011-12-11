import urwid
import random
import Reddit
import base

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

    def __init__ (self, points, title, weight):
        self.opened = False
        self.title = title
        self.weight = weight
        self.linktext = LinkText(title, wrap="space")
        story_text = urwid.AttrWrap(self.linktext,
                                    'point_focus', 'focus')
        story = urwid.Padding(story_text,'left', width=('relative',100), left=3)
        point_widget = VotesWidget(points)
        #internal variable so it can be kept track of for focus reasons
        self._both = urwid.AttrWrap(urwid.Columns(
                                        [point_widget, 
                                        ('weight', weight, story)]),
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
        self.load_stories(self.storyList)

        urwid.connect_signal(up, 'click', self.on_click_up)
        urwid.connect_signal(down, 'click', self.on_click_down)

        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
        self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke)
        self.loop.run()
        
    def keystroke (self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif input in ['esc', ':']:
            self.set_command()
        elif input in ["c"]:
            self.focus = self.listbox.get_focus()
            self.type_comment()
        elif input in ["enter"]:
		self.focus = self.listbox.get_focus()
          	if isinstance(self.run_time_list[self.focus[1]], StoryWidget):
                	self.storyList = self.r.load_more()
                	self.load_stories(self.storyList)
                	self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
                	self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
                	self.loop.widget = self.view
                	self.view.get_body().set_focus(len(self.storyList.stories))            
     		elif isinstance(self.items[self.focus[1]], StoryWidget):
                	now_focus = self.focus[1]
                	if self.focus[0].opened:
                    		self.close_comment(self.focus[1])
                    		self.view.get_body().set_focus(now_focus)
                    		self.focus[0].opened = False
                	else:
                    		item = self.run_time_list[self.focus[1]]
                    		if isinstance(item, base.Story):
                        		storyID = item.storyID
                        		self.run_time_list[self.focus[1]] = self.r.load_comments(storyID)
                    		self.showComment(self.focus[1])
                    		self.view.get_body().set_focus(now_focus)
                    		self.focus[0].opened = True

    
    def load_stories(self, storyList):
        self.items = []
        self.run_time_list = []
        for story in self.storyList.stories:
            self.items.append(StoryWidget(story.points, story.text, 10))
            self.run_time_list.append(story)
        load_more = StoryWidget("", "-------Load More News-------",10)
        self.items.append(load_more)
        self.run_time_list.append(load_more)        

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

    def get_text(self, comment_list):
        result_list = []
        for com in comment_list:
            result_list.append(com.text + "\nBy user: " + com.username)
        return result_list
	
    def showComment(self, i):
        item = self.run_time_list[i]
        if isinstance(item, base.Story):                                       
            comment_list = item.comment_list
        else:
            comment_list = item.subcomments
        a = i
        for com in comment_list:
            a = a + 1
            self.run_time_list.insert(a, com)
        com_str_list = self.get_text(comment_list)
        b = i
        for com in com_str_list:
            b = b + 1
            if len(self.run_time_list[b].subcomments) > 0:
                self.items.insert(b, StoryWidget("Comments", com, self.items[i].weight-2))
            else:
                self.items.insert(b, StoryWidget("Comment", com, self.items[i].weight-2))
        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
        self.loop.widget = self.view    	

    def close_comment(self, i):
        weight = self.items[i].weight
        a = i + 1
        while a < len(self.items) and self.items[a].weight < weight:
            del self.items[a]
            del self.run_time_list[a]
        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
        self.loop.widget = self.view

    def type_comment(self):
        self.footer = FooterEdit('Comment text:> ')
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self.comment_on_item)        
    
    def comment_on_item(self, text):
        urwid.disconnect_signal(self.footer, 'entered', self.comment_on_item)
        item = self.run_time_list[self.focus[1]]
        if isinstance(item, base.Story):                                       
            storyID = item.storyID
            result = self.r.comment_on_story(storyID, text)
            if result == True:
                self.view.set_footer(urwid.Text("Comment Successfull! Please reload the comment page."))
            else:
                self.view.set_footer(urwid.Text(result))
        else:
            commentID = item.commentID
            i = self.focus[1] - 1
            while not isinstance(self.run_time_list[i], base.Story):
                i = i - 1
            storyID = self.run_time_list[i].storyID
            result = self.r.reply_to_comment(storyID, commentID, text)
            if result == True:
                self.view.set_footer(urwid.Text("Reply Successfull! Please reload the comment page."))
            else:
                self.view.set_footer(urwid.Text(result))
        self.view.set_focus('body')

if __name__ == '__main__':
    StoryView()
