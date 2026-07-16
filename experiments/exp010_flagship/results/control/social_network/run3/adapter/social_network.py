# file: social_network.py
from candidate import follow_member
from candidate import get_inbox
from candidate import get_timeline
from candidate import get_wall
from candidate import publish_post
from candidate import send_direct_message


class SocialNetwork:
    def __init__(self, clock):
        self.clock = clock

    def post(self, member, message):
        return publish_post(member, message, self.clock())

    def timeline(self, member):
        return get_timeline(member)

    def follow(self, follower, followee):
        return follow_member(follower, followee)

    def wall(self, member):
        return get_wall(member)

    def send_direct_message(self, sender, recipient, message):
        return send_direct_message(sender, recipient, message, self.clock())

    def direct_messages(self, member):
        return get_inbox(member)
