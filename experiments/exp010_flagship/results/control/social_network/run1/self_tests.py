from solution import SocialNetwork

def test_publishing_to_personal_timeline():
    network = SocialNetwork()
    network.publish("Hello, world!", "Alice", 1)
    timeline = network.get_timeline("Alice")
    
    # AC-1.1: "Hello, world!" appears on Alice's timeline
    assert timeline == ["Hello, world!"]
    
    # AC-1.2: Independent timelines
    timeline_bob = network.get_timeline("Bob")
    assert timeline_bob == []
    
    # AC-1.3: Order most recent first (already is since single post)
    network.publish("Another post!", "Alice", 2)
    timeline = network.get_timeline("Alice")
    assert timeline == ["Another post!", "Hello, world!"]
    
    # AC-1.4: Empty timeline for members who never posted
    assert network.get_timeline("Charlie") == []

def test_following_members_and_reading_wall():
    network = SocialNetwork()
    network.publish("Hello, world!", "Alice", 1)
    network.publish("Good morning!", "Bob", 2)
    network.follow("Alice", "Bob")
    
    wall = network.get_wall("Alice")
    # AC-2.1: Wall entry format for own posts
    assert wall == ["Alice: Hello, world!", "Bob: Good morning!"]

    # AC-2.2: Following makes Bob's posts appear on Alice's wall
    network.publish("Another post by Bob!", "Bob", 3)
    wall = network.get_wall("Alice")
    assert wall == ["Alice: Hello, world!", "Bob: Another post by Bob!", "Bob: Good morning!"]

    # AC-2.3: Merging own posts with followed members' posts
    network.publish("Alice's new post!", "Alice", 4)
    wall = network.get_wall("Alice")
    assert wall == ["Alice: Alice's new post!", "Bob: Another post by Bob!", "Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.4: Posts by non-followed members should not appear
    network.publish("Post from Charlie", "Charlie", 5)
    wall = network.get_wall("Alice")
    assert wall == ["Alice: Alice's new post!", "Bob: Another post by Bob!", "Bob: Good morning!", "Alice: Hello, world!"]

    # AC-2.5: Following is one-directional
    wall_bob = network.get_wall("Bob")
    assert wall_bob == ["Bob: Another post by Bob!", "Bob: Good morning!"]

    # AC-2.6: No duplicates on wall
    network.follow("Alice", "Bob")
    wall_bob = network.get_wall("Bob")
    assert wall_bob == ["Bob: Another post by Bob!", "Bob: Good morning!"]

    # AC-2.7: Empty wall for member with no posts and no follows
    assert network.get_wall("Charlie") == []

def test_reaching_members_through_mentions():
    network = SocialNetwork()
    network.publish("Hello @Bob!", "Alice", 1)
    network.publish("Hi @Alice!", "Bob", 2)
    
    wall_bob = network.get_wall("Bob")
    # AC-3.1: Mentioned post appears on Bob's wall
    assert wall_bob == ["Alice: Hello @Bob!"]

    # AC-3.2: Punctuation after mention does not break it
    network.publish("Hey @Bob!!!", "Alice", 3)
    wall_bob = network.get_wall("Bob")
    assert wall_bob == ["Alice: Hey @Bob!!!", "Alice: Hello @Bob!"]

    # AC-3.3: Mention does not appear on Alice's timeline
    timeline_alice = network.get_timeline("Alice")
    assert timeline_alice == ["Hello @Bob!", "Hi @Alice!"]

def test_exchanging_direct_messages():
    network = SocialNetwork()
    network.send_direct_message("Alice", "Bob", "Hey there!", 1)
    
    inbox_bob = network.get_inbox("Bob")
    # AC-4.1: Direct message is delivered correctly
    assert inbox_bob == ["Alice: Hey there!"]
    
    # AC-4.2: Messages should be ordered most recent first
    network.send_direct_message("Alice", "Bob", "How are you?", 2)
    inbox_bob = network.get_inbox("Bob")
    assert inbox_bob == ["Alice: How are you?", "Alice: Hey there!"]

    # AC-4.3: Direct messages are private
    timeline_alice = network.get_timeline("Alice")
    assert timeline_alice == []
    wall_bob = network.get_wall("Bob")
    assert wall_bob == []

    # AC-4.4: Empty inbox for member with no direct messages
    assert network.get_inbox("Charlie") == []

def test_ordering_by_the_clock():
    network = SocialNetwork()
    network.publish("First post", "Alice", 1)
    network.publish("Second post", "Alice", 2)
    
    # AC-5.1: Ordering by timestamps instead of order of insertion
    network.publish("Third post", "Alice", 0)
    timeline = network.get_timeline("Alice")
    assert timeline == ["Second post", "First post", "Third post"]

    # AC-5.2: Entries with same timestamp ordered latest-posted first
    network.publish("Duplicate timestamp post", "Alice", 2)
    timeline = network.get_timeline("Alice")
    assert timeline == ["Duplicate timestamp post", "Second post", "First post", "Third post"]