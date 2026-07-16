class SocialNetwork:
    def __init__(self):
        self.timelines = {}
        self.walls = {}
        self.direct_messages = {}
        self.following = {}

    def publish(self, message, member, timestamp):
        if member not in self.timelines:
            self.timelines[member] = []
        self.timelines[member].append((timestamp, message))

    def get_timeline(self, member):
        if member not in self.timelines:
            return []
        return [msg for timestamp, msg in sorted(self.timelines[member], key=lambda x: (-x[0], self.timelines[member].index(x)))][::-1]

    def follow(self, follower, followee):
        if follower not in self.following:
            self.following[follower] = set()
        self.following[follower].add(followee)

    def get_wall(self, member):
        wall_posts = []
        if member in self.timelines:
            wall_posts.extend([f"{member}: {msg}" for timestamp, msg in sorted(self.timelines[member], key=lambda x: -x[0])[::-1]])
        for followee in self.following.get(member, []):
            if followee in self.timelines:
                wall_posts.extend([f"{followee}: {msg}" for timestamp, msg in sorted(self.timelines[followee], key=lambda x: -x[0])[::-1]])
        return wall_posts

    def send_direct_message(self, sender, receiver, message, timestamp):
        if receiver not in self.direct_messages:
            self.direct_messages[receiver] = []
        self.direct_messages[receiver].append((timestamp, f"{sender}: {message}"))

    def get_inbox(self, member):
        if member not in self.direct_messages:
            return []
        return [msg for timestamp, msg in sorted(self.direct_messages[member], key=lambda x: -x[0])[::-1]]