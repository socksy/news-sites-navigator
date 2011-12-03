#Mostly pseudo code

class Story():

    """Representation of a story in reddit, HN.

    Keeps a representation of a one story item. It contains:
    text --- the text of the story, e.g. the title.
    content --- the URL to where it goes, or the text of a self post.
    comment_list --- a list of Comment objects, if there are any comments.
    points --- the aggregate number of points.

    Has a method to comment on the story, comment_on_story(), and to vote on
    a story, vote().
    """

    def __init__(self, text, content=None, comment_list=None, points=None):
        
        self.text = text
        self.content = uri
        self.comment_list = comment_list
        self.points = points

    def comment_on_story(self, comment_text):
        """Comments with comment_text, will fail if not logged in"""
        #do comment if logged in
        pass

    def vote(up=True):
        """Votes up on a story, or takes a boolean for whether up or down"""
        pass

class Comment():

    """Represents a comment on a story, or on a comment within a story.

    Has:
    username --- the username of the person who made the comment.
    text --- the text of the comment.
    subcomments --- a list of child comments of that comment, if they exist.
    points --- if there is any points, then this will be the votes on that 
               particular comment.

    Has a method to reply to a comment, reply(), and to vote on a story,
    vote().
    """

    def __init__(self, username, text, subcomments=None, points=None):
        self.username = username
        self.text = text
        self.subcomments = subcomments
        self.points = points

    def reply(self, comment_text):
        """Replies with comment_text. Will fail if not logged in."""
        #reply to this comment if logged in
        pass
    
    def vote(up=True):
        """Votes up on a comment, or takes a boolean for whether up or down"""
        pass

class Username():

    """Represents a username on a system

    Has three fields:
    username --- the text of the username itself
    info --- miscellaneous information on the user, changes depending on the
             context. May be None.
    points --- the number of points (or karma) the user has accrued. May be
               None.
    """

    def __init__(self, username, info=None, points=None):
        self.username = username
        self.info = info
        self.points = points

def login (username, password):
    #do login
    pass

def submit_story(story_title, story_text=None, story_url=None):
    #blah
    pass
