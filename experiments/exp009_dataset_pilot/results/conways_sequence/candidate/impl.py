# candidate/impl.py

class LookAndSay:
    @staticmethod
    def next_term(term: str) -> str:
        if not term or not term.isdigit():
            raise ValueError("term must be a non-empty string of digits")
        
        result = []
        count = 1
        
        for i in range(1, len(term)):
            if term[i] == term[i - 1]:
                count += 1
            else:
                result.append(f"{count}{term[i - 1]}")
                count = 1
        
        result.append(f"{count}{term[-1]}")
        return ''.join(result)

    @staticmethod
    def iterate(seed: str, iterations: int) -> str:
        if iterations < 0:
            raise ValueError("iterations must be non-negative")
        if not seed or not seed.isdigit():
            raise ValueError("term must be a non-empty string of digits")
        
        current_term = seed
        for _ in range(iterations):
            current_term = LookAndSay.next_term(current_term)
        
        return current_term
