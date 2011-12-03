#Mostly pseudo code

class Story():

    def __init__(self, uri, comment_list, points):
        self.uri = uri
        self.comment_list = comment_list
        self.points = points

    def comment_on_story(self, comment_text):
        #do comment if logged in
        pass

class Comment():

    def __init__(self, username, text, subcomments, points=None):
        self.username = username
        self.text = text
        self.subcomments = subcomments
        self.points = points

    def reply(self, comment_text):
        #reply to this comment if logged in
        pass

class Username():
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
