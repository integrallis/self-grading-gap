from solution import publish_post, follow_member, get_timeline, get_wall, send_direct_message, get_inbox

def test_publishing_to_personal_timeline():
    # AC-1.1
    publish_post("Alice", "Hello World!", 1)
    assert get_timeline("Alice") == ["Hello World!"]  # Alice's post should appear on her timeline

    # AC-1.2
    publish_post("Bob", "Goodbye World!", 2)
    assert get_timeline("Alice") == ["Hello World!"]  # Alice's timeline should not include Bob's post

    # AC-1.3
    publish_post("Alice", "Second post", 3)
    assert get_timeline("Alice") == ["Second post", "Hello World!"]  # Most recent first

    # AC-1.4
    assert get_timeline("Charlie") == []  # Charlie has never posted, so timeline should be empty

def test_following_members_and_reading_a_wall():
    publish_post("Alice", "Hello World!", 1)
    publish_post("Bob", "Goodbye World!", 2)
    publish_post("Charlie", "How are you?", 3)

    follow_member("Alice", "Bob")
    
    # AC-2.1
    assert get_wall("Alice") == ["Bob: Goodbye World!", "Alice: Hello World!"]  # Alice's wall should include her and Bob's post

    # AC-2.2
    follow_member("Alice", "Charlie")
    assert get_wall("Alice") == ["Charlie: How are you?", "Bob: Goodbye World!", "Alice: Hello World!"]  # All followed posts should be included

    # AC-2.3
    publish_post("Bob", "Another post", 4)
    assert get_wall("Alice") == ["Bob: Another post", "Charlie: How are you?", "Bob: Goodbye World!", "Alice: Hello World!"]  # Most recent first
    
    # AC-2.4
    publish_post("David", "Not followed", 5)
    assert get_wall("Alice") == ["Bob: Another post", "Charlie: How are you?", "Bob: Goodbye World!", "Alice: Hello World!"]  # David's post should not appear

    # AC-2.5
    assert get_wall("Bob") == ["Bob: Another post", "Bob: Goodbye World!"]  # Bob's wall should only include his posts

    # AC-2.6
    follow_member("Alice", "Bob")  # Following Bob again should not create duplicate entries
    assert get_wall("Alice") == ["Bob: Another post", "Charlie: How are you?", "Bob: Goodbye World!", "Alice: Hello World!"]

    # AC-2.7
    assert get_wall("Eve") == []  # Eve has no posts and follows no one

def test_reaching_members_through_mentions():
    publish_post("Alice", "Hello @Bob!", 1)
    publish_post("Alice", "Hello @Charlie!", 2)

    # AC-3.1
    assert get_wall("Bob") == ["Alice: Hello @Bob!"]  # Bob should see the mention on his wall

    # AC-3.2
    publish_post("Alice", "Hello @Bob!!!", 3)  # Punctuation after mention
    assert get_wall("Bob") == ["Alice: Hello @Bob!!!", "Alice: Hello @Bob!"]  # Should still recognize mention

    # AC-3.3
    assert get_timeline("Bob") == []  # Bob's timeline should remain empty

def test_exchanging_direct_messages():
    send_direct_message("Alice", "Bob", "Hi Bob!", 1)
    send_direct_message("Alice", "Bob", "How are you?", 2)

    # AC-4.1
    assert get_inbox("Bob") == ["Alice: How are you?", "Alice: Hi Bob!"]  # Bob's inbox should contain messages from Alice

    # AC-4.2
    send_direct_message("Alice", "Bob", "Last message", 3)
    assert get_inbox("Bob") == ["Alice: Last message", "Alice: How are you?", "Alice: Hi Bob!"]  # Most recent first

    # AC-4.3
    assert get_wall("Alice") == []  # Messages should not appear on Alice's wall
    assert get_wall("Bob") == []  # Messages should not appear on Bob's wall

    # AC-4.4
    assert get_inbox("Charlie") == []  # Charlie has received no messages, inbox should be empty

def test_ordering_everything_by_the_clock():
    publish_post("Alice", "Post 1", 1)
    publish_post("Alice", "Post 2", 2)
    publish_post("Alice", "Post 3", 1)  # Same timestamp as Post 1

    # AC-5.1
    assert get_timeline("Alice") == ["Post 2", "Post 3", "Post 1"]  # Ordered by timestamp

    # AC-5.2
    publish_post("Alice", "Post 4", 2)
    assert get_timeline("Alice") == ["Post 4", "Post 2", "Post 3", "Post 1"]  # Latest-posted first for same timestamp

    # Testing clock ordering
    publish_post("Alice", "Post 5", 5)
    publish_post("Alice", "Post 6", 4)
    assert get_timeline("Alice") == ["Post 5", "Post 6", "Post 4", "Post 2", "Post 3", "Post 1"]  # Ordered by clock timestamps

    # Additional tests for wall with timestamps
    follow_member("Alice", "Bob")
    publish_post("Bob", "Bob's first post", 3)
    assert get_wall("Alice") == ["Bob: Bob's first post", "Alice: Post 5", "Alice: Post 6", "Alice: Post 4", "Alice: Post 2", "Alice: Post 3", "Alice: Post 1"]  # Wall should respect timestamps

    publish_post("Bob", "Bob's second post", 4)
    assert get_wall("Alice") == ["Bob: Bob's second post", "Bob: Bob's first post", "Alice: Post 5", "Alice: Post 6", "Alice: Post 4", "Alice: Post 2", "Alice: Post 3", "Alice: Post 1"]  # Wall should respect timestamps and be most recent first