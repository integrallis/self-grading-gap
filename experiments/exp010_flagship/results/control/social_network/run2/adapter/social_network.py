# file: social_network.py
from candidate import direct_message as _direct_message
from candidate import follow as _follow
from candidate import inbox as _inbox
from candidate import publish as _publish
from candidate import timeline as _timeline
from candidate import wall as _wall


class SocialNetwork:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def post(self, author, message):
        return _publish(author, message, self.timestamp)

    def follow(self, follower, followee):
        return _follow(follower, followee)

    def timeline(self, member):
        return _timeline(member)

    def wall(self, member):
        return _wall(member)

    def send_direct_message(self, sender, recipient, message):
        return _direct_message(sender, recipient, message, self.timestamp)

    def direct_messages(self, member):
        return _inbox(member)
