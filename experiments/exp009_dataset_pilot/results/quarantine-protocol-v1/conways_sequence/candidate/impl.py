# candidate/impl.py

class LookAndSay:
    @staticmethod
    def next_term(term: str) -> str:
        if not LookAndSay._is_valid_term(term):
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
    def iterate(term: str, iterations: int) -> str:
        if iterations < 0:
            raise ValueError("iterations must be non-negative")
        if not LookAndSay._is_valid_term(term):
            raise ValueError("term must be a non-empty string of digits")
        
        for _ in range(iterations):
            term = LookAndSay.next_term(term)
        return term

    @staticmethod
    def _is_valid_term(term: str) -> bool:
        return bool(term) and term.isdigit()
