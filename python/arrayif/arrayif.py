def calculate(scores: list) -> str:
    grade = sum(scores) / len(scores)
    scale = {90 <= grade <= 100: "O", 80 <=
             grade < 90: "E", 70 <= grade < 80: "A",
             55 <= grade < 70: "P", 40 <= grade < 55: "D",
             grade < 40: "T"}
    return scale.get(True)


print(calculate([100, 100, 90, 90, 80, 80, 70, 70, 60, 60, 50, 50]))
