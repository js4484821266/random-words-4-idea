const result = document.querySelector("#result");
const countInput = document.querySelector("#word-count");
const drawButton = document.querySelector("#draw-button");
const message = document.querySelector("#message");

let words = [];

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle("error", isError);
  message.setAttribute("role", isError ? "alert" : "status");
}

function readCount() {
  const rawValue = countInput.value.trim();
  const count = Number(rawValue);

  if (rawValue === "" || !Number.isInteger(count) || count < 1 || count > 100) {
    showMessage("단어 수는 1부터 100까지의 정수로 입력해 주세요.", true);
    return null;
  }

  return count;
}

function pickUniqueWords(count) {
  const pickedIndexes = new Set();

  while (pickedIndexes.size < count) {
    pickedIndexes.add(Math.floor(Math.random() * words.length));
  }

  return [...pickedIndexes].map((index) => words[index]);
}

function drawWords() {
  const count = readCount();

  if (count === null) {
    return;
  }

  result.textContent = pickUniqueWords(count).join("\n");
  showMessage("");
}

async function loadWords() {
  try {
    const response = await fetch("data/words.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const loadedWords = await response.json();
    if (!Array.isArray(loadedWords) || loadedWords.length < 100) {
      throw new Error("단어 데이터 형식이 올바르지 않습니다.");
    }

    words = loadedWords;
    countInput.disabled = false;
    drawButton.disabled = false;
    result.textContent = "단어를 뽑아 보세요";
    showMessage("");
  } catch (error) {
    console.error("단어 목록 로딩 실패:", error);
    result.textContent = "단어 목록을 불러오지 못했습니다";
    showMessage("페이지를 새로고침해 주세요. 문제가 계속되면 data/words.json을 확인하세요.", true);
  }
}

drawButton.addEventListener("click", drawWords);
countInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !drawButton.disabled) {
    drawWords();
  }
});

loadWords();
