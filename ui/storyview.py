import urwid
import random
import Reddit

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

class PasswordEdit (FooterEdit):
    
    def keypress (self, size, key):
        if key == 'enter':
            urwid.emit_signal(self, 'entered', self.get_edit_text())
            return
        

class VotesWidget (urwid.WidgetWrap):
    """A widget that deals with voting information on the left of a story.

    This widget is constructed with a pile widget with an up arrow button,
    the number of points that the story has gained, and a down arrow button.
    """

    def __init__ (self, points):
        self.up_wid = urwid.Padding(urwid.AttrWrap(urwid.Button(u'\u21d1'),
                              'body', 'focus'), 'center', 5)
        self.down_wid = urwid.Padding(urwid.AttrWrap(urwid.Button(u'\u21d3'), 
                             'body', 'focus'), 'center', 5)
        point_element = urwid.Padding(urwid.Text(str(points)), 'center',
                                      'pack', len(str(points)), 1, 1)
        self.widget = urwid.Pile([self.up_wid, point_element, self.down_wid])
        self.__super.__init__(self.widget)
   
    def selectable (self):
        return True

    def keypress (self, size, key): #TODO: Selection is broken!
        if key == "j":
            self.down_wid.set_focus()
        elif key == "h":
            self.up_wid.set_focus()
        else:
            return key

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
        story_text = urwid.AttrWrap(LinkText(title, wrap="space"),
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

    def keypress (self, size, key):
        if key in ["right", "l"]:
            self._both.original_widget.set_focus(1)
        elif key in ["left", "h"]:
            self._both.original_widget.set_focus(0)
        else:
            return key


class StoryView (object):

    def __init__(self):
        self.palette = [
                ('body', 'dark cyan', '', 'standout', '#f96', ''),
                ('focus', 'white', 'dark magenta', 'standout,underline',
                    '#f96', '#063'),
                ('point body', 'dark cyan', '', ''),
                ('point focus', 'dark cyan', 'dark gray', 'bold')
                ]

        self.r = Reddit.Reddit()
        storyList = self.r.load_stories("opensource")
        self.title = []
        for story in storyList.stories:
        	self.title.append(story.text)

        items = []
        for i in range(0,len(self.title)):
            items.append(StoryWidget(i+1, self.title[i]))

        listbox = urwid.ListBox(urwid.SimpleListWalker(items))
        self.view = urwid.Frame(urwid.AttrWrap(listbox, 'body'))
        loop = urwid.MainLoop(self.view, self.palette, 
                             unhandled_input=self.keystroke)
        loop.run()
    def keystroke (self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif input in ['esc', ':']:
            self.set_command()

    def set_command(self):
        self.footer = FooterEdit(':> ')
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self.command)

    def command(self, command):
        urwid.disconnect_signal(self, self.footer, 'entered', self.command)
        if command in ['quit', 'exit', ':q', 'q']:
            raise urwid.ExitMainLoop()
        elif command == "login":
            self.login()
        else :
            self.view.set_focus('body')

    def login(self):
        self.footer = FooterEdit(u'username: ')
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self._user)

    def _user(self, name):
        urwid.disconnect_signal(self.footer, 'entered', self._user)
        self.username = name
        self.footer = PasswordEdit(u"password: ")
        self.view.set_footer(self.footer)
        self.view.set_focus('footer')
        urwid.connect_signal(self.footer, 'entered', self._password)

    def _password(self, password):
        urwid.disconnect_signal(self.footer, 'entered', self._password)
        self.password = password
        self.view.set_focus('body')
        self.view.set_footer(urwid.Text(self.password))
       

if __name__ == '__main__':
    StoryView()
