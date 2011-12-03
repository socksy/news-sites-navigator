import urwid

class FooterEdit():

    __metaclass__=urwid.signals.MetaSignals
    signals = ['done']

    def key_input(input):
        if key == 'enter':
            urwid.emit_signal('done', None)
            return
        elif key == 'esc':
            urwid.emit_signal('done', None)
            return
           
    urwid.key_input(input)