import reddit
import session
import base

class Reddit(session.Session):
	
	def __init__(self):
	
		"""
		limit -- int, the numbers of news that would be load
		logged_in -- bool, if user is logged in
		info -- String, name of subreddit
		"""
	
		self.r = reddit.Reddit(user_agent = "null")
		self.limit = 0
		self.logged_in = False
		self.info = "null"
	
	def login(self, ID, password):
		
		"""allow login, requires user name and password"""
	
		self.r.login(user=ID,password=password)
		if isinstance(self.r.user, reddit.redditor.LoggedInRedditor):
			self.logged_in = True
		return self.logged_in
	
	def load_stories(self, info):
	
		""" load hottest news in particular subreddit
		Parameters:
		info -- String, name of subreddit
		"""
	
		self.info = info
		self.limit += 5
		submissions =  self.r.get_subreddit(info).get_hot(self.limit)
		storyList = base.StoryList(info, [])
		for sub in submissions:
			story = base.Story(sub.id, sub.title, sub.permalink, [], sub.score)
			storyList.stories.append(story)
		return storyList
	
	def load_comments(self, storyID):
	
		""" load all comments and replies of a story
		storyID -- id of story which need to load comments
		"""
	
		sub = self.r.get_submission(storyID)
		story = base.Story(sub.id, sub.title, sub.permalink, [], sub.score)
		for com in sub.comments:
			reply_list = self.load_replies(com)
			comment = base.Comment(com.id, com.author.name, com.body, reply_list)
			story.comment_list.append(comment)
		return story
		
	def load_replies(self, comment):
	
		""" return a list of all replies of a comment
		comment -- reddit.Comment
		"""
	
		if len(comment.replies) > 0:
			reply_list = []
			for rep in comment.replies:
				reply = base.Comment(rep.id, rep.author.name, rep.body, reply_list)
				reply_list.append(reply)
				reply.subcomments = self.load_replies(rep)
			return reply_list
		else:
			return []
		
	def load_more(self):
		return self.load_stories(self.info)
	
	def comment_on_story(self, storyID, comment_text):
	
		""" comment to a story, requires story id, text of comment
		storyID -- String
		comment -- String
		"""
	
		if self.logged_in:
			story = self.r.get_submission(storyID)
			story.add_comment(comment_text)
            		return True
		else:
			return "Error, please login first!"

	def reply_to_comment(self, storyID, commentID, comment_text):
	
		""" reply to a comment, requires story id, comment id and text of comment
		storyID -- String
		commentID -- String
		comment -- String
		"""
	
		if self.logged_in:
			story = self.r.get_submission(storyID)
            		comment = None
            		for com in story.comments:
                		if comment == None:
                    			comment = self.get_com(com, commentID)
			comment.reply(comment_text)
            		return True
		else:
			return "Error, please login first!"
		
	def vote(self, storyID, commentID, up):
	
		""" vote a story or comment, requires story id, comment id (option)
			and a bool represent up or down
		storyID -- String
		commentID -- String, optional
		up -- bool, if True, means up
		"""
	
		if self.logged_in:
            		story = self.r.get_submission(storyID)
			if commentID == None:
				if up:
					story.upvote()
				else:
					story.downvote()
			else:
                		comment = None
                		for com in story.comments:
                    			if comment == None:
                        			comment = self.get_com(com, commentID)
				if up:
					comment.upvote()
				else:
					comment.downvote()
			return "OK"
		else:
			return "Error, please login first!"

    	def get_com(self, comment, commentID):
    	
    		""" help function to get a comment according to the id recursively
    		comment -- reddit.Comment
    		commentID -- String
    		"""
    	
		result = None
            	for rep in comment.replies:
                	if rep.id == commentID:
                    		result = rep
                	else:
                    		result = self.get_com(rep, commentID)
            	return result
