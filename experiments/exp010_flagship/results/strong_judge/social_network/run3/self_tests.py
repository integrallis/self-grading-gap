from solution import Network

def create_network(clock):
    return Network(clock)

def test_publish_post_adds_message_to_timeline():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When member "Alice" posts a message "Hello World!"
    network.publish_post("Alice", "Hello World!")
    # Then Alice's timeline should contain the message
    timeline = network.get_timeline("Alice")
    assert timeline == ["Hello World!"]  # AC-1.1

def test_timeline_only_contains_own_posts():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When members "Alice" and "Bob" post messages
    network.publish_post("Alice", "Hello from Alice!")
    network.publish_post("Bob", "Hello from Bob!")
    # Then Alice's timeline should only contain her posts
    timeline = network.get_timeline("Alice")
    assert timeline == ["Hello from Alice!"]  # AC-1.2

def test_timeline_is_ordered_most_recent_first():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When member "Alice" posts two messages
    network.publish_post("Alice", "First post!")  # timestamp 1
    network.publish_post("Alice", "Second post!") # timestamp 2
    # Then Alice's timeline should be ordered most recent first
    timeline = network.get_timeline("Alice")
    assert timeline == ["Second post!", "First post!"]  # AC-1.3

def test_empty_timeline_for_no_posts():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When we get Alice's timeline who has not posted
    timeline = network.get_timeline("Alice")
    # Then it should be empty
    assert timeline == []  # AC-1.4

def test_following_member_adds_their_posts_to_wall():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When member "Bob" posts a message and "Alice" follows Bob
    network.publish_post("Bob", "Bob's post")  # timestamp 1
    network.follow_member("Alice", "Bob")
    # Then Alice's wall should include Bob's post
    wall = network.get_wall("Alice")
    assert wall == ["Bob: Bob's post"]  # AC-2.2

def test_wall_contains_own_posts_and_followed_members_posts():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When members "Alice" and "Bob" post messages and Alice follows Bob
    network.publish_post("Alice", "Alice's post")  # timestamp 1
    network.publish_post("Bob", "Bob's post")      # timestamp 2
    network.follow_member("Alice", "Bob")
    # Then Alice's wall should merge her posts and Bob's posts
    wall = network.get_wall("Alice")
    assert wall == ["Bob: Bob's post", "Alice: Alice's post"]  # AC-2.3

def test_wall_excludes_unfollowed_members_posts():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When member "Bob" posts a message and Alice does not follow Bob
    network.publish_post("Bob", "Bob's post")  # timestamp 1
    wall = network.get_wall("Alice")
    # Then Alice's wall should be empty
    assert wall == []  # AC-2.4

def test_following_is_one_directional():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice posts a message and follows Bob
    network.publish_post("Alice", "Alice's post")  # timestamp 1
    network.follow_member("Alice", "Bob")
    # Then Bob's wall should not include Alice's posts
    wall = network.get_wall("Bob")
    assert wall == []  # AC-2.5

def test_no_duplicate_wall_entries_on_multiple_follows():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice follows Bob twice
    network.publish_post("Bob", "Bob's post")  # timestamp 1
    network.follow_member("Alice", "Bob")
    network.follow_member("Alice", "Bob")  # Following Bob again
    wall = network.get_wall("Alice")
    # Then it should only include one entry for Bob's post
    assert wall == ["Bob: Bob's post"]  # AC-2.6

def test_empty_wall_for_no_posts_and_no_follows():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice has no posts and follows no one
    wall = network.get_wall("Alice")
    # Then it should be empty
    assert wall == []  # AC-2.7

def test_mentions_on_posts_add_to_mentioned_members_wall():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice mentions Bob in a post
    network.publish_post("Alice", "Hello @Bob!")  # timestamp 1
    wall = network.get_wall("Bob")
    # Then Bob's wall should include the mention from Alice's post
    assert wall == ["Alice: Hello @Bob!"]  # AC-3.1

def test_punctuation_after_mentions_does_not_break_it():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice mentions Bob in a post with punctuation
    network.publish_post("Alice", "Hello @Bob, how are you?")  # timestamp 1
    wall = network.get_wall("Bob")
    # Then Bob's wall should still include the mention
    assert wall == ["Alice: Hello @Bob, how are you?"]  # AC-3.2

def test_mentions_do_not_appear_on_mentioned_members_timeline():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice mentions Bob in a post
    network.publish_post("Alice", "Hello @Bob!")  # timestamp 1
    timeline = network.get_timeline("Bob")
    # Then Bob's timeline should still be empty
    assert timeline == []  # AC-3.3

def test_send_direct_message_adds_to_inbox():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice sends a direct message to Bob
    network.send_direct_message("Alice", "Hello Bob!", "Bob")  # timestamp 1
    inbox = network.get_inbox("Bob")
    # Then Bob's inbox should include the direct message
    assert inbox == ["Alice: Hello Bob!"]  # AC-4.1

def test_inbox_is_ordered_most_recent_first():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice sends two direct messages to Bob
    network.send_direct_message("Alice", "First message", "Bob")  # timestamp 1
    network.send_direct_message("Alice", "Second message", "Bob")  # timestamp 2
    inbox = network.get_inbox("Bob")
    # Then Bob's inbox should be ordered most recent first
    assert inbox == ["Alice: Second message", "Alice: First message"]  # AC-4.2

def test_direct_messages_are_private():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice sends a direct message to Bob
    network.send_direct_message("Alice", "Hello Bob!", "Bob")  # timestamp 1
    timeline = network.get_timeline("Alice")
    # Then Alice's timeline should not include the direct message
    assert timeline == []  # AC-4.3
    wall = network.get_wall("Alice")
    assert wall == []  # AC-4.3

def test_empty_inbox_for_no_direct_messages():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Bob has received no direct messages
    inbox = network.get_inbox("Bob")
    # Then it should be empty
    assert inbox == []  # AC-4.4

def test_post_ordering_by_timestamp():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice posts two messages with different timestamps
    network.publish_post("Alice", "Post 1")  # timestamp 1
    network.publish_post("Alice", "Post 2")  # timestamp 2
    timeline = network.get_timeline("Alice")
    # Then it should be ordered by timestamp
    assert timeline == ["Post 2", "Post 1"]  # AC-5.1

def test_same_timestamp_order_by_recent_post():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice posts two messages with the same timestamp
    network.publish_post("Alice", "Post 1")  # timestamp 1
    network.publish_post("Alice", "Post 2")  # same timestamp
    timeline = network.get_timeline("Alice")
    # Then it should order by latest posted first
    assert timeline == ["Post 2", "Post 1"]  # AC-5.2

def test_non_monotonic_post_ordering():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice posts messages with non-monotonic timestamps
    network.publish_post("Alice", "Post 1")  # timestamp 100
    network.publish_post("Alice", "Post 2")  # timestamp 10
    network.publish_post("Alice", "Post 3")  # timestamp 50
    timeline = network.get_timeline("Alice")  
    # Then it should be ordered correctly by timestamps
    assert timeline == ["Post 1", "Post 3", "Post 2"]  # AC-5.1

def test_equal_timestamp_ordering_for_wall():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice and Bob post at the same time
    network.publish_post("Alice", "Post 1")  # timestamp 1
    network.follow_member("Alice", "Bob")
    network.publish_post("Bob", "Post 2")  # timestamp 1
    # Then the wall should list the most recent post first
    wall = network.get_wall("Alice")  
    assert wall == ["Bob: Post 2", "Alice: Post 1"]  # AC-5.2

def test_direct_message_inbox_ordering():
    # Given a network with a clock
    network = create_network(clock=lambda: 1)
    # When Alice sends direct messages to Bob
    network.send_direct_message("Alice", "First message", "Bob")  # timestamp 1
    network.send_direct_message("Alice", "Second message", "Bob")  # timestamp 2
    inbox = network.get_inbox("Bob")
    # Then the inbox should show the latest message first
    assert inbox == ["Alice: Second message", "Alice: First message"]  # AC-4.2