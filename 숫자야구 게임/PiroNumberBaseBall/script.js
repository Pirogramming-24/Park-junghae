const MAX_ATTEMPTS = 9;

let answer = [];
let attemptsLeft = MAX_ATTEMPTS;
let gameOver = false;

document.addEventListener("DOMContentLoaded", () => {
  initGame();
});

// 초기화
function initGame() {
  attemptsLeft = MAX_ATTEMPTS;
  gameOver = false;

  answer = generateRandomNumbers(3);

  clearInputs();
  document.getElementById("results").innerHTML = "";
  document.getElementById("game-result-img").src = "";
  updateAttemptsText();

  const submitButton = document.querySelector(".submit-button");
  submitButton.disabled = false;
  submitButton.style.cursor = "pointer";
}

// 0~9 중복되지 않는 숫자 생성
function generateRandomNumbers(count) {
  const nums = [];
  while (nums.length < count) {
    const digit = Math.floor(Math.random() * 10);
    if (!nums.includes(digit)) nums.push(digit);
  }
  return nums;
}

// 버튼 클릭 시 실행
function check_numbers() {
  if (gameOver) return;

  const n1 = document.getElementById("number1").value;
  const n2 = document.getElementById("number2").value;
  const n3 = document.getElementById("number3").value;

  if (n1 === "" || n2 === "" || n3 === "") {
    clearInputs();
    return;
  }

  const guess = [Number(n1), Number(n2), Number(n3)];

  let strikes = 0;
  let balls = 0;

  for (let i = 0; i < 3; i++) {
    if (guess[i] === answer[i]) strikes++;
    else if (answer.includes(guess[i])) balls++;
  }

  let resultText = "";
  let isOut = false;

  if (strikes === 0 && balls === 0) {
    resultText = "O";
    isOut = true;
  } else {
    resultText = `${strikes} S ${balls} B`;
  }

  printResultLine(guess, resultText, isOut);

  attemptsLeft--;
  updateAttemptsText();

  checkGameEnd(strikes);

  clearInputs();
}

// 결과 표시 + 색상 적용
function printResultLine(guessArray, resultText, isOut) {
  const resultsDiv = document.getElementById("results");

  const line = document.createElement("div");
  line.classList.add("check-result");

  const leftSpan = document.createElement("span");
  leftSpan.classList.add("left");
  leftSpan.textContent = guessArray.join(" ");

  const rightSpan = document.createElement("span");
  rightSpan.classList.add("right");

  if (isOut) {
    const outSpan = document.createElement("span");
    outSpan.classList.add("num-result", "out");
    outSpan.textContent = "O";
    rightSpan.appendChild(outSpan);
  } else {
    const [strikeCnt, , ballCnt] = resultText.split(" ");

    const sSpan = document.createElement("span");
    sSpan.classList.add("num-result", "strike");
    sSpan.textContent = strikeCnt + "S";

    const bSpan = document.createElement("span");
    bSpan.classList.add("num-result", "ball");
    bSpan.textContent = ballCnt + "B";

    rightSpan.appendChild(sSpan);
    rightSpan.appendChild(bSpan);
  }

  line.appendChild(leftSpan);
  line.appendChild(rightSpan);

  resultsDiv.appendChild(line);
}

// 남은 횟수 표시
function updateAttemptsText() {
  document.getElementById("attempts").textContent = attemptsLeft;
}

// 승패 처리
function checkGameEnd(strikes) {
  const resultImg = document.getElementById("game-result-img");
  const submitButton = document.querySelector(".submit-button");

  if (strikes === 3) {
    resultImg.src = "success.png";
    gameOver = true;
  } else if (attemptsLeft === 0) {
    resultImg.src = "fail.png";
    gameOver = true;
  }

  if (gameOver) {
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  }
}

// input 초기화
function clearInputs() {
  const n1 = document.getElementById("number1");
  const n2 = document.getElementById("number2");
  const n3 = document.getElementById("number3");

  n1.value = "";
  n2.value = "";
  n3.value = "";
  n1.focus();
}
