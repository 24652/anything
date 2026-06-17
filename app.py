import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Real Baseball Play Match", layout="centered")
st.title("⚾ KBO 프로야구 풀 매치 (타격 & 투구 + 불펜)")

baseball_pro_v2_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Pro Baseball Full Engine</title>
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
            border: 4px solid #475569; background-color: #1e3a1e;
            box-shadow: 0 0 30px rgba(0,0,0,0.6); border-radius: 12px;
        }
        #teamSelectScreen {
            position: absolute; top: 0; left: 0; width: 440px; height: 600px;
            background: rgba(15, 23, 42, 0.98); display: flex; flex-direction: column;
            justify-content: center; align-items: center; border-radius: 12px; z-index: 20;
        }
        .team-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 85%; margin-top: 15px;
        }
        .team-btn {
            background: #1e293b; color: white; border: 2px solid #475569; padding: 10px;
            border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 13px;
        }
        .team-btn:hover { background: #2563eb; border-color: #60a5fa; }
        #gameUi {
            display: flex; justify-content: space-between; width: 440px;
            margin-bottom: 8px; font-size: 13px; font-weight: 700; background: #0f172a; padding: 10px; border-radius: 8px;
            box-sizing: border-box; border: 1px solid #334155;
        }
        .stat-val { color: #f59e0b; }
        #msg {
            position: absolute; top: 38%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 16px; color: #fff; text-shadow: 2px 2px 5px #000;
            pointer-events: none; line-height: 1.6; width: 85%; z-index: 5;
        }
        #controlPanel {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 8px; z-index: 10; width: 90%; justify-content: center;
        }
        .action-btn {
            background: #2563eb; color: white; border: none; padding: 8px 14px;
            border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .action-btn:hover { background: #1d4ed8; }
        .pitch-btn { background: #dc2626; }
        .pitch-btn:hover { background: #b91c1c; }
        .bullpen-btn { background: #4b5563; }
        .bullpen-btn:hover { background: #374151; }
        #adminUi {
            display: none; position: absolute; top: 55px; left: 50%; transform: translateX(-50%);
            background-color: rgba(219, 39, 119, 0.95); padding: 4px 12px; border-radius: 20px;
            font-size: 11px; font-weight: bold; color: #fff; z-index: 10;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="teamSelectScreen">
            <h2 style="margin-bottom:2px; color:#f8fafc;">⚾ 구단 선택</h2>
            <p style="color:#94a3b8; font-size:12px; margin:0 0 10px 0;">팀을 고르면 전체 수비 라인업과 불펜이 구성됩니다.</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>
        
        <div id="adminUi">[ADMIN] [ : 이전 이닝 / ] : 다음 이닝</div>
        
        <div id="gameUi">
            <div><span id="uiInning">1회초</span><br><span id="uiRole" style="color:#38bdf8;">공격 중</span></div>
            <div style="text-align: center;">SCORE<br><span id="uiScore" class="stat-val" style="font-size:16px;">0 : 0</span></div>
            <div style="text-align: center;"><span id="uiCurrentPitcher" style="font-size:11px; color:#94a3b8;">투수</span><br><span id="uiCurrentBatter" style="color:#60a5fa;">타자</span></div>
            <div style="text-align: right;">B:<span id="uiB" style="color:#fbbf24;">0</span> S:<span id="uiS" style="color:#f87171;">0</span> O:<span id="uiO" style="color:#ef4444;">0</span></div>
        </div>
        <canvas id="gameCanvas" width="440" height="600"></canvas>
        <div id="msg">팀 선택 후 매치가 시작됩니다!</div>
        
        <div id="controlPanel"></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msg");
        const adminUi = document.getElementById("adminUi");
        const controlPanel = document.getElementById("controlPanel");
        
        // 투수 불펜(선발, 중간, 마무리) 및 타자 전체 리스트업 완료
        const kboDatabase = {
            "삼성 라이온즈": {
                pitchers: ["원태인", "최하늘", "오승환"],
                batters: ["구자욱", "강민호", "맥키넌", "류지혁", "김영웅", "이재현", "김지찬", "이성규", "김성윤"]
            },
            "LG 트윈스": {
                pitchers: ["임찬규", "유영찬", "김진성"],
                batters: ["홍창기", "신민재", "오스틴", "문보경", "박동원", "오지환", "박해민", "구본혁", "이영빈"]
            },
            "KIA 타이거즈": {
                pitchers: ["양현종", "전상현", "정해영"],
                batters: ["박찬호", "최원준", "김도영", "최형우", "나성범", "소크라테스", "김선빈", "김태군", "변우혁"]
            },
            "두산 베어스": {
                pitchers: ["곽빈", "이병헌", "김택연"],
                batters: ["정수빈", "허경민", "양의지", "김재환", "양석환", "강승호", "라모스", "전민재", "조수행"]
            },
            "KT 위즈": {
                pitchers: ["고영표", "김민", "박영현"],
                batters: ["로하스", "강백호", "장성우", "황재균", "오재일", "배정대", "신본기", "심우준", "문상철"]
            },
            "SSG 랜더스": {
                pitchers: ["김광현", "노경은", "문승원"],
                batters: ["최정", "에레디아", "한유섬", "박성한", "고명준", "이지영", "최지훈", "추신수", "박지환"]
            },
            "롯데 자이언츠": {
                pitchers: ["반즈", "김상수", "김원중"],
                batters: ["황성빈", "윤동희", "레이예스", "전준우", "나승엽", "고승민", "유강남", "박승욱", "노진혁"]
            },
            "한화 이글스": {
                pitchers: ["류현진", "한승혁", "주현상"],
                batters: ["페라자", "노시환", "안치홍", "채은성", "문현빈", "최재훈", "이도윤", "장진혁", "황영묵"]
            },
            "NC 다이노스": {
                pitchers: ["신민혁", "김영규", "이용찬"],
                batters: ["박민우", "권희동", "데이비슨", "박건우", "서호철", "김형준", "김성욱", "김주원", "도태훈"]
            },
            "키움 히어로즈": {
                pitchers: ["후라도", "조상우", "주승우"],
                batters: ["이주형", "도슨", "송성문", "최주환", "김혜성", "고영우", "김재현", "이형종", "장재영"]
            }
        };

        let playerTeam = "", cpuTeam = "";
        let currentInning = 1, isTop = true; // 초: 플레이어 타격(CPU 투구) / 말: 플레이어 투구(CPU 타격)
        let scores = { player: 0, cpu: 0 };
        let count = { B: 0, S: 0, O: 0 };
        let bases = [false, false, false];

        // 투수 포지션 인덱스 (0: 선발, 1: 중간, 2: 마무리)
        let playerPitcherIdx = 0, cpuPitcherIdx = 0;
        let playerBatterIdx = 0, cpuBatterIdx = 0;

        let gameActive = false;
        let ball = { x: 220, y: 220, vx: 0, vy: 0, radius: 4, active: false, type: 'normal' };
        let isSwinging = false, swingFrame = 0;
        let feedback = { text: "", alpha: 0, color: "#fff" };
        let cheatBuffer = ""; let isAdmin = false;

        // 팀 선택 그리드 생성
        const teamGrid = document.getElementById("teamGrid");
        Object.keys(kboDatabase).forEach(name => {
            let btn = document.createElement("button");
            btn.className = "team-btn";
            btn.innerText = name;
            btn.onclick = () => { playerTeam = name; selectCpuTeam(); };
            teamGrid.appendChild(btn);
        });

        function selectCpuTeam() {
            let remaining = Object.keys(kboDatabase).filter(t => t !== playerTeam);
            cpuTeam = remaining[Math.floor(Math.random() * remaining.length)];
            document.getElementById("teamSelectScreen").style.display = "none";
            startMatch();
        }

        function startMatch() {
            scores = { player: 0, cpu: 0 };
            currentInning = 1; isTop = true;
            playerPitcherIdx = 0; cpuPitcherIdx = 0;
            playerBatterIdx = 0; cpuBatterIdx = 0;
            resetHalfInning();
            gameActive = true;
            updateInterface();
        }

        function resetHalfInning() {
            count.B = 0; count.S = 0; count.O = 0;
            bases = [false, false, false];
            ball.active = false; isSwinging = false;
            buildControlButtons();
        }

        function updateInterface() {
            document.getElementById("uiInning").innerText = `${currentInning}회${isTop ? '초' : '말'}`;
            document.getElementById("uiRole").innerText = isTop ? "공격 (타격)" : "수비 (투구)";
            document.getElementById("uiRole").style.color = isTop ? "#38bdf8" : "#f87171";
            document.getElementById("uiScore").innerText = `${scores.player} : ${scores.cpu}`;
            document.getElementById("uiB").innerText = count.B;
            document.getElementById("uiS").innerText = count.S;
            document.getElementById("uiO").innerText = count.O;

            let pName = isTop ? kboDatabase[cpuTeam].pitchers[cpuPitcherIdx] : kboDatabase[playerTeam].pitchers[playerPitcherIdx];
            let bName = isTop ? kboDatabase[playerTeam].batters[playerBatterIdx] : kboDatabase[cpuTeam].batters[cpuBatterIdx];
            
            document.getElementById("uiCurrentPitcher").innerText = `투수: ${pName}`;
            document.getElementById("uiCurrentBatter").innerText = `타자: ${bName}`;
        }

        function buildControlButtons() {
            controlPanel.innerHTML = "";
            if (!gameActive) return;

            if (isTop) {
                // 공격 모드: 타격 원버튼 스윙 구성
                let btn = document.createElement("button");
                btn.className = "action-btn";
                btn.innerText = "⚾ 배트 휘두르기 (스페이스바)";
                btn.onclick = () => { if(!ball.active) cpuPitching(); else swingBat(); };
                controlPanel.appendChild(btn);
            } else {
                // 수비 모드: 구종 직접 골라서 투구하기 버튼 + 불펜 교체 버튼 추가
                const pitches = [
                    { name: "포심 직구", type: "fast" },
                    { name: "슬라이더", type: "slider" },
                    { name: "체인지업", type: "changeup" }
                ];
                pitches.forEach(p => {
                    let btn = document.createElement("button");
                    btn.className = "action-btn pitch-btn";
                    btn.innerText = p.name;
                    btn.onclick = () => playerPitching(p.type);
                    controlPanel.appendChild(btn);
                });

                // 불펜 교체 버튼 버튼 추가
                let bpBtn = document.createElement("button");
                bpBtn.className = "action-btn bullpen-btn";
                bpBtn.innerText = "🔄 불펜 투수 교체";
                bpBtn.onclick = callBullpen;
                controlPanel.appendChild(bpBtn);
            }
        }

        // 불펜 교체 기능 제어 루틴
        function callBullpen() {
            if (ball.active) return;
            playerPitcherIdx = (playerPitcherIdx + 1) % 3;
            let currentName = kboDatabase[playerTeam].pitchers[playerPitcherIdx];
            showFeedback(`투수 교체! 마운드에 [${currentName}]`, "#fbbf24");
            updateInterface();
        }

        // 플레이어가 직접 던지는 로직
        function playerPitching(type) {
            if (ball.active) return;
            ball.x = 220; ball.y = 220; ball.radius = 4; ball.active = true; ball.type = type;
            msgDiv.style.display = "none";

            if (type === "fast") { ball.vy = 7.5; ball.vx = 0; }
            else if (type === "slider") { ball.vy = 5.5; ball.vx = -1.6; }
            else { ball.vy = 4.2; ball.vx = 0.4; } // 체인지업 타이밍 감속용

            // CPU 타자의 인공지능 배트 스윙 여부 및 타이밍 예약 계산
            let swingDelay = 400 + Math.random() * 250;
            if (type === "changeup") swingDelay += 120;
            
            setTimeout(() => {
                if (ball.active && !isTop) cpuSwingLogic();
            }, swingDelay);
        }

        // CPU가 자동으로 던져주는 로직
        function cpuPitching() {
            ball.x = 220; ball.y = 220; ball.radius = 4; ball.active = true;
            let rand = Math.random();
            if (rand < 0.33) { ball.type = "fast"; ball.vy = 6.5; ball.vx = 0; }
            else if (rand < 0.66) { ball.type = "slider"; ball.vy = 5.2; ball.vx = 1.4; }
            else { ball.type = "changeup"; ball.vy = 4.0; ball.vx = -0.3; }
            msgDiv.style.display = "none";
        }

        // CPU 타자 자동 타격 AI 판정
        function cpuSwingLogic() {
            isSwinging = true; swingFrame = 0;
            let dist = Math.abs(ball.y - 490);
            if (dist < 35) {
                ball.active = false;
                if (dist < 12) { showFeedback("🔥 CPU 홈런! 🔥", "#ef4444"); advanceBases(4); }
                else { showFeedback("⚾ CPU 안타! ⚾", "#f59e0b"); advanceBases(1); }
                nextBatterLineup();
            } else {
                showFeedback("헛스윙 스트라이크!", "#38bdf8");
                recordStrike();
            }
        }

        function swingBat() {
            if (isSwinging || !ball.active) return;
            isSwinging = true; swingFrame = 0;
            
            let dist = Math.abs(ball.y - 490);
            if (dist < 38) {
                ball.active = false;
                if (dist < 10) { showFeedback("🔥 홈런!!! 🔥", "#38bdf8"); advanceBases(4); }
                else { showFeedback("⚾ 안타 성공! ⚾", "#10b981"); advanceBases(1); }
                nextBatterLineup();
            } else {
                showFeedback("헛스윙!", "#ef4444");
                recordStrike();
            }
        }

        function recordStrike() {
            count.S++;
            if (count.S >= 3) {
                showFeedback("❌ 삼진 아웃! ❌", "#ef4444");
                recordOut();
                nextBatterLineup();
            }
            updateInterface();
        }

        function recordOut() {
            count.O++;
            if (count.O >= 3) {
                toggleInningChange();
            }
            updateInterface();
        }

        function advanceBases(num) {
            let directRuns = 0;
            for (let i = 0; i < num; i++) {
                if (bases[2]) directRuns++;
                bases[2] = bases[1]; bases[1] = bases[0]; bases[0] = (i === 0);
            }
            if (isTop) scores.player += directRuns;
            else scores.cpu += directRuns;
            count.B = 0; count.S = 0;
            updateInterface();
        }

        function nextBatterLineup() {
            count.B = 0; count.S = 0;
            if (isTop) playerBatterIdx = (playerBatterIdx + 1) % 9;
            else cpuBatterIdx = (cpuBatterIdx + 1) % 9;
            
            setTimeout(() => {
                if(gameActive) {
                    msgDiv.innerHTML = isTop ? "공을 기다리는 중... 스윙 준비하세요!" : "구종을 골라 플레이볼!";
                    msgDiv.style.display = "block";
                    ball.active = false;
                }
            }, 1000);
        }

        function toggleInningChange() {
            if (isTop) {
                isTop = false; resetHalfInning();
                msgDiv.innerHTML = `공수 교대! 수비 시점 🥎<br>구종 버튼을 눌러 직접 투구하세요.`;
            } else {
                isTop = true; currentInning++;
                if (currentInning > 9) {
                    gameActive = false; buildControlButtons();
                    let finalWinner = scores.player > scores.cpu ? playerTeam : (scores.player < scores.cpu ? cpuTeam : "무승부");
                    msgDiv.innerHTML = `🏁 경기 종료! 최종 승리구단: [${finalWinner}]<br>F5를 눌러 재경기 가능`;
                } else {
                    resetHalfInning();
                    msgDiv.innerHTML = `${currentInning}회초 전환! 공격 개시 (${playerTeam})`;
                }
            }
            msgDiv.style.display = "block";
            updateInterface();
        }

        function showFeedback(txt, col) {
            feedback.text = txt; feedback.color = col; feedback.alpha = 1;
        }

        // 관리자용 이닝 컨트롤러
        function adminShiftInning(dir) {
            if (dir === 'next') currentInning++;
            else if (dir === 'prev' && currentInning > 1) currentInning--;
            resetHalfInning(); updateInterface();
            msgDiv.innerHTML = `⚙️ 치트 권한 강제 이동: ${currentInning}회`;
        }

        document.addEventListener("keydown", (e) => {
            let kl = e.key.toLowerCase(); cheatBuffer += kl;
            if (cheatBuffer.endsWith("joonmin")) { isAdmin = !isAdmin; adminUi.style.display = isAdmin ? "block" : "none"; cheatBuffer = ""; }
            if (cheatBuffer.length > 20) cheatBuffer = cheatBuffer.substring(10);
            if (isAdmin) { if (e.key === "]") adminShiftInning('next'); if (e.key === "[") adminShiftInning('prev'); }
            
            if (e.key === " " && isTop) {
                e.preventDefault();
                if (!ball.active) cpuPitching(); else swingBat();
            }
        });

        function renderStadium() {
            // 필드 베이스라인 렌더링
            ctx.fillStyle = "#14532d"; ctx.fillRect(0,0,440,600);
            ctx.fillStyle = "#b45309"; // 흙 구역
            ctx.beginPath(); ctx.moveTo(220, 520); ctx.lineTo(380, 360); ctx.lineTo(220, 200); ctx.lineTo(60, 360); ctx.closePath(); ctx.fill();
            ctx.fillStyle = "#15803d"; // 잔디 패치
            ctx.beginPath(); ctx.moveTo(220, 450); ctx.lineTo(310, 360); ctx.lineTo(220, 270); ctx.lineTo(130, 360); ctx.closePath(); ctx.fill();

            // 베이스 주자 상황 연출
            ctx.fillStyle = "#ffffff"; ctx.fillRect(215, 515, 10, 10);
            ctx.fillStyle = bases[0] ? "#ef4444" : "#ffffff"; ctx.fillRect(370, 355, 12, 12);
            ctx.fillStyle = bases[1] ? "#ef4444" : "#ffffff"; ctx.fillRect(214, 194, 12, 12);
            ctx.fillStyle = bases[2] ? "#ef4444" : "#ffffff"; ctx.fillRect(58, 355, 12, 12);

            // 포지션별 완벽 수비수 배치
            ctx.font = "bold 12px sans-serif"; ctx.fillStyle = "#f8fafc";
            ctx.fillText("P", 215, 255); ctx.fillText("C", 215, 555);
            ctx.fillText("1B", 330, 330); ctx.fillText("2B", 265, 230);
            ctx.fillText("3B", 95, 330); ctx.fillText("SS", 155, 230);
            ctx.fillText("LF", 80, 120); ctx.fillText("CF", 215, 90); ctx.fillText("RF", 340, 120);

            // 실감나는 타격 스트라이크 존 시각 가이드라인
            ctx.fillStyle = "rgba(234, 179, 8, 0.25)"; ctx.fillRect(0, 460, 440, 50);
            ctx.strokeStyle = "#eab308"; ctx.lineWidth = 2; ctx.strokeRect(0, 460, 440, 50);
        }

        function runMainLoop() {
            renderStadium();

            if (ball.active) {
                // 구종 궤적 커스텀 적용 물리엔진
                if (ball.type === "slider") ball.x += ball.vx;
                ball.y += ball.vy;
                ball.radius += 0.2;

                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
                ctx.fillStyle = "#ffffff"; ctx.fill();
                ctx.strokeStyle = "#334155"; ctx.stroke(); ctx.closePath();

                if (ball.y > 545) {
                    ball.active = false;
                    if (isTop) { showFeedback("스트라이크!", "#ef4444"); recordStrike(); }
                    else { showFeedback("루킹 스트라이크!", "#38bdf8"); recordStrike(); }
                }
            }

            // 배트 회전 타격 애니메이션 구조
            if (isSwinging) {
                swingFrame++;
                ctx.save(); ctx.translate(220, 490);
                ctx.rotate((swingFrame * 22 - 45) * Math.PI / 180);
                ctx.fillStyle = "#d97706"; ctx.fillRect(0, -5, 55, 10); ctx.restore();
                if (swingFrame > 8) isSwinging = false;
            } else {
                ctx.save(); ctx.translate(220, 490); ctx.rotate(-45 * Math.PI / 180);
                ctx.fillStyle = "#d97706"; ctx.fillRect(0, -5, 45, 9); ctx.restore();
            }

            if (feedback.alpha > 0) {
                ctx.font = "bold 22px sans-serif"; ctx.fillStyle = feedback.color;
                ctx.save(); ctx.globalAlpha = feedback.alpha;
                ctx.fillText(feedback.text, 220 - ctx.measureText(feedback.text).width/2, 160);
                ctx.restore(); feedback.alpha -= 0.015;
            }

            requestAnimationFrame(runMainLoop);
        }

        runMainLoop();
    </script>
</body>
</html>
"""

components.html(baseball_pro_v2_html, height=680, scrolling=False)
