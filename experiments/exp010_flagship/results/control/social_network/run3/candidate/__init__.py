members = {}


def publish_post(member, message, timestamp=None):
    if member not in members:
        members[member] = {'timeline': [], 'follows': set(), 'inbox': []}
    members[member]['timeline'].append((timestamp, message))


def get_timeline(member):
    if member in members:
        return [msg for _, msg in sorted(members[member]['timeline'], reverse=True)]
    return []


def follow_member(follower, followee):
    if follower not in members:
        members[follower] = {'timeline': [], 'follows': set(), 'inbox': []}
    if followee in members:
        members[follower]['follows'].add(followee)


def get_wall(member):
    if member not in members:
        return []
    wall = []
    for followee in members[member]['follows']:
        wall.extend(f"{followee}: {msg}" for _, msg in sorted(members[followee]['timeline'], reverse=True))
    wall.extend(f"{member}: {msg}" for _, msg in sorted(members[member]['timeline'], reverse=True))
    return wall


def send_direct_message(sender, recipient, message, timestamp=None):
    if recipient not in members:
        members[recipient] = {'timeline': [], 'follows': set(), 'inbox': []}
    members[recipient]['inbox'].append((timestamp, f"{sender}: {message}"))


def get_inbox(member):
    if member in members:
        return [msg for _, msg in sorted(members[member]['inbox'], reverse=True)]
    return []
