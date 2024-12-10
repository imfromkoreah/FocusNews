/*
 * 시스템 흐름
 * 
 * - 페이지 로드
 * showBotMessage : 초기 메시지(처음 페이지 접속시에만 표시)
 * showLoopBotMessages : 반복 메시지(루프 시작마다 표시)
 * showCategoryButtons : 카테고리 표시
 * sendMessage : 카테고리 선택 또는 키워드 입력
 * 
 * 
 * - 요소
 * botAccount : 포뉴 프로필
 * getLoadingDotsHTML : 로딩 애니메이션 HTML
 * 
 */



// 전역 변수
let yesButton, noButton
let uniqueLink;
let messageQueue = [];
let messageDelay = 1500;
let loadingTimeout;
let firstBotMessage = true;

const newsCategory = ["정치", "경제", "연예", "사회", "생활/문화", "IT/과학", "세계", "인기뉴스"];

// 페이지가 로드될 때 봇 메시지 로딩 애니메이션을 실행
window.onload = function() {
    showBotMessages();
};

// 엔터 키가 눌리면 sendMessage 호출
document
    .getElementById("chatInput")
    .addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            const chatInput = document.getElementById("chatInput");
            const message = chatInput.value; // 입력된 메시지를 message에 저장
            sendMessage(message);
        }
})

// 입력창 활성화
function showInputContainer() {
    const chatInput = document.getElementById("chatInput");
    chatInput.addEventListener("input", function () {
        const sendButton = document.getElementById("sendButton");

        if (chatInput.value.trim() === "") {
            sendButton.disabled = true; // 입력이 없으면 버튼 비활성화
        } else {
            sendButton.disabled = false; // 입력이 있으면 버튼 활성화
        }
    });

    chatInput.disabled = false;
}

// 로딩 애니메이션 HTML
function getLoadingDotsHTML() {
    return '<div class="loading-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
}

// 지정한 밀리초만큼 대기하는 함수, 기본 대기 1500밀리초
function delay(ms = 1500) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 슬라이더 로드 함수
function loadSlider() {
var iframe = document.getElementById('cardSlider');
iframe.src = '/slider';  // iframe에 src 설정
iframe.style.display = 'block';  // iframe을 보이도록 설정
}

// 봇 프로필
function botAccount(container) {
    if(firstBotMessage) {
        const profileContainer = document.createElement("div");
        profileContainer.classList.add("profile-container");
    
        const profile = document.createElement("img");
        profile.src = "../static/images/fnew.jpg"; // 프로필 이미지 경로
        profile.alt = "프로필 사진";
        profile.classList.add("profile"); // CSS 클래스 추가
    
        const profileName = document.createElement("div");
        profileName.classList.add("profile-name");
        profileName.textContent = "포뉴"; // 프로필 이름 설정
    
        profileContainer.appendChild(profile); // 프로필 사진 추가
        profileContainer.appendChild(profileName); // 프로필 이름 추가
    
        container.appendChild(profileContainer); // 프로필 컨테이너 추가

        firstBotMessage = false;
    }
}

// 초기 봇 메시지 로직
async function showBotMessages() {
    const container = document.getElementById("chat"); // 프로필을 추가할 컨테이너 요소
    botAccount(container);

    const initialMessage = '저는 뉴스를 보여주는 앵커 "포-뉴"입니당.';
    const msgElement = document.getElementById("msg1");

    // 초기 메시지 표시
    showMessageWithLoading(msgElement, initialMessage);

    await delay()

    // 초기 메시지 표시 후 반복 메시지 표시
    showLoopBotMessages();
}

// 반복되는 봇 메시지 로직
function showLoopBotMessages() {
    const container = document.getElementById("chat"); // 프로필을 추가할 컨테이너 요소
    botAccount(container);

    const loopMessages = [
        '키워드를 "선택" 혹은 "입력"하면 요약된 뉴스를 보여줄 거예요.',
        '궁금한 뉴스가 있다면...',
        '카테고리를 선택하거나, 검색어를 입력하세요.',
    ];
    const botMessages = [
        document.getElementById("msg2"),
        document.getElementById("msg3"),
        document.getElementById("msg4"),
    ];

    botMessages.forEach((msg, idx) => {
        setTimeout(() => {
            showMessageWithLoading(msg, loopMessages[idx]);
        }, (idx) * 1500);
    });

    // 봇 메시지 끝나고 나서 메시지창 & 카테고리 활성화
    setTimeout(() => {
        const chatContainer = document.getElementById("chat");
        showCategoryButtons(chatContainer);
        showInputContainer()
        // 스크롤을 맨 아래로 이동
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, (botMessages.length) * 1500);
}

// 봇 메세지
function showMessageWithLoading(container, message, delay = 1500) {
    botAccount(container);

    // 새로운 메시지 요소 생성
    const msgElement = document.createElement("div");
    msgElement.className = "message bot";
    msgElement.innerHTML = getLoadingDotsHTML();
    // msgElement.style.display = "block";
    msgElement.style.minHeight = "40px";    // height 설정이 안먹혀 minHeight로 수정


    // 메시지 컨테이너에 추가
    chat.appendChild(msgElement);
    
    // 메시지가 표시될 때 스크롤을 아래로 이동
    chat.scrollTop = chat.scrollHeight;

    // 로딩 애니메이션 후 메시지 표시
    setTimeout(() => {
        if(message == ''){
            msgElement.remove();
            return;
        }
        msgElement.innerHTML = message;
        msgElement.style.height = "auto";
        msgElement.style.minHeight = "";    // minHeight 설정 초기화
    }, delay);
}

// 봇의 질문 메시지 생성(응/아니)
function replaceLoadingWithQuestion(container, message) {
    botAccount(container);

    if (newsCategory.includes(message))
        select = "선택한 카테고리";
    else
        select = "입력한 키워드";

    categoryMessage = `${select}가 "${message}" 맞아?`;

    showMessageWithLoading(container, categoryMessage)

    setTimeout(() => {
        // 입력 영역 숨기기
        const inputContainer = document.querySelector(".input-container");
        if (inputContainer) {
            inputContainer.style.display = "none";
        }

        // 확인 버튼을 담을 래퍼 생성
        const confirmationWrapper = document.createElement("div");
        confirmationWrapper.className = "confirmation-wrapper";

        // 확인 버튼 추가 함수 호출
        appendConfirmationButtons(confirmationWrapper, container, message);

        // 입력 영역 위에 확인 버튼 추가
        if (inputContainer) {
            inputContainer.parentNode.insertBefore(confirmationWrapper, inputContainer);
        }

        // 스크롤을 맨 아래로 이동
        container.scrollTop = container.scrollHeight;
    }, 1500);
}

// 사용자 메시지
function appendUserMessage(container, messageText) {
    firstBotMessage = true;

    // 사용자 메시지를 담을 div 생성
    const userMessageWrapper = document.createElement("div");
    userMessageWrapper.classList.add("message-wrapper");
    userMessageWrapper.style.flexDirection = "column";
  
    // 실제 사용자 메시지 요소 생성
    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");
    userMessage.textContent = messageText;
  
    // 사용자 메시지를 래퍼에 추가하고, 채팅 컨테이너에 추가
    userMessageWrapper.appendChild(userMessage);
    container.appendChild(userMessageWrapper);
  
    // 스크롤을 맨 아래로 이동하여 최신 메시지가 보이도록 설정
    container.scrollTop = container.scrollHeight;
}

// 카테고리 버튼을 동적으로 추가하는 함수
// function showCategoryButtons(container) {
//     // 기존에 존재하는 카테고리 버튼 컨테이너가 있다면 삭제
//     const existingCategoryButtons = document.getElementById("categoryButtons");
//     if (existingCategoryButtons) {
//         existingCategoryButtons.remove();
//     }

//     // 카테고리 버튼 컨테이너 생성
//     const categoryButtonsWrapper = document.createElement("div");
//     categoryButtonsWrapper.className = "button-container";
//     categoryButtonsWrapper.id = "categoryButtons";
//     categoryButtonsWrapper.style.display = "block"; // 카테고리 버튼을 보이도록 설정
  
//     const buttonRow1 = document.createElement("div");
//     buttonRow1.className = "button-row";
  
//     const categories = newsCategory.slice(0,4);
//     categories.forEach(category => {
//         const button = document.createElement("button");
//         button.className = "styled-button";
//         button.textContent = category;
//         button.onclick = () => sendMessage(category);
//         buttonRow1.appendChild(button);
//     });
  
//     const buttonRow2 = document.createElement("div");
//     buttonRow2.className = "button-row";
  
//     const moreCategories = newsCategory.slice(4);
//     moreCategories.forEach(category => {
//         const button = document.createElement("button");
//         button.className = "styled-button";
//         button.textContent = category;
//         button.onclick = () => sendMessage(category);
//         buttonRow2.appendChild(button);
//     });
  
//     // 버튼들을 카테고리 버튼 컨테이너에 추가
//     categoryButtonsWrapper.appendChild(buttonRow1);
//     categoryButtonsWrapper.appendChild(buttonRow2);
  
//     // 채팅 컨테이너에 카테고리 버튼을 추가
//     container.appendChild(categoryButtonsWrapper);
// }

function showCategoryButtons(container) {
    // 기존에 존재하는 카테고리 버튼 컨테이너가 있다면 삭제
    const existingCategoryButtons = document.getElementById("categoryButtons");
    if (existingCategoryButtons) {
        existingCategoryButtons.remove();
    }

    // 카테고리 버튼 컨테이너 생성
    const categoryButtonsWrapper = document.createElement("div");
    categoryButtonsWrapper.className = "button-container";
    categoryButtonsWrapper.id = "categoryButtons";

    // 버튼 생성 및 추가
    newsCategory.forEach((category) => {
        const button = document.createElement("button");
        button.className = "styled-button";
        button.textContent = category;
        button.onclick = () => sendMessage(category);
        categoryButtonsWrapper.appendChild(button);
    });

    // 컨테이너에 버튼 컨테이너 추가
    container.appendChild(categoryButtonsWrapper);
}

// 카테고리 선택 및 키워드 입력시 로직
function sendMessage(message) {
    if (message === "") {
        return;
    }
    const chatInput = document.getElementById("chatInput");

    chatInput.disabled = true;  // 입력창 비활성화
    chatInput.value = ""; // 입력창 내용 지우기

    console.log("키워드: "+message);

    const chatContainer = document.getElementById("chat");
  
    // 1. 사용자 메시지 생성 및 추가
    appendUserMessage(chatContainer, message);
  
    // 카테고리 버튼 UI 숨기기
    const categoryButtons = document.getElementById("categoryButtons");
    if (categoryButtons) {
        categoryButtons.style.display = "none"; // 기존 카테고리 버튼을 숨김
    }
  
    // 2. 질문 말풍선 출력
    replaceLoadingWithQuestion(chatContainer, message);
}
  
// 확인 버튼 추가 함수
function appendConfirmationButtons(wrapper, container, message) {
    // "응!" 버튼 생성
    const yesButton = document.createElement("button"); // 전역 변수를 사용하지 않음
    yesButton.className = "ynbutton";

    const yesButtonText = document.createElement("div");
    yesButtonText.className = "button-text";
    yesButtonText.textContent = "응!";

    yesButton.appendChild(yesButtonText);
    wrapper.appendChild(yesButton);
  
    // "아니야" 버튼 생성
    const noButton = document.createElement("button"); // 전역 변수를 사용하지 않음
    noButton.className = "ynbutton";

    const noButtonText = document.createElement("div");
    noButtonText.className = "button-text";
    noButtonText.textContent = "아니야";

    noButton.appendChild(noButtonText);
    wrapper.appendChild(noButton);
  
    // "응!" 버튼 클릭 시 로직
    yesButton.addEventListener("click", function() {
        yesButtonEvent(wrapper, container, message);
    });

    // "아니야" 버튼 클릭 시 로직
    noButton.addEventListener("click", function() {
        noButtonEvent(wrapper, container);
    });
};

// 응 버튼 함수
async function yesButtonEvent (wrapper, container, message) {
    // 확인 버튼 제거
    wrapper.remove();
    // 사용자 응답 메시지 추가
    appendUserMessage(container, "응!");

    // 로딩 애니메이션 표시
    botAccount(container)
    const loadingWrapper = document.createElement("div");
    loadingWrapper.classList.add("message-wrapper");
    loadingWrapper.style.flexDirection = "column";

    const msgElement = document.createElement("div");
    msgElement.className = "message bot";
    msgElement.innerHTML = getLoadingDotsHTML();
    msgElement.style.display = "block";
    msgElement.style.height = "40px";

    // 메시지 컨테이너에 추가
    loadingWrapper.appendChild(msgElement);
    container.appendChild(loadingWrapper);
    container.scrollTop = container.scrollHeight;

    try {
        const response = await fetch('/crawl_news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message }) // 선택된 키워드를 메시지로 전송
        });

        const data = await response.json();

        // 로딩 애니메이션을 제거하고 크롤링 완료 메시지를 표시
        loadingWrapper.remove(); // 로딩 애니메이션 제거

        if (data.status === 'success' && data.news_items!="") {
            // 크롤링 완료 메시지 추가
            showMessageWithLoading(container, "뉴스 검색이 완료됐어!", 0);
            container.scrollTop = container.scrollHeight;

            // 크롤링된 뉴스 데이터도 사용할 수 있음
            console.log(data.news_items);

            // 카드뉴스 표시
            showCardNews(container, message);
        } else {
            // 에러 메시지 처리
            showMessageWithLoading(container, "크롤링 중 오류가 발생했습니다. 다시 시도해 주세요.");
        }
    } catch (error) {
        console.error('Fetch error:', error);
        loadingWrapper.remove();
        showMessageWithLoading(container, "서버와의 연결에 문제가 발생했습니다. 나중에 다시 시도해 주세요.");
    }
}

// 아니 버튼 함수
async function noButtonEvent(wrapper, container) {
    // 확인 버튼 제거
    wrapper.remove();

    // 사용자 응답 메시지 추가
    appendUserMessage(container, "아니야");

    // 봇 메세지 표시
    showMessageWithLoading(container, "잘못 입력했구나..?");
    await delay();
    showMessageWithLoading(container, "그럼 다시 한번 검색해 봐!");
    
    // 카테고리 버튼을 다시 표시
    await delay();
    showCategoryButtons(container);
    
    // 입력 영역 활성화
    const inputContainer = document.querySelector(".input-container");
    inputContainer.style.display = "flex"; // 입력 영역 다시 표시
    // inputContainer.style.flexDirection = "row"; // 레이아웃 복원
    showInputContainer(); // 입력창 활성화
    
    // 스크롤을 맨 아래로 이동
    container.scrollTop = container.scrollHeight
}

// 뉴스 카드 보여주기
async function showCardNews(container, message) {
    if (newsCategory.includes(message))
        select = "카테고리";
    else
        select = "키워드";
    // 봇 메세지 표시
    showMessageWithLoading(container, `"${message}" ${select}에 맞는 뉴스 카드를 보여줄 테니`);
    await delay();
    showMessageWithLoading(container, "5개의 카드 중 1개의 카드를 선택해 봐!");
    await delay();
    
    // 메시지가 다 출력된 후 슬라이더를 로드하는 코드 실행
    loadSlider();

    container.scrollTop = container.scrollHeight;
}

// 카드 선택 이벤트 리스너
window.addEventListener("message", (event) => {
    if (event.data.type === "cardSelected") {
        const { cardHTML, style, uniqueLink } = event.data;
        const chatContainer = document.getElementById("chat");
        selectCardNews(chatContainer, cardHTML, style, uniqueLink);
    }
});

// 뉴스 카드 선택
async function selectCardNews(container, cardHTML, style, uniqueLink) {
    addSelectedCardToChat(container, cardHTML, style);

    const { title, summary, insight } = await fetchCardData(uniqueLink);

    showMessageWithLoading(container, "이 뉴스 카드를 골랐구나!!!..?");
    await delay();
    showMessageWithLoading(container, "[ 특보❗ : " + title + " ]");    // 뉴스 제목 출력
    await delay();
    showMessageWithLoading(container, summary);
    await delay();
    showMessageWithLoading(container, insight);
    
    firstBotMessage = true; // 다음 루프에 봇 프로필 띄우며 시작

    // 다음 루프 실행
    await delay();
    container.scrollTop = container.scrollHeight;
    retry(container);
}

// 카드 선택 후 서버에서 데이터 가져오기
async function fetchCardData(uniqueLink) {
    try {
        const titleResponse = await fetch(`/get_newstitle?unique_link=${uniqueLink}`);
        const titleData = await titleResponse.json();
        const title = titleData.status === 'success' ? titleData.summary : "타이틀 정보를 가져오는 데 실패했습니다. 다시 시도해 주세요.";

        const summaryResponse = await fetch(`/get_summary?unique_link=${uniqueLink}`);
        const summaryData = await summaryResponse.json();
        const summary = summaryData.status === 'success' ? summaryData.summary : "요약 정보를 가져오는 데 실패했습니다. 다시 시도해 주세요.";

        const insightResponse = await fetch(`/get_insight?unique_link=${uniqueLink}`);
        const insightData = await insightResponse.json();
        const insight = insightData.status === 'success' ? insightData.insight : "통찰력을 가져오는 데 실패했습니다. 다시 시도해 주세요.";

        return { title, summary, insight };
    } catch (error) {
        console.error("Fetch error:", error);
        return { summary: "서버와 연결할 수 없습니다. 나중에 다시 시도해 주세요.", insight: "서버와 연결할 수 없습니다. 나중에 다시 시도해 주세요." };
    }
}

// 선택된 카드를 채팅 화면에 추가하는 함수
function addSelectedCardToChat(container, cardHTML, style) {
    firstBotMessage = true; // 다음 봇 메세지에 사용자 프로필 추가

    const filteredStyle = style.replace(/body\s*{[^}]*}/g, "");
    const userMessageWrapper = document.createElement("div");
    userMessageWrapper.classList.add("message-wrapper");
    userMessageWrapper.style.flexDirection = "column";
    userMessageWrapper.style.marginTop = "20px";
    userMessageWrapper.style.alignItems = "flex-end";

    const userMessage = document.createElement("div");
    userMessage.classList.add("user");
    userMessage.innerHTML = cardHTML;

    const styleElement = document.createElement("style");
    styleElement.innerHTML = filteredStyle;
    document.head.appendChild(styleElement);

    userMessageWrapper.appendChild(userMessage);
    container.appendChild(userMessageWrapper);
    container.scrollTop = container.scrollHeight;

    document.getElementById("cardSlider").style.display = "none";
}

// 루프
async function retry(container){
    showMessageWithLoading(container, "다시 해볼까?");
    await delay(1500);

    appendRetryButton(container)
}

// "다시 할래!" 버튼 추가 함수
function appendRetryButton(container) {
    // 입력 영역 숨기기
    const inputContainer = document.querySelector(".input-container");
    if (inputContainer) {
        inputContainer.style.display = "none";
    }

    // "다시 할래!" 버튼을 담을 래퍼 생성
    const retryWrapper = document.createElement("div");
    retryWrapper.className = "confirmation-wrapper";

    // "다시 할래!" 버튼 생성
    const retryButton = document.createElement("button");
    retryButton.className = "ynbutton";

    const retryButtonText = document.createElement("div");
    retryButtonText.className = "button-text";
    retryButtonText.textContent = "다시 할래!";

    retryButton.appendChild(retryButtonText);
    retryWrapper.appendChild(retryButton); // 수정: wrapper 대신 retryWrapper에 추가

    // 버튼을 페이지에 삽입
    if (inputContainer) {
        inputContainer.parentNode.insertBefore(retryWrapper, inputContainer);
    }

    container.scrollTop = container.scrollHeight;

    // "다시 할래!" 버튼 클릭 시 로직
    retryButton.addEventListener("click", function() {
        retryWrapper.remove();  // 버튼 제거
        inputContainer.style.display = "flex";  // 입력 영역 다시 표시
        firstBotMessage = true; // 프로필 표시

        showInputContainer();   // 입력창 생성
        document.getElementById("chatInput").disabled = true;  // 입력창 비활성화

        container.scrollTop = container.scrollHeight;
        showLoopBotMessages();  // showLoopBotMessages 함수 실행
    });
}
