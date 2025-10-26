const quizData = [
    {
        question:"че за рыло?",
        images:[
            "зубы.jpg",
            "https://via.placeholder.com/200x150/2196F3/white?text=Фото+2"
        ],
        options: ["Гурка","БАГИРАУ","Фьюрер, Генералиссимус Приходько", "просто саня"],
        correctAnswer: 3
    },
    {
        question:"че за рыло?",
        images:[
            "гураль.jpg",
            "https://via.placeholder.com/200x150/2196F3/white?text=Фото+2"
        ],
        options: ["Гурка","ЗАХАРАУ","Фьюрер, Генералиссимус Приходько", "просто саня"],
        correctAnswer: 0
    },
    {
        question:"че за рыло?",
        images:[
            "вая_каса.jpg",
            "https://via.placeholder.com/200x150/2196F3/white?text=Фото+2"
        ],
        options: ["Гурка","БАГИРАУ","Фьюрер, Генералиссимус Приходько", "просто саня"],
        correctAnswer: 1
    },
];

let currentQuestion = 0;
let score = 0;

const questionElement = document.getElementById('question');
const image1Element = document.getElementById('image1');
const image2Element = document.getElementById('image2');
const progressElement = document.getElementById('progress');
const buttons = document.querySelectorAll('.quiz-button');
const feedbackElement = document.getElementById('feedback');
const quizSection = document.getElementById('quiz-section');
const resultSection = document.getElementById('result-section');

function loadQuestion() {
    const currentQuiz = quizData[currentQuestion];

    questionElement.textContent = currentQuiz.question;
    image1Element.src = currentQuiz.images[0];
    image1Element.alt = `Фото 1 для вопроса ${currentQuestion + 1}`;
    image2Element.src = currentQuiz.images[1];
    image2Element.alt = `Фото 2 для вопроса ${currentQuestion + 1}`;
    
    buttons.forEach((button, index) => {
        button.textContent = currentQuiz.options[index];
        button.dataset.correct = (index === currentQuiz.correctAnswer).toString();
        button.classList.remove('wrong');
        button.disabled = false;
        button.style.background = ''; // Сбрасываем цвет фона
    });
    
    progressElement.textContent = `Пытанне ${currentQuestion + 1} з ${quizData.length}`;
    feedbackElement.textContent = '';
    feedbackElement.className = 'feedback';
}

function checkAnswer(selectedButton) {
    const isCorrect = selectedButton.dataset.correct === 'true';
    
    buttons.forEach(button => {
        button.disabled = true;
        if (button.dataset.correct === 'true') {
            button.style.background = '#4CAF50';
        } else if (button === selectedButton && !isCorrect) {
            button.classList.add('wrong');
        }
    });

    if (isCorrect) {
        score++;
        feedbackElement.textContent = 'Правiльна!';
        feedbackElement.className = 'feedback correct-feedback';
    } else {
        feedbackElement.textContent = 'Няправiльна! Паспрабуй наступнае пытанне.';
        feedbackElement.className = 'feedback wrong-feedback';
    }

    setTimeout(() => {
        currentQuestion++;
        if (currentQuestion < quizData.length) {
            loadQuestion();
        } else {
            showResult();
        }
    }, 1500);
}

function showResult() {
    quizSection.style.display = 'none';
    resultSection.style.display = 'block';
    
    const resultTitle = document.querySelector('.result-title');
    resultTitle.textContent = `Ты набраў ${score} з ${quizData.length} балаў!`;
}

function restartQuiz() {
    currentQuestion = 0;
    score = 0;
    quizSection.style.display = 'block';
    resultSection.style.display = 'none';
    loadQuestion();
}

buttons.forEach(button => {
    button.addEventListener('click', () => checkAnswer(button));
});


loadQuestion();
