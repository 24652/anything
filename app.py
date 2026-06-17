import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Vertical Rhythm Game", layout="centered")

# 깔끔한 제목
st.title("🎵 세로형 모바일 리듬 게임")

# 리듬 게임 HTML/JS
rhythm_game_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Vertical Rhythm Game</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #0e1117;
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        #gameContainer { position: relative; }
        #gameCanvas {
            border: 4px solid #a932ff;
            background-color: #0b0813;
            box-shadow: 0 0 25px rgba(169, 50, 255, 0.4);
            border-radius: 12px;
        }
        #gameUi {
            display: flex;
            justify-content: space-between;
            width: 400px;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 700;
        }
        .stat-val { color: #00ffcc; }
        #msg {
            position: absolute;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-size: 18px;
            color: #fff;
            text-shadow: 1px 1px 4px #000;
            pointer-events: none;
            line-height: 1.6;
            width: 80%;
        }
        #adminUi {
            display: none;
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(255, 0, 127, 0.85);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            box-shadow: 0 0 10px rgba(255, 0, 127, 0.5);
            z-index: 10;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="adminUi">[ADMIN MODE] 대괄호 키로 조작 가능 ( [ : 이전 / ] : 다음 )</div>
        <div id="gameUi">
            <div>STAGE: <span id="stage" class="stat-val">1</span></div>
            <div>COMBO: <span id="combo" class="stat-val">0</span></div>
            <div>LIVES: <span id="lives" class="stat-val">10</span></div>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <div id="msg">키보드 D, F, J, K 또는 화면을 터치하세요!<br>스페이스바나 클릭 시 음악이 시작됩니다.</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const comboSpan = document.getElementById("combo");
        const livesSpan = document.getElementById("lives");
        const stageSpan = document.getElementById("stage");
        const msgDiv = document.getElementById("msg");
        const adminUi = document.getElementById("adminUi");

        // 게임 설정 변수
        let stage = 1;
        let combo = 0;
        let maxCombo = 0;
        let lives = 10;
        let score = 0;
        let gameActive = false;
        let noteSpeed = 5;
        let notes = [];
        let totalNotesCreated = 0;
        let totalNotesLimit = 40; // 한 스테이지당 내려올 총 노트 개수

        // 판정선 및 라인 세팅
        const lineCount = 4;
        const lineWidth = canvas.width / lineCount;
        const judgmentY = canvas.height - 80; // 판정선 높이
        const noteHeight = 20;

        // 조작 키 맵핑
        const keys = { 'd': 0, 'f': 1, 'j': 2, 'k': 3 };
        let keyStatus = [false, false, false, false];
        let judgmentTexts = []; // 판정 텍스트 이펙트 배열

        // 관리자 모드 관련
        let cheatBuffer = "";
        let isAdmin = false;

        function initStage() {
            notes = [];
            totalNotesCreated = 0;
            totalNotesLimit = 30 + stage * 10;
            noteSpeed = 5 + stage * 0.8;
            lives = 10;
            combo = 0;
            comboSpan.innerText = combo;
            livesSpan.innerText = lives;
            stageSpan.innerText = stage;
        }

        // 무작위 노트 생성 패턴
        function spawnNote() {
            if (totalNotesCreated >= totalNotesLimit) return;
            
            let lane = Math.floor(Math.random() * lineCount);
            let isGold = Math.random() < 0.15; // 15% 확률로 황금 보너스 노트
            notes.push({
                lane: lane,
                y: -noteHeight,
                type: isGold ? 'gold' : 'normal'
            });
            totalNotesCreated++;
        }

        function checkHit(lane) {
            let hitFound = false;
            for (let i = 0; i < notes.length; i++) {
                let n = notes[i];
                if (n.lane === lane) {
                    // 판정선 타겟 거리에 수렴하는지 체크 (오차범위 계산)
                    let distance = Math.abs(n.y - judgmentY);
                    if (distance < 45) {
                        hitFound = true;
                        let rating = "PERFECT";
                        if (distance <= 15) { rating = "PERFECT"; combo++; }
                        else if (distance <= 30) { rating = "GOOD"; combo++; }
                        else { rating = "BAD"; combo = 0; lives = Math.max(0, lives - 1); }
                        
                        if (n.type === 'gold' && rating !== "BAD") combo += 2; // 골드노트는 추가 콤보
                        
                        judgmentTexts.push({ text: rating, alpha: 1, y: judgmentY - 40, color: rating === "PERFECT" ? "#ff00cc" : "#00ffcc" });
                        notes.splice(i, 1);
                        break;
                    }
                }
            }
            if (!hitFound) {
                // 허공을 쳤을 때 미세 효과 피드백
            }
            comboSpan.innerText = combo;
            livesSpan.innerText = lives;
        }

        function changeStage(direction) {
            if (direction === 'next') stage++;
            else if (direction === 'prev' && stage > 1) stage--;
            
            gameActive = false;
            initStage();
            msgDiv.innerHTML = `⚙️ 스테이지 임의 이동: STAGE ${stage}<br>다시 시작하려면 스페이스바를 누르세요!`;
            msgDiv.style.display = "block";
        }

        initStage();

        // 키보드 핸들러
        document.addEventListener("keydown", (e) => {
            let keyLower = e.key.toLowerCase();
            
            // 치트 입력 검사
            cheatBuffer += keyLower;
            if (cheatBuffer.endsWith("joonmin")) {
                isAdmin = !isAdmin;
                adminUi.style.display = isAdmin ? "block" : "none";
                cheatBuffer = "";
            }
            if (cheatBuffer.length > 20) cheatBuffer = cheatBuffer.substring(10);

            if (isAdmin) {
                if (e.key === "]") { changeStage('next'); return; }
                if (e.key === "[") { changeStage('prev'); return; }
            }

            // 시작 토글
            if ((e.key === " " || keyLower in keys) && !gameActive && lives > 0) {
                gameActive = true;
                msgDiv.style.display = "none";
            }

            if (keyLower in keys) {
                let lane = keys[keyLower];
                keyStatus[lane] = true;
                if (gameActive) checkHit(lane);
            }
        });

        document.addEventListener("keyup", (e) => {
            let keyLower = e.key.toLowerCase();
            if (keyLower in keys) {
                keyStatus[keys[keyLower]] = false;
            }
        });

        // 모바일/마우스용 터치 판정 처리
        canvas.addEventListener("mousedown", (e) => {
            if (!gameActive && lives > 0) {
                gameActive = true;
                msgDiv.style.display = "none";
                return;
            }
            let clientX = e.clientX - canvas.getBoundingClientRect().left;
            let lane = Math.floor(clientX / lineWidth);
            if (lane >= 0 && lane < lineCount && gameActive) {
                keyStatus[lane] = true;
                checkHit(lane);
                setTimeout(() => { keyStatus[lane] = false; }, 80);
            }
        });

        let frameCounter = 0;

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. 레인 가이드 라인 그리기
            for (let i = 0; i < lineCount; i++) {
                ctx.strokeStyle = "rgba(169, 50, 255, 0.15)";
                ctx.beginPath();
                ctx.moveTo(i * lineWidth, 0);
                ctx.lineTo(i * lineWidth, canvas.height);
                ctx.stroke();

                // 키 누르고 있을 때 레인 배경 하이라이트 효과
                if (keyStatus[i]) {
                    ctx.fillStyle = "rgba(169, 50, 255, 0.2)";
                    ctx.fillRect(i * lineWidth, 0, lineWidth, canvas.height);
                }
            }

            // 2. 판정선 가이드바 시각화
            ctx.strokeStyle = "#4a90e2";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(0, judgmentY);
            ctx.lineTo(canvas.width, judgmentY);
            ctx.stroke();
            ctx.lineWidth = 1;

            // 판정 자리에 있는 버튼 텍스트 표시
            const btnLabels = ['D', 'F', 'J', 'K'];
            ctx.font = "bold 16px sans-serif";
            for (let i = 0; i < lineCount; i++) {
                ctx.fillStyle = keyStatus[i] ? "#00ffcc" : "#666";
                ctx.fillText(btnLabels[i], i * lineWidth + lineWidth / 2 - 6, judgmentY + 30);
            }

            if (gameActive) {
                frameCounter++;
                // 특정 프레임 간격마다 무작위 노트 떨구기
                let spawnInterval = Math.max(25 - stage * 2, 12);
                if (frameCounter % Math.floor(spawnInterval) === 0) {
                    spawnNote();
                }

                // 3. 노트 이동 및 충돌 체크
                for (let i = 0; i < notes.length; i++) {
                    let n = notes[i];
                    n.y += noteSpeed;

                    // 노트 드로잉
                    ctx.beginPath();
                    ctx.rect(n.lane * lineWidth + 4, n.y, lineWidth - 8, noteHeight);
                    ctx.fillStyle = n.type === 'gold' ? "#ffd700" : "#0095DD";
                    ctx.fill();
                    ctx.closePath();

                    // 판정선을 완전히 지나쳐 화면 아래로 새버렸을 때 (MISS 처리)
                    if (n.y > canvas.height) {
                        combo = 0;
                        lives = Math.max(0, lives - 1);
                        comboSpan.innerText = combo;
                        livesSpan.innerText = lives;
                        
                        judgmentTexts.push({ text: "MISS", alpha: 1, y: judgmentY - 40, color: "#ff3333" });
                        notes.splice(i, 1);
                        i--;
                    }
                }

                // 라이프 아웃 패배 조건 판단
                if (lives <= 0) {
                    gameActive = false;
                    msgDiv.innerHTML = "💥 GAME OVER 💥<br>새로고침(F5)으로 부활하세요.";
                    msgDiv.style.display = "block";
                }

                // 곡 끝까지 다 떨어뜨렸고 남은 노트가 없으면 클리어!
                if (totalNotesCreated >= totalNotesLimit && notes.length === 0) {
                    stage++;
                    gameActive = false;
                    initStage();
                    msgDiv.innerHTML = `🎉 STAGE CLEAR! 🎉<br>다음 난이도 STAGE ${stage} (클릭하여 시작)`;
                    msgDiv.style.display = "block";
                }
            }

            // 4. 판정 텍스트 피드백 애니메이션 효과
            ctx.font = "bold 24px sans-serif";
            for (let i = 0; i < judgmentTexts.length; i++) {
                let jt = judgmentTexts[i];
                ctx.save();
                ctx.globalAlpha = jt.alpha;
                ctx.fillStyle = jt.color;
                ctx.fillText(jt.text, canvas.width / 2 - ctx.measureText(jt.text).width / 2, jt.y);
                ctx.restore();
                
                jt.y -= 0.5;
                jt.alpha -= 0.03;
                if (jt.alpha <= 0) {
                    judgmentTexts.splice(i, 1);
                    i--;
                }
            }

            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

components.html(rhythm_game_html, height=670, scrolling=False)
