# test_solution.py

from solution import publish_post, get_timeline, follow_member, get_wall, send_direct_message, get_inbox

def test_publish_post_adds_message_to_timeline():
    # Given a member "Alice"
    # When Alice publishes a message
    publish_post("Alice", "Hello, world!")
    # Then Alice's timeline should show her message
    assert get_timeline("Alice") == ["Hello, world!"]

def test_get_timeline_returns_only_own_posts():
    # Given members "Alice" and "Bob"
    publish_post("Alice", "Alice's first post")
    publish_post("Bob", "Bob's first post")
    # When getting Alice's timeline
    # Then it should only show Alice's posts
    assert get_timeline("Alice") == ["Alice's first post"]

def test_get_timeline_is_ordered_most_recent_first():
    # Given a member "Alice" who posts multiple messages
    publish_post("Alice", "First post", timestamp=1)
    publish_post("Alice", "Second post", timestamp=2)
    # When getting Alice's timeline
    # Then it should be ordered from most recent to oldest
    assert get_timeline("Alice") == ["Second post", "First post"]

def test_get_timeline_for_member_with_no_posts_is_empty():
    # Given a member "Alice" who has never posted
    # When getting Alice's timeline
    # Then it should be empty
    assert get_timeline("Alice") == []

def test_following_member_adds_posts_to_wall():
    # Given members "Alice" and "Bob"
    publish_post("Bob", "Bob's post")
    follow_member("Alice", "Bob")
    # When getting Alice's wall
    # Then it should show Bob's post
    assert get_wall("Alice") == ["Bob: Bob's post"]

def test_get_wall_merges_own_posts_with_followed_members():
    # Given members "Alice" and "Bob"
    publish_post("Alice", "Alice's post")
    publish_post("Bob", "Bob's post")
    follow_member("Alice", "Bob")
    # When getting Alice's wall
    # Then it should show both Alice's and Bob's posts, most recent first
    assert get_wall("Alice") == ["Alice: Alice's post", "Bob: Bob's post"]

def test_get_wall_excludes_posts_from_non_followed_members():
    # Given members "Alice", "Bob", and "Charlie"
    publish_post("Bob", "Bob's post")
    publish_post("Charlie", "Charlie's post")
    follow_member("Alice", "Bob")
    # When getting Alice's wall
    # Then it should only show Bob's post
    assert get_wall("Alice") == ["Bob: Bob's post"]

def test_following_is_one_directional():
    # Given members "Alice" and "Bob"
    publish_post("Alice", "Alice's post")
    follow_member("Alice", "Bob")
    # When getting Bob's wall
    # Then it should be empty (Alice's posts do not appear on Bob's wall)
    assert get_wall("Bob") == []

def test_following_same_member_twice_creates_no_duplicates():
    # Given members "Alice" and "Bob"
    publish_post("Bob", "Bob's post")
    follow_member("Alice", "Bob")
    follow_member("Alice", "Bob")  # Following Bob again
    # When getting Alice's wall
    # Then it should still show only one entry for Bob's post
    assert get_wall("Alice") == ["Bob: Bob's post"]

def test_get_wall_for_member_with_no_posts_and_no_follows_is_empty():
    # Given a member "Alice" who has no posts and follows no one
    # When getting Alice's wall
    # Then it should be empty
    assert get_wall("Alice") == []

def test_posting_with_mention_adds_to_mentioned_members_wall():
    # Given members "Alice" and "Bob"
    follow_member("Alice", "Bob")  # Bob follows Alice
    publish_post("Alice", "Hello @Bob!")
    # When getting Bob's wall
    # Then it should include Alice's post due to mention
    assert get_wall("Bob") == ["Alice: Hello @Bob!"]

def test_mention_with_punctuation_does_not_break_it():
    # Given members "Alice" and "Bob"
    publish_post("Alice", "Hello @Bob!")
    # When getting Bob's wall
    # Then it should include Alice's post
    assert get_wall("Bob") == ["Alice: Hello @Bob!"]

def test_post_does_not_appear_on_mentioned_member_timeline():
    # Given members "Alice" and "Bob"
    publish_post("Alice", "Hello @Bob!")
    # When getting Bob's timeline
    # Then it should be empty (the post does not appear on Bob's timeline)
    assert get_timeline("Bob") == []

def test_send_direct_message_delivers_to_recipient_inbox():
    # Given members "Alice" and "Bob"
    send_direct_message("Alice", "Bob", "Hello, Bob!")
    # When getting Bob's inbox
    # Then it should show the message from Alice
    assert get_inbox("Bob") == ["Alice: Hello, Bob!"]

def test_inbox_is_ordered_most_recent_first():
    # Given members "Alice" and "Bob"
    send_direct_message("Alice", "Bob", "First message", timestamp=1)
    send_direct_message("Alice", "Bob", "Second message", timestamp=2)
    # When getting Bob's inbox
    # Then it should be ordered from most recent to oldest
    assert get_inbox("Bob") == ["Alice: Second message", "Alice: First message"]

def test_direct_messages_are_private():
    # Given members "Alice" and "Bob"
    send_direct_message("Alice", "Bob", "Hello, Bob!")
    # When getting Alice's timeline
    # Then it should not show the direct message
    assert get_timeline("Alice") == []

def test_inbox_for_member_with_no_direct_messages_is_empty():
    # Given a member "Alice" who has not received any direct messages
    # When getting Alice's inbox
    # Then it should be empty
    assert get_inbox("Alice") == []