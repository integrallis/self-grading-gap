from solution import publish, follow, wall, timeline, direct_message, inbox

def test_publishing_to_personal_timeline():
    # AC-1.1: A posted message appears on its author's timeline.
    publish("Alice", "Hello, world!", timestamp=1)
    assert timeline("Alice") == ["Hello, world!"]

    # AC-1.2: A timeline lists only that member's own posts; different members' timelines are independent.
    publish("Bob", "Goodbye, world!", timestamp=2)
    assert timeline("Alice") == ["Hello, world!"]
    assert timeline("Bob") == ["Goodbye, world!"]

    # AC-1.3: A timeline is ordered most recent first.
    publish("Alice", "Another message", timestamp=3)
    assert timeline("Alice") == ["Another message", "Hello, world!"]

    # AC-1.4: A member who has never posted has an empty timeline.
    assert timeline("Charlie") == []

def test_following_members_and_reading_a_wall():
    publish("Alice", "Hello, world!", timestamp=1)
    publish("Bob", "Goodbye, world!", timestamp=2)
    follow("Charlie", "Alice")

    # AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message.
    assert wall("Charlie") == ["Alice: Hello, world!"]

    # AC-2.2: After following a member, that member's posts appear on the follower's wall.
    follow("Charlie", "Bob")
    assert wall("Charlie") == ["Bob: Goodbye, world!", "Alice: Hello, world!"]

    # AC-2.3: A wall merges the member's own posts with all followed members' posts, most recent first.
    publish("Charlie", "My own post", timestamp=3)
    assert wall("Charlie") == ["Charlie: My own post", "Bob: Goodbye, world!", "Alice: Hello, world!"]

    # AC-2.4: Posts by members who are not followed stay off the wall.
    publish("Dave", "Unfollowed message", timestamp=4)
    assert wall("Charlie") == ["Charlie: My own post", "Bob: Goodbye, world!", "Alice: Hello, world!"]

    # AC-2.5: Following is one-directional: the follower's posts do not appear on the followed member's wall.
    assert wall("Alice") == []

    # AC-2.6: Following the same member twice creates no duplicate wall entries.
    follow("Charlie", "Alice")  # Following Alice again
    assert wall("Charlie") == ["Charlie: My own post", "Bob: Goodbye, world!", "Alice: Hello, world!"]

    # AC-2.7: A member with no posts and no follows has an empty wall.
    assert wall("Eve") == []

def test_reaching_members_through_mentions():
    publish("Alice", "Hello, @Bob!", timestamp=1)
    publish("Bob", "Goodbye, world!", timestamp=2)

    # AC-3.1: A post containing an at-sign directly before a member's name lands on that member's wall even though they follow no one.
    assert wall("Bob") == ["Alice: Hello, @Bob!"]

    # AC-3.2: Punctuation immediately after a mention does not break it.
    publish("Alice", "Hello, @Bob!", timestamp=3)  # Same message
    assert wall("Bob") == ["Alice: Hello, @Bob!", "Alice: Hello, @Bob!"]

    # AC-3.3: Mentions affect walls only: the post never appears on the mentioned member's timeline.
    assert timeline("Bob") == ["Goodbye, world!"]

def test_exchanging_direct_messages():
    direct_message("Alice", "Bob", "Hello, Bob!", timestamp=1)
    direct_message("Bob", "Alice", "Hi, Alice!", timestamp=2)

    # AC-4.1: A direct message is delivered to the recipient's inbox, formatted as the sender's name, a colon and a space, then the message.
    assert inbox("Bob") == ["Alice: Hello, Bob!"]
    assert inbox("Alice") == ["Bob: Hi, Alice!"]

    # AC-4.2: An inbox lists direct messages most recent first.
    assert inbox("Alice") == ["Bob: Hi, Alice!", "Alice: Hello, Bob!"]

    # AC-4.3: Direct messages are private: they never appear on any timeline or wall, neither the sender's nor the recipient's.
    assert timeline("Alice") == []
    assert timeline("Bob") == []

    # AC-4.4: A member who has received no direct messages has an empty inbox.
    assert inbox("Charlie") == []

def test_ordering_everything_by_the_clock():
    publish("Alice", "Msg 1", timestamp=2)
    publish("Alice", "Msg 2", timestamp=1)
    assert timeline("Alice") == ["Msg 1", "Msg 2"]  # AC-5.1: Recency comes from the supplied clock's timestamps

    direct_message("Alice", "Bob", "DM 1", timestamp=3)
    direct_message("Alice", "Bob", "DM 2", timestamp=1)
    assert inbox("Bob") == ["Alice: DM 1", "Alice: DM 2"]  # AC-5.1 for direct messages

    publish("Alice", "Msg 3", timestamp=1)
    publish("Bob", "Msg 4", timestamp=1)
    assert wall("Charlie") == ["Bob: Msg 4", "Alice: Msg 3"]  # AC-5.2: Entries sharing the same timestamp are ordered latest-posted first.