# your complete test file
from solution import Network

def test_publish_to_timeline():
    network = Network()  # Fresh instance for each test
    # AC-1.1: A posted message appears on its author's timeline.
    network.publish_post("Alice", "Hello world", 1)
    assert network.get_timeline("Alice") == ["Hello world"]  # Alice's timeline should show her post.

    # AC-1.2: A timeline lists only that member's own posts.
    network.publish_post("Bob", "Good morning", 2)
    assert network.get_timeline("Alice") == ["Hello world"]  # Alice's timeline should not include Bob's post.

    # AC-1.3: A timeline is ordered most recent first.
    network.publish_post("Alice", "Second post", 3)
    assert network.get_timeline("Alice") == ["Second post", "Hello world"]  # Most recent first.

    # AC-1.4: A member who has never posted has an empty timeline.
    assert network.get_timeline("Charlie") == []  # Charlie has never posted, so his timeline is empty.

def test_following_members_and_reading_a_wall():
    network = Network()  # Fresh instance for each test
    network.publish_post("Alice", "Hello world", 1)
    network.publish_post("Bob", "Good morning", 2)
    network.follow_member("Charlie", "Alice")  # Charlie follows Alice.

    # AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message.
    assert network.get_wall("Charlie") == ["Alice: Hello world"]  # Charlie's wall should show Alice's post.

    # AC-2.2: After following a member, that member's posts appear on the follower's wall.
    network.follow_member("Charlie", "Bob")  # Charlie also follows Bob.
    assert network.get_wall("Charlie") == ["Bob: Good morning", "Alice: Hello world"]  # Both posts should be on the wall.

    # AC-2.3: A wall merges the member's own posts with all followed members' posts.
    network.publish_post("Charlie", "My own post", 3)
    assert network.get_wall("Charlie") == ["Charlie: My own post", "Bob: Good morning", "Alice: Hello world"]  # Own post first.

    # AC-2.4: Posts by members who are not followed stay off the wall.
    network.publish_post("David", "Not followed post", 4)
    assert network.get_wall("Charlie") == ["Charlie: My own post", "Bob: Good morning", "Alice: Hello world"]  # David's post should not appear.

    # AC-2.5: Following is one-directional.
    assert network.get_wall("Alice") == []  # Alice should not see Charlie's posts on her wall.

    # AC-2.6: Following the same member twice creates no duplicate wall entries.
    network.follow_member("Charlie", "Alice")  # Following Alice again.
    assert network.get_wall("Charlie") == ["Charlie: My own post", "Bob: Good morning", "Alice: Hello world"]  # No duplicates.

    # AC-2.7: A member with no posts and no follows has an empty wall.
    assert network.get_wall("Eve") == []  # Eve has no posts and follows no one.

def test_reaching_members_through_mentions():
    network = Network()  # Fresh instance for each test
    network.publish_post("Alice", "Hello @Bob!", 1)
    network.publish_post("Bob", "Hey @Alice, how are you?", 2)

    # AC-3.1: A post containing an at-sign directly before a member's name lands on that member's wall.
    assert network.get_wall("Bob") == ["Alice: Hello @Bob!", "Bob: Hey @Alice, how are you?"]  # Bob sees Alice's mention.

    # AC-3.2: Punctuation immediately after a mention does not break it.
    network.publish_post("Alice", "Hello @Bob.", 3)  # Notice the punctuation.
    assert network.get_wall("Bob") == ["Alice: Hello @Bob.", "Alice: Hello @Bob!", "Bob: Hey @Alice, how are you?"]  # Both mentions should be visible.

    # AC-3.3: Mentions affect walls only: the post never appears on the mentioned member's timeline.
    assert network.get_timeline("Bob") == ["Hey @Alice, how are you?"]  # Bob's timeline should show his own post.

def test_exchanging_direct_messages():
    network = Network()  # Fresh instance for each test
    network.send_direct_message("Alice", "Bob", "Hello Bob!", 1)
    network.send_direct_message("Bob", "Alice", "Hi Alice!", 2)

    # AC-4.1: A direct message is delivered to the recipient's inbox.
    assert network.get_inbox("Bob") == ["Alice: Hello Bob!"]  # Bob should see Alice's message.

    # AC-4.2: An inbox lists direct messages most recent first.
    assert network.get_inbox("Alice") == ["Bob: Hi Alice!"]  # Alice should see Bob's message.

    # AC-4.3: Direct messages are private and never appear on any timeline or wall.
    assert network.get_wall("Alice") == []  # Alice's wall should not show any direct messages.
    assert network.get_wall("Bob") == []  # Bob's wall should not show any direct messages.

    # AC-4.4: A member who has received no direct messages has an empty inbox.
    assert network.get_inbox("Charlie") == []  # Charlie has received no messages.

def test_ordering_by_timestamps():
    network = Network()  # Fresh instance for each test
    network.publish_post("Alice", "First post", 3)
    network.publish_post("Bob", "Second post", 1)  # Publish later but with an earlier timestamp.
    network.publish_post("Charlie", "Third post", 2)

    # Check that the order is based on timestamps, not insertion.
    assert network.get_timeline("Alice") == ["First post"]  # Alice's timeline is unaffected.
    assert network.get_wall("Charlie") == ["Charlie: Third post", "Alice: First post", "Bob: Second post"]  # Check wall order.

def test_equal_timestamp_handling():
    network = Network()  # Fresh instance for each test
    network.publish_post("Alice", "Post 1", 1)
    network.publish_post("Alice", "Post 2", 1)  # Same timestamp, later post.
    
    # Both posts should appear, ordered by latest-posted first.
    assert network.get_timeline("Alice") == ["Post 2", "Post 1"]  # Latest-posted first for Alice's timeline.

def test_direct_message_ordering():
    network = Network()  # Fresh instance for each test
    network.send_direct_message("Alice", "Bob", "First message", 1)
    network.send_direct_message("Alice", "Bob", "Second message", 2)  # Later message with a later timestamp.

    # AC-4.2: An inbox lists direct messages most recent first.
    assert network.get_inbox("Bob") == ["Second message", "First message"]  # Bob's inbox should show messages in order.

def test_equal_timestamp_handling_in_inbox():
    network = Network()  # Fresh instance for each test
    network.send_direct_message("Alice", "Bob", "Message 1", 1)
    network.send_direct_message("Alice", "Bob", "Message 2", 1)  # Same timestamp, later message.
    
    # Both messages should appear, ordered by latest-sent first.
    assert network.get_inbox("Bob") == ["Message 2", "Message 1"]  # Latest-sent first for Bob's inbox.