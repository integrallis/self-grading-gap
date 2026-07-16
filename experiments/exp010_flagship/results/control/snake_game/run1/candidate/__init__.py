class Game:
    def __init__(self, width, height, food_positions):
        if width <= 0 or height <= 0:
            raise ValueError("grid dimensions must be positive")
        self.width = width
        self.height = height
        self.food_positions = food_positions
        self.snake = [(0, 0)]
        self.heading = 'right'
        self.score = 0
        self.is_game_over = False
        self.food = self.food_positions.pop(0) if self.food_positions else None

    def change_heading(self, new_heading):
        valid_directions = {'up', 'down', 'left', 'right'}
        if new_heading not in valid_directions:
            raise ValueError(f"unknown direction: '{new_heading}'")
        # Prevent reversing direction
        if (self.heading == 'up' and new_heading == 'down') or \
           (self.heading == 'down' and new_heading == 'up') or \
           (self.heading == 'left' and new_heading == 'right') or \
           (self.heading == 'right' and new_heading == 'left'):
            return
        self.heading = new_heading

    def tick(self):
        if self.is_game_over:
            return
        head_x, head_y = self.snake[0]
        if self.heading == 'up':
            head_y -= 1
        elif self.heading == 'down':
            head_y += 1
        elif self.heading == 'left':
            head_x -= 1
        elif self.heading == 'right':
            head_x += 1

        # Check for collisions with walls
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.is_game_over = True
            return

        # Check for collisions with self
        if (head_x, head_y) in self.snake:
            self.is_game_over = True
            return

        # Move the snake
        self.snake.insert(0, (head_x, head_y))

        # Check for food
        if (head_x, head_y) == self.food:
            self.score += 1
            if self.food_positions:
                self.food = self.food_positions.pop(0)
            else:
                self.food = None
        else:
            self.snake.pop()  # Remove tail if no food eaten

    def __str__(self):
        return f"Snake: {self.snake}, Score: {self.score}, Food: {self.food}, Game Over: {self.is_game_over}"