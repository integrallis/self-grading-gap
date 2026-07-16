# file: social_network.py
from candidate import SocialNetwork as CandidateSocialNetwork


class SocialNetwork:
    def __init__(self, timestamp):
        self._network = CandidateSocialNetwork()
        self._timestamp = timestamp

    def post(self, member, message):
        return self._network.publish(message, member, self._timestamp)

    def timeline(self, member):
        return self._network.get_timeline(member)

    def follow(self, follower, followee):
        return self._network.follow(follower, followee)

    def wall(self, member):
        return self._network.get_wall(member)

    def send_direct_message(self, sender, receiver, message):
        return self._network.send_direct_message(
            sender,
            receiver,
            message,
            self._timestamp,
        )

    def direct_messages(self, member):
        return self._network.get_inbox(member)
