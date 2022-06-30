function calculate(scores) {
    var grade, scale;

    let sum = 0;

    for (let i = 0; i < scores.length; i++) {
        sum += scores[i];
    }

    grade = sum / scores.length;

    scale = {
        [90 <= grade && grade <= 100]: "O",
        [80 <= grade && grade < 90]: "E",
        [70 <= grade && grade < 80]: "A",
        [55 <= grade && grade < 70]: "P",
        [40 <= grade && grade < 55]: "D",
        [grade < 40]: "T"
    };
    console.log(scale.true);
}

calculate([100, 100, 90, 90, 80, 80, 70, 70, 60, 60, 50, 50])
