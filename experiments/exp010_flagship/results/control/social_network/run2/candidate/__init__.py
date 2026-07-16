from collections import defaultdict

# Data structures to hold timelines, walls, follows, and inboxes
members = defaultdict(lambda: {'timeline': [], 'wall': [], 'follows': set(), 'inbox': []})

def publish(author, message, timestamp):
    # Publish a message to the author's timeline
    members[author]['timeline'].append((timestamp, message))
    # Sort the timeline by timestamp (most recent first)
    members[author]['timeline'].sort(reverse=True)

    # Update walls for followers if any
    for follower in members:
        if author in members[follower]['follows']:
            members[follower]['wall'].append((timestamp, f'{author}: {message}'))

    # Mentions
    for word in message.split():
        if word.startswith('@'):
            mentioned_member = word[1:]
            members[mentioned_member]['wall'].append((timestamp, f'{author}: {message}'))


def follow(follower, followee):
    # A member follows another member
    members[follower]['follows'].add(followee)


def timeline(member):
    # Return the timeline of a member with messages sorted by timestamp
    return [message for _, message in members[member]['timeline']]


def wall(member):
    # Combine member's own posts with followed members' posts
    wall_entries = []
    # Add own posts
    wall_entries.extend(members[member]['wall'])
    # Sort the wall entries by timestamp (most recent first)
    wall_entries.sort(reverse=True)
    return [message for _, message in wall_entries]


def direct_message(sender, recipient, message, timestamp):
    # Send a direct message to a recipient
    members[recipient]['inbox'].append((timestamp, f'{sender}: {message}'))
    # members[sender]['inbox'].append((timestamp, f'{sender}: {message}')) # Removed incorrect line
    members[recipient]['inbox'].sort(reverse=True)


def inbox(member):
    # Return the inbox messages of a member sorted by timestamp
    return [message for _, message in members[member]['inbox']]