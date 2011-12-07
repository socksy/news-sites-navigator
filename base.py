class StoryList(object):
    """A list of stories
    
    It has:
    id --- a string representing this collection of stories, such as a subreddit, or a twitter username etc.
    stories --- the list of stories themselves
    """

    def __init__ (self, id, stories=[]):
        self.stories = stories
        self.id = id

class Story(object):

    """Representation of a story in reddit, HN, etc.

    Keeps a representation of a one story item. It contains:
    text --- the text of the story, e.g. the title.
    content --- the URL to where it goes, or the text of a self post.
    comment_list --- a list of Comment objects, if there are any comments.
    points --- the aggregate number of points.

    Has a method to comment on the story, comment_on_story(), and to vote on
    a story, vote().
    """

    def __init__(self, storyID, text, content=None, comment_list=None, points=None):
        
        self.storyID = storyID
        self.text = text
        self.content = content
        self.comment_list = comment_list
        self.points = points


class Comment(object):

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

    def __init__(self, commentID, username, text, subcomments=None, points=None):
        self.commentID = commentID
        self.username = username
        self.text = text
        self.subcomments = subcomments
        self.points = points


class Username(object):

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
