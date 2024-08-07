let questionNumber = 1;
let answeredCount = 0;

function nextQuestion() {
    questionNumber++;
    answeredCount++;
    updateQuestion();
}

function prevQuestion() {
    if (questionNumber > 1) {
        questionNumber--;
        updateQuestion();
    }
}

function updateQuestion() {
    document.getElementById('questionCount').textContent = answeredCount;
    document.getElementById('questionContainer').style.opacity = '0';
    setTimeout(() => {
        document.getElementById('currentQuestion').innerHTML = `
            <h2>Question ${questionNumber}</h2>
            <p>This is question ${questionNumber}. Replace with actual question content.</p>
        `;
        document.getElementById('options').innerHTML = `
            <div class="option" onclick="selectOption(this)"><div class="option-checkbox"></div>A) Option for Q${questionNumber}</div>
            <div class="option" onclick="selectOption(this)"><div class="option-checkbox"></div>B) Option for Q${questionNumber}</div>
            <div class="option" onclick="selectOption(this)"><div class="option-checkbox"></div>C) Option for Q${questionNumber}</div>
            <div class="option" onclick="selectOption(this)"><div class="option-checkbox"></div>D) Option for Q${questionNumber}</div>
        `;
        document.getElementById('questionContainer').style.opacity = '1';
    }, 300);

    document.getElementById('prevBtn').disabled = questionNumber === 1;
}

function selectOption(option) {
    const options = document.querySelectorAll('.option');
    options.forEach(opt => opt.classList.remove('selected'));
    option.classList.add('selected');
}

function showConfirmation() {
    document.getElementById('confirmationOverlay').style.display = 'flex';
}

function hideConfirmation() {
    document.getElementById('confirmationOverlay').style.display = 'none';
}

function submitQuiz() {
    hideConfirmation();
    calculateAndDisplayScore();
}

function calculateAndDisplayScore() {
    // This is a placeholder calculation. In a real scenario,
    // you'd calculate based on correct answers.
    const score = Math.floor(Math.random() * 31) + 70; // Random score between 70 and 100
    const totalQuestions = 100; // Assuming there are 100 questions total

    document.getElementById('scoreDisplay').textContent = `${score}/${totalQuestions}`;
    document.getElementById('scoreOverlay').style.display = 'flex';
}

function closeScoreOverlay() {
    document.getElementById('scoreOverlay').style.display = 'none';
    // You might want to redirect the user or perform other actions here
}

// Timer functionality
let seconds = 0;
function updateTimer() {
    seconds++;
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;
    document.getElementById('timer').textContent = 
        (hours < 10 ? "0" + hours : hours) + ":" +
        (minutes < 10 ? "0" + minutes : minutes) + ":" +
        (secs < 10 ? "0" + secs : secs);
}
setInterval(updateTimer, 1000);