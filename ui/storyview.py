import urwid
import random

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
        self._both = urwid.AttrWrap(urwid.Columns([point_widget, 
                             ('weight', 5, story)]), 'point body',
                             'point focus')
        widget = urwid.Pile([urwid.Divider('-'), self._both, urwid.Divider('-')])
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

        self.lorem = [
                 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sollicitudin, nulla id viverra pulvinar. Cras a magna sit amet felis fringilla lobortis.',
                 'Sed sollicitudin, nulla id viverra pulvinar.',
                 'Cras a magna sit amet felis fringilla lobortis.',
         ]

        items = []
        for i in range(1,101):
            items.append(StoryWidget(i, random.choice(self.lorem)))

        listbox = urwid.ListBox(urwid.SimpleListWalker(items))
        view = urwid.Frame(urwid.AttrWrap(listbox, 'body'))
        loop = urwid.MainLoop(view, self.palette, 
                            unhandled_input=self.keystroke)
        loop.run()
    def keystroke (self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

if __name__ == '__main__':
    StoryView()
