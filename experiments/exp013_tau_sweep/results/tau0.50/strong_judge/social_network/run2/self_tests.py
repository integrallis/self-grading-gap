from solution import Network, Clock

def test_publish_message_adds_post_to_timeline():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    message = "Hello, world!"
    
    # Act
    network.publish_message(member_name, message)
    
    # Assert
    timeline = network.get_timeline(member_name)
    assert timeline == ["Hello, world!"]  # AC-1.1, AC-1.2

def test_get_timeline_lists_only_own_posts():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member1 = "Alice"
    member2 = "Bob"
    network.publish_message(member1, "Hello from Alice!")
    network.publish_message(member2, "Hello from Bob!")
    
    # Act
    timeline = network.get_timeline(member1)
    
    # Assert
    assert timeline == ["Hello from Alice!"]  # AC-1.2

def test_get_timeline_orders_posts_most_recent_first():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    network.publish_message(member_name, "First post!")
    clock.tick(1)  # Advance the clock
    network.publish_message(member_name, "Second post!")
    
    # Act
    timeline = network.get_timeline(member_name)
    
    # Assert
    assert timeline == ["Second post!", "First post!"]  # AC-1.3

def test_get_timeline_empty_for_no_posts():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    
    # Act
    timeline = network.get_timeline(member_name)
    
    # Assert
    assert timeline == []  # AC-1.4

def test_follow_member_posts_appear_on_wall():
    # Arrange
    clock = Clock()
    network = Network(clock)
    follower = "Alice"
    followed = "Bob"
    network.publish_message(followed, "Hello from Bob!")
    network.follow_member(follower, followed)
    
    # Act
    wall = network.get_wall(follower)
    
    # Assert
    assert wall == ["Bob: Hello from Bob!"]  # AC-2.2

def test_get_wall_merges_own_posts_with_followed_posts():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member1 = "Alice"
    member2 = "Bob"
    network.publish_message(member1, "Alice's post")
    clock.tick(1)  # Advance the clock
    network.publish_message(member2, "Bob's post")
    network.follow_member(member1, member2)
    
    # Act
    wall = network.get_wall(member1)
    
    # Assert
    assert wall == ["Bob: Bob's post", "Alice: Alice's post"]  # AC-2.3

def test_get_wall_excludes_unfollowed_members_posts():
    # Arrange
    clock = Clock()
    network = Network(clock)
    follower = "Alice"
    followed = "Bob"
    not_followed = "Charlie"
    network.publish_message(followed, "Hello from Bob!")
    network.publish_message(not_followed, "Hello from Charlie!")
    network.follow_member(follower, followed)
    
    # Act
    wall = network.get_wall(follower)
    
    # Assert
    assert wall == ["Bob: Hello from Bob!"]  # AC-2.4

def test_following_is_one_directional():
    # Arrange
    clock = Clock()
    network = Network(clock)
    follower = "Alice"
    followed = "Bob"
    network.publish_message(follower, "Alice's post")
    network.follow_member(follower, followed)
    
    # Act
    wall = network.get_wall(followed)
    
    # Assert
    assert wall == []  # AC-2.5

def test_following_the_same_member_twice_creates_no_duplicates():
    # Arrange
    clock = Clock()
    network = Network(clock)
    follower = "Alice"
    followed = "Bob"
    network.publish_message(followed, "Hello from Bob!")
    network.follow_member(follower, followed)
    network.follow_member(follower, followed)  # Following twice
    
    # Act
    wall = network.get_wall(follower)
    
    # Assert
    assert wall == ["Bob: Hello from Bob!"]  # AC-2.6

def test_get_wall_empty_for_no_posts_and_no_follows():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    
    # Act
    wall = network.get_wall(member_name)
    
    # Assert
    assert wall == []  # AC-2.7

def test_mentioning_member_posts_on_wall():
    # Arrange
    clock = Clock()
    network = Network(clock)
    mentioner = "Alice"
    mentioned = "Bob"
    network.publish_message(mentioner, "Hey @Bob, check this out!")
    
    # Act
    wall = network.get_wall(mentioned)
    
    # Assert
    assert wall == ["Alice: Hey @Bob, check this out!"]  # AC-3.1

def test_punctuation_after_mention_does_not_break():
    # Arrange
    clock = Clock()
    network = Network(clock)
    mentioner = "Alice"
    mentioned = "Bob"
    network.publish_message(mentioner, "Hey @Bob! How are you?")
    
    # Act
    wall = network.get_wall(mentioned)
    
    # Assert
    assert wall == ["Alice: Hey @Bob! How are you?"]  # AC-3.2

def test_mentions_do_not_appear_on_timeline():
    # Arrange
    clock = Clock()
    network = Network(clock)
    mentioner = "Alice"
    mentioned = "Bob"
    network.publish_message(mentioner, "Hey @Bob, check this out!")
    
    # Act
    timeline = network.get_timeline(mentioned)
    
    # Assert
    assert timeline == []  # AC-3.3

def test_send_direct_message_delivers_to_inbox():
    # Arrange
    clock = Clock()
    network = Network(clock)
    sender = "Alice"
    recipient = "Bob"
    message = "Hello Bob!"
    
    # Act
    network.send_direct_message(sender, recipient, message)
    
    # Assert
    inbox = network.get_inbox(recipient)
    assert inbox == ["Alice: Hello Bob!"]  # AC-4.1

def test_get_inbox_orders_messages_most_recent_first():
    # Arrange
    clock = Clock()
    network = Network(clock)
    sender = "Alice"
    recipient = "Bob"
    network.send_direct_message(sender, recipient, "First message")
    clock.tick(1)  # Advance the clock
    network.send_direct_message(sender, recipient, "Second message")
    
    # Act
    inbox = network.get_inbox(recipient)
    
    # Assert
    assert inbox == ["Alice: Second message", "Alice: First message"]  # AC-4.2

def test_direct_messages_are_private():
    # Arrange
    clock = Clock()
    network = Network(clock)
    sender = "Alice"
    recipient = "Bob"
    message = "Hello Bob!"
    network.send_direct_message(sender, recipient, message)
    
    # Act
    timeline_sender = network.get_timeline(sender)
    wall_recipient = network.get_wall(recipient)
    timeline_recipient = network.get_timeline(recipient)
    wall_sender = network.get_wall(sender)
    
    # Assert
    assert timeline_sender == []  # AC-4.3
    assert wall_recipient == []  # AC-4.3
    assert timeline_recipient == []  # AC-4.3
    assert wall_sender == []  # AC-4.3

def test_get_inbox_empty_for_no_messages():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Bob"
    
    # Act
    inbox = network.get_inbox(member_name)
    
    # Assert
    assert inbox == []  # AC-4.4

def test_recency_from_clock_timestamps():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    network.publish_message(member_name, "First message")
    clock.tick(1)  # Advance the clock
    network.publish_message(member_name, "Second message")
    clock.tick(0)  # Same timestamp
    network.publish_message(member_name, "Third message")  # Same timestamp as second
    
    # Act
    timeline = network.get_timeline(member_name)
    
    # Assert
    assert timeline == ["Third message", "Second message", "First message"]  # AC-5.1, AC-5.2

def test_wall_recency_from_clock_timestamps():
    # Arrange
    clock = Clock()
    network = Network(clock)
    follower = "Alice"
    followed = "Bob"
    network.publish_message(followed, "Bob's post")
    clock.tick(1)  # Advance the clock
    network.publish_message(follower, "Alice's post")
    network.follow_member(follower, followed)
    
    # Act
    wall = network.get_wall(follower)
    
    # Assert
    assert wall == ["Alice: Alice's post", "Bob: Bob's post"]  # AC-5.1

def test_inbox_recency_from_clock_timestamps():
    # Arrange
    clock = Clock()
    network = Network(clock)
    sender = "Alice"
    recipient = "Bob"
    network.send_direct_message(sender, recipient, "First message")
    clock.tick(1)  # Advance the clock
    network.send_direct_message(sender, recipient, "Second message")
    
    # Act
    inbox = network.get_inbox(recipient)
    
    # Assert
    assert inbox == ["Alice: Second message", "Alice: First message"]  # AC-5.1

def test_clock_reversal():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member_name = "Alice"
    network.publish_message(member_name, "First message")  # This gets timestamp 1
    clock.tick(2)  # Advance clock to timestamp 2
    network.publish_message(member_name, "Second message")  # This gets timestamp 2
    clock.tick(1)  # Advance clock to timestamp 3
    network.publish_message(member_name, "Third message")  # This gets timestamp 3
    clock.set_time(0)  # Set clock back to timestamp 0
    network.publish_message(member_name, "Fourth message")  # This gets timestamp 0
    
    # Act
    timeline = network.get_timeline(member_name)
    
    # Assert
    assert timeline == ["Third message", "Second message", "First message", "Fourth message"]  # AC-5.1, AC-5.2

def test_wall_equal_timestamp_latest_posted_first():
    # Arrange
    clock = Clock()
    network = Network(clock)
    member1 = "Alice"
    member2 = "Bob"
    network.publish_message(member1, "Alice's first post")
    clock.tick(1)  # Advance the clock
    network.publish_message(member2, "Bob's post")
    clock.tick(0)  # Same timestamp
    network.publish_message(member1, "Alice's second post")  # Same timestamp as first
    
    # Act
    network.follow_member(member2, member1)
    wall = network.get_wall(member2)
    
    # Assert
    assert wall == ["Alice: Alice's second post", "Bob: Bob's post", "Alice: Alice's first post"]  # AC-5.2

def test_inbox_equal_timestamp_latest_message_first():
    # Arrange
    clock = Clock()
    network = Network(clock)
    sender = "Alice"
    recipient = "Bob"
    network.send_direct_message(sender, recipient, "First message")
    clock.tick(1)  # Advance the clock
    network.send_direct_message(sender, recipient, "Second message")
    clock.tick(0)  # Same timestamp
    network.send_direct_message(sender, recipient, "Third message")  # Same timestamp as second
    
    # Act
    inbox = network.get_inbox(recipient)
    
    # Assert
    assert inbox == ["Alice: Third message", "Alice: Second message", "Alice: First message"]  # AC-5.2