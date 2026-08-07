from solution import Network

def test_publishing_to_personal_timeline():
    network = Network()
    
    # AC-1.1: A posted message appears on its author's timeline.
    network.publish_post("Alice", "Hello, world!", 1)
    assert network.get_timeline("Alice") == ["Hello, world!"]

    # AC-1.2: A timeline lists only that member's own posts; different members' timelines are independent.
    network.publish_post("Bob", "Hi there!", 2)
    assert network.get_timeline("Alice") == ["Hello, world!"]
    assert network.get_timeline("Bob") == ["Hi there!"]

    # AC-1.3: A timeline is ordered most recent first.
    network.publish_post("Alice", "First post", 1)
    network.publish_post("Alice", "Second post", 2)
    assert network.get_timeline("Alice") == ["Second post", "First post", "Hello, world!"]

    # AC-1.4: A member who has never posted has an empty timeline.
    assert network.get_timeline("Charlie") == []

def test_following_members_and_reading_a_wall():
    network = Network()
    
    # AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message.
    network.publish_post("Alice", "Hello, world!", 1)
    network.follow_member("Bob", "Alice")
    assert network.get_wall("Bob") == ["Alice: Hello, world!"]

    # AC-2.2: After following a member, that member's posts appear on the follower's wall.
    network.publish_post("Alice", "Good morning!", 2)
    assert network.get_wall("Bob") == ["Alice: Good morning!", "Alice: Hello, world!"]

    # AC-2.3: A wall merges the member's own posts with all followed members' posts, most recent first.
    network.publish_post("Bob", "Hey everyone!", 3)
    assert network.get_wall("Bob") == ["Bob: Hey everyone!", "Alice: Good morning!", "Alice: Hello, world!"]

    # AC-2.4: Posts by members who are not followed stay off the wall.
    network.publish_post("Charlie", "Hello!", 4)
    assert network.get_wall("Bob") == ["Bob: Hey everyone!", "Alice: Good morning!", "Alice: Hello, world!"]

    # AC-2.5: Following is one-directional: the follower's posts do not appear on the followed member's wall.
    network.publish_post("Bob", "Hello Alice!", 5)
    assert network.get_wall("Alice") == ["Alice: Good morning!", "Alice: Hello, world!"]

    # AC-2.6: Following the same member twice creates no duplicate wall entries.
    network.follow_member("Bob", "Alice")  # Following again
    assert network.get_wall("Bob") == ["Bob: Hey everyone!", "Alice: Good morning!", "Alice: Hello, world!"]

    # AC-2.7: A member with no posts and no follows has an empty wall.
    network.follow_member("Charlie", "David")  # Charlie has not posted or followed anyone
    assert network.get_wall("Charlie") == []

def test_reaching_members_through_mentions():
    network = Network()
    
    # AC-3.1: A post containing an at-sign directly before a member's name lands on that member's wall even though they follow no one.
    network.publish_post("Alice", "Hello @Bob!", 1)
    assert network.get_wall("Bob") == ["Alice: Hello @Bob!"]

    # AC-3.2: Punctuation immediately after a mention does not break it.
    network.publish_post("Alice", "How are you, @Bob?", 2)
    assert network.get_wall("Bob") == ["Alice: How are you, @Bob!", "Alice: Hello @Bob!"]

    # AC-3.3: Mentions affect walls only: the post never appears on the mentioned member's timeline.
    assert network.get_timeline("Bob") == []

def test_exchanging_direct_messages():
    network = Network()
    
    # AC-4.1: A direct message is delivered to the recipient's inbox, formatted as the sender's name, a colon and a space, then the message.
    network.send_direct_message("Alice", "Bob", "Hello Bob!", 1)
    assert network.get_inbox("Bob") == ["Alice: Hello Bob!"]

    # AC-4.2: An inbox lists direct messages most recent first.
    network.send_direct_message("Alice", "Bob", "Second message!", 2)
    assert network.get_inbox("Bob") == ["Alice: Second message!", "Alice: Hello Bob!"]

    # AC-4.3: Direct messages are private: they never appear on any timeline or wall, neither the sender's nor the recipient's.
    assert network.get_timeline("Alice") == []
    assert network.get_wall("Alice") == []
    assert network.get_timeline("Bob") == []
    assert network.get_wall("Bob") == []

    # AC-4.4: A member who has received no direct messages has an empty inbox.
    assert network.get_inbox("Charlie") == []

def test_ordering_by_the_clock():
    network = Network()
    
    # AC-5.1: Recency comes from the supplied clock's timestamps rather than insertion order.
    network.publish_post("Alice", "Old post", 2)
    network.publish_post("Bob", "Newer post", 1)
    assert network.get_timeline("Alice") == ["Old post"]
    assert network.get_timeline("Bob") == ["Newer post"]

def test_same_timestamp_ordering():
    network = Network()
    
    # AC-5.2: Entries sharing the same timestamp are ordered latest-posted first.
    network.publish_post("Alice", "Message A", 1)
    network.publish_post("Bob", "Message B", 1)
    assert network.get_wall("Alice") == ["Alice: Message A"]
    assert network.get_wall("Bob") == ["Bob: Message B"]