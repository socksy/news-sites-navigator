#!/usr/bin/python

import urwid
import FooterEdit

palette = [('header', 'white', 'dark gray'),
           ('footer', 'white', 'dark gray'),
    ('reveal focus', 'black', 'dark cyan', 'standout')]
    
text  = [urwid.Text("news"),
         urwid.Text("news"),
         urwid.Text("news")]
         
sky = urwid.SimpleListWalker([
    urwid.AttrMap(w, None, 'reveal focus') for w in text])
    
listbox = urwid.ListBox(sky)

head_text = urwid.Text("latest news", wrap = 'clip')
head = urwid.AttrMap(head_text, 'header')
top = urwid.Frame(listbox, head)

def input_display(input, raw):

    head_text.set_text("latest news   Pressed: " + " ".join([
        unicode(i) for i in input]))
    return input


def key_input(input):
    if input in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif input == 'up':
        focus_widget, idx = listbox.get_focus()
        if idx > 0:
            idx = idx-1
            listbox.set_focus(idx)
    elif input == 'down':
        focus_widget, idx = listbox.get_focus()
        idx = idx+1
        listbox.set_focus(idx)
    elif input == 'esc':
        log_in()
        
def out(s):
    head_text.set_text(str(s))
    
    
def log_in():
    foot = FooterEdit(' Username: ')
    view.setfooter(foot)
    view.setfocus('footer')
    urwid.connect_signal(foot, 'done')
    
    
loop = urwid.MainLoop(top, palette,
    input_filter=input_display, unhandled_input=key_input)
loop.run()