from solution import publish_post, follow_member, get_timeline, get_wall, send_direct_message, get_inbox

# Fixture to create a fresh network for each test
def reset_network():
    # Assuming there is a function to reset the network state
    pass  # Replace with actual reset logic if needed

def test_publishing_to_personal_timeline():
    reset_network()
    # AC-1.1: A posted message appears on its author's timeline.
    publish_post("Alice", "Hello World!", 1)
    assert get_timeline("Alice") == ["Hello World!"]  # Alice's timeline should contain her post.

    # AC-1.2: A timeline lists only that member's own posts; different members' timelines are independent.
    publish_post("Bob", "Goodbye World!", 2)
    assert get_timeline("Alice") == ["Hello World!"]  # Alice's timeline should not contain Bob's post.

    # AC-1.3: A timeline is ordered most recent first.
    publish_post("Alice", "Another post!", 3)
    assert get_timeline("Alice") == ["Another post!", "Hello World!"]  # Most recent first.

    # AC-1.4: A member who has never posted has an empty timeline.
    assert get_timeline("Charlie") == []  # Charlie has no posts.

def test_following_members_and_reading_a_wall():
    reset_network()
    publish_post("Alice", "Hello World!", 1)
    publish_post("Bob", "Goodbye World!", 2)
    follow_member("Alice", "Bob")

    # AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message.
    assert get_wall("Alice") == ["Alice: Hello World!", "Bob: Goodbye World!"]  # Correct formatting.

    # AC-2.2: After following a member, that member's posts appear on the follower's wall.
    # Already checked in the previous assertion.

    # AC-2.3: A wall merges the member's own posts with all followed members' posts, most recent first.
    publish_post("Alice", "Another post!", 3)
    assert get_wall("Alice") == ["Alice: Another post!", "Bob: Goodbye World!", "Alice: Hello World!"]  # Most recent first.

    # AC-2.4: Posts by members who are not followed stay off the wall.
    publish_post("Charlie", "Hey there!", 4)
    assert get_wall("Alice") == ["Alice: Another post!", "Bob: Goodbye World!", "Alice: Hello World!"]  # Charlie's post not included.

    # AC-2.5: Following is one-directional.
    assert get_wall("Bob") == []  # Bob's wall should not include any posts since he has none.

    # AC-2.6: Following the same member twice creates no duplicate wall entries.
    follow_member("Alice", "Bob")  # Follow again
    assert get_wall("Alice") == ["Alice: Another post!", "Bob: Goodbye World!", "Alice: Hello World!"]  # No duplicates.

    # AC-2.7: A member with no posts and no follows has an empty wall.
    assert get_wall("Charlie") == []  # Charlie has neither posts nor follows.

def test_reaching_members_through_mentions():
    reset_network()
    publish_post("Alice", "Hello @Bob!", 1)
    publish_post("Bob", "Hi @Alice!", 2)
    
    # AC-3.1: A post containing a mention lands on that member's wall.
    assert get_wall("Bob") == ["Bob: Hi @Alice!", "Alice: Hello @Bob!"]  # Bob should see Alice's mention.

    # AC-3.2: Punctuation immediately after a mention does not break it.
    publish_post("Alice", "Hello @Bob!!!", 3)
    assert get_wall("Bob") == ["Alice: Hello @Bob!!!", "Bob: Hi @Alice!", "Alice: Hello @Bob!"]  # Bob should see this post with punctuation.

    # AC-3.3: Mentions affect walls only; the post never appears on the mentioned member's timeline.
    assert get_timeline("Bob") == ["Hi @Alice!"]  # Bob's timeline should remain with his own post.

def test_exchanging_direct_messages():
    reset_network()
    send_direct_message("Alice", "Bob", "Hello Bob!", 1)
    
    # AC-4.1: A direct message is delivered to the recipient's inbox.
    assert get_inbox("Bob") == ["Alice: Hello Bob!"]  # Bob should receive Alice's message.

    # AC-4.2: An inbox lists direct messages most recent first.
    send_direct_message("Alice", "Bob", "Another message!", 2)
    assert get_inbox("Bob") == ["Alice: Another message!", "Alice: Hello Bob!"]  # Most recent first.

    # AC-4.3: Direct messages are private; they never appear on any timeline or wall.
    assert get_timeline("Alice") == []  # Alice's timeline should be empty.
    assert get_wall("Bob") == []  # Bob's wall should not include any posts.

    # AC-4.4: A member who has received no direct messages has an empty inbox.
    assert get_inbox("Charlie") == []  # Charlie has no messages.

def test_ordering_by_the_clock():
    reset_network()
    publish_post("Alice", "Post 1", 1)  # timestamp 1
    publish_post("Alice", "Post 2", 2)  # timestamp 2
    publish_post("Alice", "Post 3", 1)  # timestamp 1 again, should appear later than Post 2

    # AC-5.1: Recency comes from the supplied clock's timestamps.
    assert get_timeline("Alice") == ["Post 2", "Post 3", "Post 1"]  # Ordered by timestamp.

    publish_post("Alice", "Post 4", 3)  # timestamp 3
    assert get_timeline("Alice") == ["Post 4", "Post 2", "Post 3", "Post 1"]  # Most recent on top.

    # AC-5.2: Entries sharing the same timestamp are ordered latest-posted first.
    publish_post("Alice", "Post 5", 2)  # Another post at timestamp 2
    assert get_timeline("Alice") == ["Post 4", "Post 5", "Post 2", "Post 3", "Post 1"]  # Post 5 appears before Post 3.