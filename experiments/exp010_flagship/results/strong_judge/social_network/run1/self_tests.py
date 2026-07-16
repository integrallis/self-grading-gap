from solution import publish, follow, wall, direct_message, inbox

def test_publish_to_personal_timeline():
    # AC-1.1: A posted message appears on its author's timeline.
    publish("Alice", "Hello, world!", 1)
    assert wall("Alice") == ["Alice: Hello, world!"]  # Alice's timeline should contain her post.

    # AC-1.2: A timeline lists only that member's own posts; different members' timelines are independent.
    publish("Bob", "Good morning!", 2)
    assert wall("Alice") == ["Alice: Hello, world!"]  # Alice's posts remain unchanged.
    assert wall("Bob") == ["Bob: Good morning!"]  # Bob's timeline should contain his post.

    # AC-1.3: A timeline is ordered most recent first.
    publish("Alice", "First post!", 3)
    assert wall("Alice") == ["Alice: First post!", "Alice: Hello, world!"]  # Most recent post first.

    # AC-1.4: A member who has never posted has an empty timeline.
    assert wall("Charlie") == []  # Charlie has not posted anything.


def test_following_members_and_reading_a_wall():
    publish("Alice", "Hello, world!", 1)
    publish("Bob", "Good morning!", 2)
    follow("Alice", "Bob")

    # AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message.
    assert wall("Alice") == ["Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.2: After following a member, that member's posts appear on the follower's wall.
    assert wall("Bob") == ["Bob: Good morning!"]  # Bob's own wall should only show his post.

    # AC-2.3: A wall merges the member's own posts with all followed members' posts, most recent first.
    publish("Alice", "Second post!", 3)
    assert wall("Alice") == ["Alice: Second post!", "Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.4: Posts by members who are not followed stay off the wall.
    publish("Charlie", "Hey there!", 4)
    assert wall("Alice") == ["Alice: Second post!", "Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.5: Following is one-directional: the follower's posts do not appear on the followed member's wall.
    assert wall("Bob") == ["Bob: Good morning!"]

    # AC-2.6: Following the same member twice creates no duplicate wall entries.
    follow("Alice", "Bob")
    assert wall("Alice") == ["Alice: Second post!", "Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.7: A member with no posts and no follows has an empty wall.
    assert wall("Dana") == []  # Dana has no posts and follows no one.


def test_reaching_members_through_mentions():
    publish("Bob", "Good morning!", 2)
    publish("Alice", "Hello @Bob!", 1)

    # AC-3.1: A post containing an at-sign directly before a member's name lands on that member's wall even though they follow no one.
    assert wall("Bob") == ["Alice: Hello @Bob!"]  # Bob's wall should show the mention.

    # AC-3.2: Punctuation immediately after a mention does not break it.
    publish("Alice", "Hey @Bob.", 3)
    assert wall("Bob") == ["Alice: Hey @Bob.", "Alice: Hello @Bob!"]  # Both mentions should be present.

    # AC-3.3: Mentions affect walls only: the post never appears on the mentioned member's timeline.
    assert wall("Alice") == ["Alice: Hey @Bob.", "Alice: Hello @Bob!"]  # Alice's timeline does not include the mentioning post.


def test_exchanging_direct_messages():
    direct_message("Alice", "Bob", "Hello, Bob!", 1)
    
    # AC-4.1: A direct message is delivered to the recipient's inbox, formatted as the sender's name, a colon and a space, then the message.
    assert inbox("Bob") == ["Alice: Hello, Bob!"]

    # AC-4.2: An inbox lists direct messages most recent first.
    direct_message("Alice", "Bob", "How are you?", 2)
    assert inbox("Bob") == ["Alice: How are you?", "Alice: Hello, Bob!"]

    # AC-4.3: Direct messages are private: they never appear on any timeline or wall, neither the sender's nor the recipient's.
    assert wall("Alice") == []  # Alice's wall should be empty.
    assert wall("Bob") == []  # Bob's wall should also be empty.

    # AC-4.4: A member who has received no direct messages has an empty inbox.
    assert inbox("Charlie") == []  # Charlie has received no messages.


def test_ordering_everything_by_the_clock():
    publish("Alice", "Post 1", 2)
    publish("Alice", "Post 2", 1)
    assert wall("Alice") == ["Alice: Post 1", "Alice: Post 2"]  # Should be ordered by timestamp, latest first.
    
    publish("Alice", "Post 3", 3)
    assert wall("Alice") == ["Alice: Post 3", "Alice: Post 1", "Alice: Post 2"]  # Newest post first, ordered by timestamp.