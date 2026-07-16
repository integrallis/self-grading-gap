from solution import publish_post, get_timeline, follow_member, get_wall, send_direct_message, get_inbox

import pytest

@pytest.fixture(autouse=True)
def reset_network():
    # Assume a function to reset the network state exists
    # This should be called before each test to ensure isolation
    reset_network_state()

def test_publish_post_creates_own_timeline():
    publish_post("Alice", "Hello world!", timestamp=1)
    assert get_timeline("Alice") == ["Hello world!"]  # AC-1.1

def test_get_timeline_only_shows_own_posts():
    publish_post("Alice", "Hello world!", timestamp=1)
    publish_post("Bob", "Goodbye world!", timestamp=2)
    assert get_timeline("Alice") == ["Hello world!"]  # AC-1.2

def test_get_timeline_is_ordered_most_recent_first():
    publish_post("Alice", "Post 1", timestamp=1)
    publish_post("Alice", "Post 2", timestamp=2)
    assert get_timeline("Alice") == ["Post 2", "Post 1"]  # AC-1.3

def test_get_timeline_is_empty_for_no_posts():
    assert get_timeline("Alice") == []  # AC-1.4

def test_follow_member_adds_posts_to_wall():
    publish_post("Bob", "Hello from Bob!", timestamp=1)
    follow_member("Alice", "Bob")
    assert get_wall("Alice") == ["Bob: Hello from Bob!"]  # AC-2.2

def test_wall_combines_own_posts_with_followed_members():
    publish_post("Alice", "My post", timestamp=2)
    publish_post("Bob", "Bob's post", timestamp=1)
    follow_member("Alice", "Bob")
    assert get_wall("Alice") == ["Alice: My post", "Bob: Bob's post"]  # AC-2.3

def test_wall_excludes_unfollowed_members_posts():
    publish_post("Bob", "Bob's post", timestamp=1)
    follow_member("Alice", "Charlie")
    assert get_wall("Alice") == []  # AC-2.4

def test_following_is_one_directional():
    publish_post("Alice", "Alice's post", timestamp=1)
    follow_member("Alice", "Bob")
    assert get_wall("Bob") == []  # AC-2.5

def test_following_twice_does_not_duplicate_wall_entries():
    publish_post("Bob", "Bob's post", timestamp=1)
    follow_member("Alice", "Bob")
    follow_member("Alice", "Bob")
    assert get_wall("Alice") == ["Bob: Bob's post"]  # AC-2.6

def test_wall_is_empty_for_no_posts_and_no_follows():
    assert get_wall("Alice") == []  # AC-2.7

def test_post_with_mention_appears_on_mentioned_member_wall():
    publish_post("Alice", "Hello @Bob!", timestamp=1)
    assert get_wall("Bob") == ["Alice: Hello @Bob!"]  # AC-3.1

def test_mention_with_punctuation():
    publish_post("Alice", "Hello @Bob!", timestamp=1)
    publish_post("Alice", "Great day @Bob.", timestamp=2)
    assert get_wall("Bob") == ["Alice: Great day @Bob.", "Alice: Hello @Bob!"]  # AC-3.2

def test_mentions_do_not_appear_on_timeline():
    publish_post("Alice", "Hello @Bob!", timestamp=1)
    assert get_timeline("Bob") == []  # AC-3.3

def test_send_direct_message_creates_inbox_entry():
    send_direct_message("Alice", "Bob", "Hello Bob!", timestamp=1)
    assert get_inbox("Bob") == ["Alice: Hello Bob!"]  # AC-4.1

def test_inbox_is_ordered_most_recent_first():
    send_direct_message("Alice", "Bob", "Old message", timestamp=1)
    send_direct_message("Alice", "Bob", "New message", timestamp=2)
    assert get_inbox("Bob") == ["Alice: New message", "Alice: Old message"]  # AC-4.2

def test_direct_messages_are_private():
    send_direct_message("Alice", "Bob", "Hello Bob!", timestamp=1)
    assert get_timeline("Alice") == []  # AC-4.3
    assert get_wall("Bob") == []  # AC-4.3
    assert get_timeline("Bob") == []  # AC-4.3

def test_inbox_is_empty_for_no_messages():
    assert get_inbox("Bob") == []  # AC-4.4

def test_recency_by_clock_timestamps():
    publish_post("Alice", "Post A", timestamp=2)
    publish_post("Alice", "Post B", timestamp=1)
    assert get_timeline("Alice") == ["Post A", "Post B"]  # AC-5.1

def test_entries_with_same_timestamp_order_latest_posted_first():
    publish_post("Alice", "Post A", timestamp=1)
    publish_post("Alice", "Post B", timestamp=1)
    assert get_timeline("Alice") == ["Post B", "Post A"]  # AC-5.2

def test_wall_combines_posts_with_out_of_order_timestamps():
    publish_post("Alice", "My post", timestamp=2)
    publish_post("Bob", "Bob's post", timestamp=1)
    follow_member("Alice", "Bob")
    assert get_wall("Alice") == ["Alice: My post", "Bob: Bob's post"]  # AC-2.3

def test_inbox_combines_direct_messages_with_out_of_order_timestamps():
    send_direct_message("Alice", "Bob", "Old message", timestamp=2)
    send_direct_message("Alice", "Bob", "New message", timestamp=1)
    assert get_inbox("Bob") == ["Alice: New message", "Alice: Old message"]  # AC-4.2