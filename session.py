
#not strictly needed for the abstract class
import base 

class Session (object):
    """An abstract class to manage a news site connection for the UI to see.

    Concrete classes can be subclassed from this to actually do real scraping
    or interacting with data.
    """
    
    #TODO N.B. it is possible to switch between concrete classes simply by dynamically
    #changing the class of an instance. Cool python feature. So, a reddit class could be
    #loaded, and then the user says they want to use a different news site, you can simply
    #do self.__class__ = NewClass and it should just change it
    #(not tested)

    def __init__ (self):
        pass

    def load_stories (self, info=None):
        """Returns a list of stories given an info string.

        The info string changes depending on what the news site is. Subreddit in reddit,
        best in HN, username on twitter, whatever. The number of stories is limited to
        something sane, with the option to load more with the load_more() function.
        """
        self.previous_info = info
        self.stories = None
        return

    def load_more(self):
        """Loads more stories with the previous info"""
        pass

    def login (self, username, password):
        """Takes a username and password, and if successful in logging in, return True"""
        self.username = username
        self.password = password
        self.logged_in = True
        return self.logged_in

    
    def comment_on_story(self, story, comment_text):
        """Comments with comment_text, will fail if not logged in"""
        #do comment only if logged in
        pass
    
    def reply_to_comment(self, comment, comment_text):
        """Replies with comment_text. Will fail if not logged in."""
        pass

    def vote(self, item,up=True):
        """Votes up on an item (story/comment), or takes a boolean for whether
        up or down"""
        pass
