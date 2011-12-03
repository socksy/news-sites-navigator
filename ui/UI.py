#!/usr/bin/python

import urwid

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
footer_text = urwid.Text("log in: ")
foot = urwid.AttrMap(footer_text, 'footer')
top = urwid.Frame(listbox, head, foot)

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
        
def out(s):
    head_text.set_text(str(s))
    
    
loop = urwid.MainLoop(top, palette,
    input_filter=input_display, unhandled_input=key_input)
loop.run()