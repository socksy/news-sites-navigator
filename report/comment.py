#!/usr/bin/python
#Legacy code

import urwid

class CommentTreeWidget(urwid.TreeWidget):
    def display_text(self):
        return self.get_node().get_value()['name']
        
class CommentNode(urwid.TreeNode):
    def load_widget(self):
        return CommentWidget(self)
        
class CommentParentNode(urwid.ParentNode):
    def load_widget(self):
        return CommentTreeWidget(self)
    
    def load_reply_keys(self):
        value = self.get_value()
        return range(len(data['reply']))
        
    def load_reply_node(self, key):
        replydata = self.getvalue()['reply'][key]
        replydepth = self.get_depth() + 1
        if 'reply' in replydata:
            replyclass = CommentParentNode
        else:
            replyclass = CommentNode
        return replyclass(replydata, parent=self, key=key, depth=replydepth)
        
        
class CommentBrowser:
    palette = [
        ('body', 'black', 'light gray'),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black','underline'),
        ('title', 'white', 'black', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),
        ]
        
    footer_text = [
        ('title', "Comments"), "    ",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  ",
        ('key', "+"), ",",
        ('key', "-"), "  ",
        ('key', "LEFT"), "  ",
        ('key', "HOME"), "  ", 
        ('key', "END"), "  ",
        ('key', "Q"),
        ]
        
    def __init__(self, data=None):
        self.topnode = CommentParentNode
        self.listbox = urwid.TreeListBox(urwid.TreeWalker(self.topnode))
        self.listbox.offset_rows = 1
        self.header = urwid.Text( "" )
        self.footer = urwid.AttrWrap( urwid.Text( self.footer_text ),
            'foot')
        self.view = urwid.Frame(
            urwid.AttrWrap( self.listbox, 'body' ),
            header=urwid.AttrWrap(self.header, 'head' ),
            footer=self.footer )
            
    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.quit_input)
        self.loop.run()
        
    def quit_input(self, k):
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()
            
def get_comment_tree():
    retval = {"name":"comment1","reply":[]}
    for i in range(10):
        retval['reply'].append({"name":"troll"})
        retval['reply'][i]['reply']=[]
        retval['reply'][i]['reply'].append({"name":"troll2"})
    return retval
   
def main():
    tree = get_comment_tree()
    CommentBrowser(tree).main()
    
    
if __name__=="__main__": 
    main()
     
     
