class Calculator:
    def __init__(self):
        self.current_value = 0
        self.history = []
        self.redo_stack = []
        self.seeded = False
        self.saved = False

    def seed(self, value):
        if not self.seeded:
            self.current_value = value
            self.history.append(('seed', value))
            self.seeded = True
        return self

    def add(self, value):
        if self.seeded and isinstance(value, int) and not self.saved:
            self.current_value += value
            self.history.append(('add', value))
            self.redo_stack.clear()
        return self

    def subtract(self, value):
        if self.seeded and isinstance(value, int) and not self.saved:
            self.current_value -= value
            self.history.append(('subtract', value))
            self.redo_stack.clear()
        return self

    def result(self):
        return self.current_value

    def undo(self):
        if self.history:
            last_action = self.history.pop()
            action_type, value = last_action
            if action_type == 'seed':
                return  # Prevent changing current_value after seeding
            elif action_type == 'add':
                self.current_value -= value
            elif action_type == 'subtract':
                self.current_value += value
            self.redo_stack.append(last_action)
        return self

    def redo(self):
        if self.saved:
            return self
        if self.redo_stack:
            last_action = self.redo_stack.pop()
            action_type, value = last_action
            if action_type == 'add':
                self.current_value += value
            elif action_type == 'subtract':
                self.current_value -= value
            self.history.append(last_action)
        return self

    def save(self):
        self.saved = True
        self.redo_stack.clear()  # Clear redo stack on save
        return self