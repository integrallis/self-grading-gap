from solution import publish_post, get_timeline, follow_member, get_wall, send_direct_message, get_inbox

def test_publish_post_adds_message_to_timeline():
    # Alice publishes a post
    publish_post("Alice", "Hello, world!")
    # Alice's timeline should contain her message
    assert get_timeline("Alice") == ["Hello, world!"]  # Only her own post, most recent first

def test_get_timeline_lists_only_own_posts():
    publish_post("Alice", "Hello, world!")
    publish_post("Bob", "Good day!")
    # Alice's timeline should only show her posts
    assert get_timeline("Alice") == ["Hello, world!"]  # Independent timelines

def test_get_timeline_is_ordered_most_recent_first():
    publish_post("Alice", "First post")
    publish_post("Alice", "Second post")
    # Alice's timeline should show the latest post first
    assert get_timeline("Alice") == ["Second post", "First post"]  # Newest first

def test_get_timeline_is_empty_for_member_with_no_posts():
    # Bob has never posted
    assert get_timeline("Bob") == []  # Empty timeline

def test_follow_member_adds_posts_to_wall():
    publish_post("Alice", "Hello, world!")
    follow_member("Bob", "Alice")
    # Bob should see Alice's posts on his wall
    assert get_wall("Bob") == ["Alice: Hello, world!"]  # Bob's wall includes Alice's post

def test_get_wall_merges_own_posts_with_followed_members():
    publish_post("Bob", "Bob's post")
    publish_post("Alice", "Alice's post")
    follow_member("Bob", "Alice")
    # Bob's wall should include his own post and Alice's post, most recent first
    assert get_wall("Bob") == ["Alice: Alice's post", "Bob: Bob's post"]  # Merged wall

def test_get_wall_excludes_unfollowed_members_posts():
    publish_post("Alice", "Hello, world!")
    follow_member("Bob", "Charlie")
    # Bob should not see Alice's post on his wall
    assert get_wall("Bob") == []  # Only follows Charlie, no posts

def test_following_is_one_directional():
    publish_post("Alice", "Hello, world!")
    follow_member("Bob", "Alice")
    # Alice's wall should include her own posts
    assert get_wall("Alice") == ["Alice: Hello, world!"]  # Alice's own post included, Bob's posts not

def test_following_twice_creates_no_duplicate_wall_entries():
    publish_post("Alice", "Hello, world!")
    follow_member("Bob", "Alice")
    follow_member("Bob", "Alice")  # Following again
    assert get_wall("Bob") == ["Alice: Hello, world!"]  # No duplicates

def test_get_wall_is_empty_if_no_posts_and_no_follows():
    assert get_wall("Bob") == []  # No posts, no follows

def test_mentioning_a_member_posts_to_their_wall():
    publish_post("Alice", "Hello @Bob!")
    # Bob's wall should include the mention
    assert get_wall("Bob") == ["Alice: Hello @Bob!"]  # Post appears on Bob's wall
    assert get_timeline("Bob") == []  # Bob's timeline is still empty

def test_mentioning_a_member_with_punctuation():
    publish_post("Alice", "Hello @Bob!")
    publish_post("Alice", "Another mention @Bob.")
    # Bob should see both mentions
    assert get_wall("Bob") == ["Alice: Another mention @Bob.", "Alice: Hello @Bob!"]  # Both mentions

def test_post_with_mention_does_not_appear_on_timeline():
    publish_post("Alice", "Hello @Bob!")
    assert get_timeline("Alice") == ["Hello @Bob!"]  # Post is on Alice's timeline

def test_send_direct_message_delivers_to_inbox():
    send_direct_message("Alice", "Bob", "Hello Bob!")
    # Bob's inbox should contain the direct message
    assert get_inbox("Bob") == ["Alice: Hello Bob!"]  # Message in inbox

def test_get_inbox_is_ordered_most_recent_first():
    send_direct_message("Alice", "Bob", "First message")
    send_direct_message("Alice", "Bob", "Second message")
    # Bob's inbox should show the latest message first
    assert get_inbox("Bob") == ["Alice: Second message", "Alice: First message"]  # Newest first

def test_direct_messages_are_private():
    send_direct_message("Alice", "Bob", "Hello Bob!")
    # Both Alice's and Bob's timelines and walls should remain empty
    assert get_timeline("Alice") == []  # No messages in Alice's timeline
    assert get_wall("Alice") == []  # No messages in Alice's wall
    assert get_timeline("Bob") == []  # No messages in Bob's timeline
    assert get_wall("Bob") == []  # No messages in Bob's wall

def test_get_inbox_is_empty_for_member_with_no_messages():
    assert get_inbox("Bob") == []  # No direct messages

def test_clock_ordering():
    publish_post("Alice", "Post 1")
    publish_post("Alice", "Post 2")
    publish_post("Alice", "Post 3")
    assert get_timeline("Alice") == ["Post 2", "Post 1", "Post 3"]  # Post 2 first, then Post 1, then Post 3

def test_equal_timestamp_ordering():
    publish_post("Alice", "Post A")
    publish_post("Alice", "Post B")  # Same timestamp
    assert get_timeline("Alice") == ["Post B", "Post A"]  # Latest posted first

def test_fake_clock_ordering():
    publish_post("Alice", "Post 1")
    publish_post("Bob", "Post 2")
    publish_post("Alice", "Post 3")
    assert get_timeline("Alice") == ["Post 3", "Post 1"]  # Latest post first

    follow_member("Alice", "Bob")
    assert get_wall("Alice") == ["Bob: Post 2"]  # Bob's post on Alice's wall