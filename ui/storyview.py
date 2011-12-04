import urwid
import random

class VotesWidget (urwid.WidgetWrap):

    def __init__ (self, points):
        up = urwid.Padding(urwid.AttrWrap(urwid.Button(u'\u21d1'),
                              'body', 'focus'), 'center', 5)
        down = urwid.Padding(urwid.AttrWrap(urwid.Button(u'\u21d3'), 'body', 
                                'focus'), 'center', 5)
        point_element = urwid.Padding(urwid.Text(str(points)), 'center',
                                    'pack', len(str(points)), 1, 1)
        w = urwid.Pile([up, point_element, down, 
                            ],2)
        self.__super.__init__(w)
   
    def selectable (self):
        return True

    def keypress (self, size, key):
        return key

class LinkText (urwid.Text):
    
    def __init__ (self, markup, align='left', wrap='space', layout=None):
        self.__super.__init__(markup, align, wrap, layout)

    def selectable (self):
        return True

    def keypress (self, size, key):
        return key

class StoryWidget (urwid.WidgetWrap):

    def __init__ (self, points, title):
        story_text = urwid.AttrWrap(LinkText(title, wrap="space"),
                                    'point_focus', 'focus')
        story = urwid.Padding(story_text,
                            'left', width=('relative',100), left=3)
        point_widget = VotesWidget(points)
        both = urwid.AttrWrap(urwid.Columns([point_widget, 
                ('weight', 5, story)]), 'point body','point focus')
        w = urwid.Pile([urwid.Divider('-'), both, urwid.Divider('-')])
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress (self, size, key):
        return key


def main ():
    palette = [
            ('body', 'dark cyan', '', 'standout', '#f96', ''),
            ('focus', 'white', 'dark magenta', 'standout,underline',
                '#f96', '#063'),
            ('point body', 'dark cyan', '', ''),
            ('point focus', 'dark cyan', 'dark gray', 'bold')
            ]

    lorem = [
             'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
             'Sed sollicitudin, nulla id viverra pulvinar.',
             'Cras a magna sit amet felis fringilla lobortis.',
     ]

    def keystroke (input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()
    items = []
    for i in range(1,101):
        items.append(StoryWidget(i, random.choice(lorem)))

    listbox = urwid.ListBox(urwid.SimpleListWalker(items))
    view = urwid.Frame(urwid.AttrWrap(listbox, 'body'))
    loop = urwid.MainLoop(view, palette, unhandled_input=keystroke)
    loop.run()

if __name__ == '__main__':
    main()
