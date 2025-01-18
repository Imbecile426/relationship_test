$(document).ready(function() {
    let currentQuestion = 0;
    const questions = [
        "What is your favorite color?",
        "What is your favorite hobby?",
        "What is your favorite cuisine?",
        "What is your dream travel destination?",
        "What is your favorite movie genre?",
        "What kind of music do you enjoy most?",
        "What is your favorite season?",
        "What is your favorite animal?",
        "What is your favorite type of sport?",
        "What is your favorite book or author?"
    ];
    const responses = [];

    $('#start-quiz').on('submit', function(event) {
        event.preventDefault();
        const name1 = $('#name1').val();
        const dob1 = $('#dob1').val();
        const name2 = $('#name2').val();
        const dob2 = $('#dob2').val();

        // Trigger GitHub Action to store participant data
        $.ajax({
            url: 'https://api.github.com/repos/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/store-data.yml/dispatches',
            type: 'POST',
            headers: {
                'Authorization': 'token YOUR_GITHUB_TOKEN',
                'Accept': 'application/vnd.github.v3+json'
            },
            data: JSON.stringify({
                ref: 'main',
                inputs: {
                    name1: name1,
                    dob1: dob1,
                    name2: name2,
                    dob2: dob2
                }
            }),
            success: function() {
                console.log('Participant data stored successfully');
            },
            error: function(error) {
                console.error('Error storing participant data: ', error);
            }
        });

        $('#participant-info').hide();
        showQuestion();
    });

    function showQuestion() {
        if (currentQuestion < questions.length) {
            $('#question').text(questions[currentQuestion]);
            $('#quiz').show();
        } else {
            showResult();
        }
    }

    $('#quiz').on('submit', function(event) {
        event.preventDefault();
        const yourAnswer = $('#your_answer').val();
        const partnerAnswer = $('#partner_answer').val();
        responses.push({ yourAnswer, partnerAnswer });

        currentQuestion++;
        $('#your_answer').val('');
        $('#partner_answer').val('');
        showQuestion();
    });

    function showResult() {
        $('#quiz').hide();
        const result = Math.random() < 0.5 ? "Not Compatible" : "Extremely Incompatible";
        $('#result').html(`<h2>Result: ${result}</h2>`);
        $('#result').show();
    }

    $('#retry').on('click', function() {
        currentQuestion = 0;
        responses.length = 0;
        $('#result').hide();
        $('#participant-info').show();
    });
});