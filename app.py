import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Real Baseball Game", layout="centered")
st.title("⚾ KBO 프로야구 9이닝 매치 (타자 시점)")

baseball_pro_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Real Baseball Game</title>
    <style>
        body {
            margin: 0; padding: 0;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background-color: #0e1117; color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            height: 100vh; overflow: hidden;
        }
        #gameContainer { position: relative; }
        #gameCanvas {
            border: 4px solid #34495e; background-color: #27ae60;
            box-shadow: 0 0 30px rgba(0,0,0,0.5); border-radius: 12px;
        }
        #teamSelectScreen {
            position: absolute; top: 0; left: 0; width: 420px; height: 600px;
            background: rgba(14, 17, 23, 0.95); display: flex; flex-direction: column;
            justify-content: center; align-items: center; border-radius: 12px; z-index: 20;
        }
        .team-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 80%; margin-top: 20px;
        }
        .team-btn {
            background: #1f2937; color: white; border: 2px solid #4b5563; padding: 12px;
            border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s;
        }
        .team-btn:hover { background: #3b82f6; border-color: #60a5fa; }
        #gameUi {
            display: flex; justify-content: space-between; width: 420px;
            margin-bottom: 8px; font-size: 14px; font-weight: 700; background: #1e293b; padding: 8px; border-radius: 6px;
        }
        .stat-val { color: #f59e0b; }
        #msg {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 18px; color: #fff; text-shadow: 2px 2px 4px #000;
            pointer-events: none; line-height: 1.6; width: 85%; z-index: 5;
        }
        #adminUi {
            display: none; position: absolute; top: 45px; left: 50%; transform: translateX(-50%);
            background-color: rgba(255, 0, 127, 0.9); padding: 4px 12px; border-radius: 20px;
            font-size: 12px; font-weight: bold; color: #fff; z-index: 10;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="teamSelectScreen">
            <h2 style="margin-bottom:5px;">팀을 선택하세요</h2>
            <p style="color:#9ca3af; font-size:13px; margin:0 0 15px 0;">플레이어 팀을 고르면 AI와 경기를 치릅니다.</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>
        
        <div id="adminUi">[ADMIN] [ 키: 이닝 뒤로 / ] 키: 이닝 앞으로</div>
        
        <div id="gameUi">
            <div><span id="uiInning">1회초</span> | <span id="uiCurrentBatter" style="color:#60a5fa;">타자</span></div>
            <div>SCORE <span id="uiScore" class="stat-val">0 : 0</span></div>
            <div>B:<span id="uiB" style="color:#fbbf24;">0</span> S:<span id="uiS" style="color:#f87171;">0</span> O:<span id="uiO" style="color:#ef4444;">0</span></div>
        </div>
        <canvas id="gameCanvas" width="420" height="600"></canvas>
        <div id="msg">팀 선택 후 경기가 시작됩니다!</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msg");
        const adminUi = document.getElementById("adminUi");
        
        // KBO 데이터 정의
        const kboTeams = {
            "삼성 라이온즈": ["원태인(P)", "구자욱", "강민호", "김지찬", "이성규", "김영웅", "이재현", "류지혁", "김성윤"],
            "LG 트윈스": ["임찬규(P)", "홍창기", "신민재", "오스틴", "문보경", "박동원", "오지환", "박해민", "구본혁"],
            "KIA 타이거즈": ["양현종(P)", "박찬호", "최원준", "김도영", "최형우", "나성범", "소크라테스", "김선빈", "김태군"],
            "두산 베어스": ["곽빈(P)", "정수빈", "허경민", "양의지", "김재환", "양석환", "강승호", "라모스", "전민재"],
            "KT 위즈": ["고영표(P)", "로하스", "강백호", "장성우", "황재균", "오재일", "배정대", "신본기", "심우준"],
            "SSG 랜더스": ["김광현(P)", "최정", "에레디아", "한유섬", "박성한", "고명준", "이지영", "최지훈", "추신수"],
            "롯데 자이언츠": ["반즈(P)", "황성빈", "윤동희", "레이예스", "전준우", "나승엽", "고승민", "유강남", "박승욱"],
            "한화 이글스": ["류현진(P)", "페라자", "노시환", "안치홍", "채은성", "문현빈", "최재훈", "이도윤", "장진혁"],
            "NC 다이노스": ["신민혁(P)", "박민우", "권희동", "데이비슨", "박건우", "서호철", "김형준", "김성욱", "김주원"],
            "키움 히어로즈": ["후라도(P)", "이주형", "도슨", "송성문", "최주환", "김혜성", "고영우", "김재현", "이형종"]
        };

        let playerTeam = "";
        let cpuTeam = "";
        let playerLineup = [];
        let cpuLineup = [];
        
        let currentInning = 1; 
        let isTop = true; // true: 초(플레이어 공격), false: 말(CPU 공격)
        let scores = { player: 0, cpu: 0 };
        let count = { B: 0, S: 0, O: 0 };
        let bases = [false, false, false]; // 1루, 2루, 3루 주자 상태

        let currentBatterIdx = 1; // 0번은 투수라 1번타자부터 시작
        let cpuBatterIdx = 1;

        // 야구 경기 메커니즘 엔진 변수
        let gameActive = false;
        let ball = { x: 210, y: 220, vx: 0, vy: 0, radius: 4, active: false, speed: 5, t: 0 };
        let isSwinging = false;
        let swingFrame = 0;
        let feedback = { text: "", alpha: 0, color: "#fff" };

        // 치트 시스템
        let cheatBuffer = "";
        let isAdmin = false;

        // 팀 선택 화면 빌드
        const teamGrid = document.getElementById("teamGrid");
        Object.keys(kboTeams).forEach(name => {
            let btn = document.createElement("button");
            btn.className = "team-btn";
            btn.innerText = name;
            btn.onclick = () => selectTeam(name);
            teamGrid.appendChild(btn);
        });

        function selectTeam(name) {
            playerTeam = name;
            playerLineup = kboTeams[playerTeam];
            
            // CPU팀 자동 배정 (선택한 팀 제외 무작위)
            let remaining = Object.keys(kboTeams).filter(t => t !== name);
            cpuTeam = remaining[Math.floor(Math.random() * remaining.length)];
            cpuLineup = kboTeams[cpuTeam];

            document.getElementById("teamSelectScreen").style.display = "none";
            resetGameMatch();
        }

        function resetGameMatch() {
            scores = { player: 0, cpu: 0 };
            currentInning = 1;
            isTop = true;
            resetInningHalf();
            gameActive = true;
            updateUi();
            msgDiv.innerHTML = `경기 개시! <b>${playerTeam}</b> VS <b>${cpuTeam}</b><br>스페이스바나 화면 터치로 타격을 준비하세요.`;
        }

        function resetInningHalf() {
            count.B = 0; count.S = 0; count.O = 0;
            bases = [false, false, false];
            ball.active = false;
            isSwinging = false;
        }

        function updateUi() {
            document.getElementById("uiInning").innerText = `${currentInning}회${isTop ? '초' : '말'}`;
            document.getElementById("uiScore").innerText = `${scores.player} : ${scores.cpu}`;
            document.getElementById("uiB").innerText = count.B;
            document.getElementById("uiS").innerText = count.S;
            document.getElementById("uiO").innerText = count.O;
            
            let currentBatterName = isTop ? playerLineup[currentBatterIdx] : cpuLineup[cpuBatterIdx];
            document.getElementById("uiCurrentBatter").innerText = `타자: ${currentBatterName}`;
        }

        function pitchBall() {
            if (ball.active) return;
            ball.x = 210; ball.y = 220; ball.radius = 4; ball.t = 0;
            ball.active = true;
            
            // 랜덤 구종 궤적 공식화
            let speedMod = 4 + (currentInning * 0.3);
            ball.vy = speedMod + Math.random() * 3;
            ball.vx = (Math.random() - 0.5) * 1.5;
            msgDiv.style.display = "none";
        }

        function handleHit(dist) {
            ball.active = false;
            if (dist < 12) {
                showFeedback("🔥 대형 홈런! 🔥", "#f59e0b");
                advanceRunners(4);
            } else if (dist < 28) {
                showFeedback("⚾ 안타! ⚾", "#3498db");
                advanceRunners(1);
            } else {
                showFeedback("⚠️ 파울 플라이 아웃 ⚠️", "#e74c3c");
                addOut();
            }
            nextBatter();
        }

        function advanceRunners(numBases) {
            let runs = 0;
            for (let b = 0; b < numBases; b++) {
                if (bases[2]) runs++;
                bases[2] = bases[1];
                bases[1] = bases[0];
                bases[0] = (b === 0);
            }
            if (isTop) scores.player += runs;
            else scores.cpu += runs;
            
            count.B = 0; count.S = 0;
            updateUi();
        }

        function addStrike() {
            count.S++;
            if (count.S >= 3) {
                showFeedback("❌ 삼진 아웃! ❌", "#ef4444");
                addOut();
                nextBatter();
            } else {
                showFeedback("STRIKE!", "#f87171");
            }
            updateUi();
        }

        function addOut() {
            count.O++;
            if (count.O >= 3) {
                switchInningHalf();
            }
            updateUi();
        }

        function nextBatter() {
            count.B = 0; count.S = 0;
            if (isTop) {
                currentBatterIdx = (currentBatterIdx % 8) + 1;
            } else {
                cpuBatterIdx = (cpuBatterIdx % 8) + 1;
            }
            setTimeout(() => {
                if(gameActive) {
                    msgDiv.innerHTML = "다음 타자 타석 진입...<br>(클릭/스페이스바로 투구)";
                    msgDiv.style.display = "block";
                }
            }, 1200);
        }

        function switchInningHalf() {
            if (isTop) {
                isTop = false;
                resetInningHalf();
                msgDiv.innerHTML = `공수 교대 (${cpuTeam} 공격)<br>클릭 시 투구를 시작합니다.`;
            } else {
                isTop = true;
                currentInning++;
                if (currentInning > 9) {
                    gameActive = false;
                    let winner = scores.player > scores.cpu ? playerTeam : (scores.player < scores.cpu ? cpuTeam : "무승부");
                    msgDiv.innerHTML = `종료! 경기 결과 [${winner}] 승리!<br>F5를 눌러 재경기`;
                } else {
                    resetInningHalf();
                    msgDiv.innerHTML = `${currentInning}회초 진행 (${playerTeam} 공격)<br>클릭하여 시작`;
                }
            }
            msgDiv.style.display = "block";
        }

        function showFeedback(txt, col) {
            feedback.text = txt; feedback.color = col; feedback.alpha = 1;
        }

        function swingBat() {
            if (isSwinging || !ball.active) return;
            isSwinging = true; swingFrame = 0;
            
            let timingY = 490;
            let dist = Math.abs(ball.y - timingY);
            if (dist < 40) {
                handleHit(dist);
            } else {
                showFeedback("헛스윙!", "#ef4444");
                addStrike();
            }
        }

        // 치트 강제 이닝 변환기
        function cheatInning(dir) {
            if (dir === 'next') currentInning++;
            else if (dir === 'prev' && currentInning > 1) currentInning--;
            resetInningHalf();
            updateUi();
            msgDiv.innerHTML = `⚙️ 관리자 모드: ${currentInning}회 이동 완료`;
        }

        // 컨트롤 리스너
        document.addEventListener("keydown", (e) => {
            let keyLower = e.key.toLowerCase();
            cheatBuffer += keyLower;
            if (cheatBuffer.endsWith("joonmin")) {
                isAdmin = !isAdmin;
                adminUi.style.display = isAdmin ? "block" : "none";
                cheatBuffer = "";
            }
            if (cheatBuffer.length > 20) cheatBuffer = cheatBuffer.substring(10);

            if (isAdmin) {
                if (e.key === "]") { cheatInning('next'); return; }
                if (e.key === "[") { cheatInning('prev'); return; }
            }

            if (e.key === " ") {
                e.preventDefault();
                if (!ball.active) pitchBall();
                else swingBat();
            }
        });

        canvas.addEventListener("mousedown", (e) => {
            if (!ball.active) pitchBall();
            else swingBat();
        });

        function drawField() {
            // 원근감 3D 야구 필드 라인 구현
            ctx.fillStyle = "#1e3a1e"; ctx.fillRect(0,0,420,600);
            
            // 내야 다이아몬드 (흙) 부채꼴 형태 라인 구성
            ctx.fillStyle = "#cc9966";
            ctx.beginPath();
            ctx.moveTo(210, 520); // 홈
            ctx.lineTo(360, 370); // 1루 방향 선상
            ctx.lineTo(210, 220); // 2루 백스크린 하단
            ctx.lineTo(60, 370);  // 3루 방향 선상
            ctx.closePath(); ctx.fill();

            // 내야 잔디 중앙 패치 심기
            ctx.fillStyle = "#27ae60";
            ctx.beginPath();
            ctx.moveTo(210, 460); ctx.lineTo(300, 370); ctx.lineTo(210, 280); ctx.lineTo(120, 370);
            ctx.closePath(); ctx.fill();

            // 베이스라인 마킹 고정 시각화
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(205, 515, 10, 10); // 홈베이스
            if(bases[0]) ctx.fillStyle = "#ff4757"; else ctx.fillStyle = "#fff";
            ctx.fillRect(350, 365, 12, 12); // 1루 오렌지 주자 점등
            if(bases[1]) ctx.fillStyle = "#ff4757"; else ctx.fillStyle = "#fff";
            ctx.fillRect(204, 215, 12, 12); // 2루
            if(bases[2]) ctx.fillStyle = "#ff4757"; else ctx.fillStyle = "#fff";
            ctx.fillRect(58, 365, 12, 12);  // 3루

            // 모든 야구 포지션 수비 포지션 완벽 싹 다 배치 (이모지 그래픽 최적화)
            ctx.font = "14px Arial";
            ctx.fillText("👤 P", 195, 260); // 투수
            ctx.fillText("👤 1B", 310, 340); // 1루수
            ctx.fillText("👤 2B", 250, 240); // 2루수
            ctx.fillText("👤 3B", 90, 340);  // 3루수
            ctx.fillText("👤 SS", 140, 240); // 유격수
            ctx.fillText("👤 LF", 70, 120);  // 좌익수
            ctx.fillText("👤 CF", 195, 90);  // 중견수
            ctx.fillText("👤 RF", 320, 120); // 우익수
            ctx.fillText("👤 C", 197, 555);  // 포수

            // 타격 타이밍 존 바 가이드라인
            ctx.fillStyle = "rgba(241, 196, 15, 0.25)";
            ctx.fillRect(0, 465, 420, 50);
            ctx.strokeStyle = "#f1c40f"; ctx.lineWidth = 2;
            ctx.strokeRect(0, 465, 420, 50);
        }

        function drawLoop() {
            ctx.clearRect(0,0,420,600);
            drawField();

            // 공 투구 궤적 랜더링
            if (ball.active) {
                ball.t += 0.05;
                ball.y += ball.vy;
                ball.x += ball.vx;
                ball.radius += 0.18; // 다가올수록 3D 원근 줌 이펙트

                ctx.beginPath();
                ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
                ctx.fillStyle = "#ffffff"; ctx.fill();
                ctx.strokeStyle = "#000"; ctx.stroke();
                ctx.closePath();

                if (ball.y > 540) {
                    addStrike();
                    ball.active = false;
                }
            }

            // 배트 애니메이션 프레임워크
            if (isSwinging) {
                swingFrame++;
                ctx.save();
                ctx.translate(210, 490);
                ctx.rotate((swingFrame * 20 - 45) * Math.PI / 180);
                ctx.fillStyle = "#b5835a";
                ctx.fillRect(0, -6, 55, 12);
                ctx.restore();
                if (swingFrame > 8) isSwinging = false;
            } else {
                ctx.save();
                ctx.translate(210, 490);
                ctx.rotate(-45 * Math.PI / 180);
                ctx.fillStyle = "#b5835a";
                ctx.fillRect(0, -6, 45, 10);
                ctx.restore();
            }

            // 피드백 텍스트 연출
            if (feedback.alpha > 0) {
                ctx.font = "bold 24px sans-serif";
                ctx.fillStyle = feedback.color;
                ctx.save(); ctx.globalAlpha = feedback.alpha;
                ctx.fillText(feedback.text, 210 - ctx.measureText(feedback.text).width/2, 180);
                ctx.restore();
                feedback.alpha -= 0.015;
            }

            requestAnimationFrame(drawLoop);
        }

        drawLoop();
    </script>
</body>
</html>
"""

components.html(baseball_pro_html, height=670, scrolling=False)
