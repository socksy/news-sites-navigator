import reddit
import session
import base

class Reddit(session.Session):
	
	def __init__(self):
		self.r = reddit.Reddit(user_agent = "null")
		self.limit = 0
		self.logged_in = False
		self.info = "null"
	
	def login(self, ID, password):
		self.r.login(user=ID,password=password)
		if isinstance(self.r.user, reddit.redditor.LoggedInRedditor):
			self.logged_in = True
		return self.logged_in
	
	def load_stories(self, info):
		self.info = info
		self.limit += 5
		submissions =  self.r.get_subreddit(info).get_hot(self.limit)
		storyList = base.StoryList(info)
		for sub in submissions:
			story = base.Story(sub.id, sub.title, sub.permalink, [], sub.score)
			storyList.stories.append(story)
		return storyList
	
	def load_comments(self, storyID):
		sub = self.r.get_submission(storyID)
		story = base.Story(sub.id, sub.title, sub.permalink, [], sub.score)
		for com in sub.comments:
			reply_list = self.load_replies(com)
			comment = base.Comment(com.id, com.author.name, com.body, reply_list)
			story.comment_list.append(comment)
		return story
		
	def load_replies(self, comment):
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
		if self.logged_in:
			story = self.r.get_submission(storyID)
			story.add_comment(comment_text)
		else:
			return "Error, please login first!"
	
	def reply_to_comment(self, storyID, commentID, comment_text):
		if self.logged_in:
			story = self.r.get_submission(storyID)
			comment = None
			for com in story.comments:
				if com.id == commentID:
					comment = com
			comment.reply(comment_text)
		else:
			return "Error, please login first!"
		
	def vote(self, storyID, commentID, up):
		if self.logged_in:
			if commentID == None:
				story = self.r.get_submission(storyID)
				if up:
					story.upvote()
				else:
					story.downvote()
			else:
				story = self.r.get_submission(storyID)
				comment = None
				for com in story.comments:
					if com.id == commentID:
						comment = com
				if up:
					comment.upvote()
				else:
					comment.downvote()
		else:
			return "Error, please login first!"
