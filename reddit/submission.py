# This file is part of reddit_api.
#
# reddit_api is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# reddit_api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with reddit_api.  If not, see <http://www.gnu.org/licenses/>.

from urls import urls
from urlparse import urljoin

from base_objects import RedditContentObject
from features import Deletable, Saveable, Voteable


class Submission(RedditContentObject, Saveable, Voteable,  Deletable):
    """A class for submissions to Reddit."""

    kind = "t3"

    def __init__(self, reddit_session, title=None, json_dict=None):
        super(Submission, self).__init__(reddit_session, title, json_dict)
        if not self.permalink.startswith(urls["reddit_url"]):
            self.permalink = urljoin(urls["reddit_url"], self.permalink)
        self._comments = None

    def __str__(self):
        title = self.title.replace("\r\n", "")
        return "{0} :: {1}".format(self.score, title.encode("utf-8"))

    @property
    def comments(self):
        if self._comments == None:
            submission_info, comment_info = self.reddit_session._request_json(
                self.permalink)
            self._comments = comment_info["data"]["children"]
            for comment in self._comments:
                comment._update_submission(self)
        return self._comments

    @comments.setter
    def comments(self, comments):
        for comment in comments:
            comment._update_submission(self)
        self._comments = comments

    def add_comment(self, text):
        """If logged in, comment on the submission using the specified text."""
        return self.reddit_session._add_comment(self.name, text)
