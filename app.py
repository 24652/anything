import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Premium Simulator", layout="wide")

premium_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KBO Premium Baseball</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center;
            background-color: #020617; color: #fff; font-family: 'Noto Sans KR', sans-serif;
            height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 900px; height: 520px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.95); border-radius: 16px;
            overflow: hidden; border: 2px solid #334155; background: #000;
        }
        canvas { display: block; }

        /* KBO 로비 화면 */
        #lobbyOverlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 100;
        }
        .lobby-title { font-size: 36px; font-weight: 900; background: linear-gradient(to right, #60a5fa, #34d399); -webkit-background-clip: text; color: transparent; margin-bottom: 5px; text-shadow: 0 4px 15px rgba(59, 130, 246, 0.5); }
        .team-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 25px; width: 80%; }
        .team-card {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            padding: 15px 10px; border-radius: 10px; cursor: pointer; text-align: center;
            transition: all 0.2s ease; font-weight: 900; font-size: 15px; color: #e2e8f0;
        }
        .team-card:hover { background: #2563eb; transform: translateY(-5px) scale(1.05); border-color: #60a5fa; box-shadow: 0 10px 20px rgba(37,99,235,0.4); }

        /* 게임 인게임 UI */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 92%; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
            border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);
            display: flex; justify-content: space-between; align-items: center; padding: 10px 25px; z-index: 10;
            box-sizing: border-box; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }
        .bso-row { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; font-weight: 900; font-size: 14px;}
        .circle { width: 13px; height: 13px; border-radius: 50%; background: #1e293b; border: 1px solid #334155; }
        .b-on { background: #34d399; box-shadow: 0 0 10px #34d399; border-color:#fff;}
        .s-on { background: #fbbf24; box-shadow: 0 0 10px #fbbf24; border-color:#fff;}
        .o-on { background: #ef4444; box-shadow: 0 0 10px #ef4444; border-color:#fff;}

        #turnIndicator {
            position: absolute; top: 85px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.8); padding: 6px 20px; border-radius: 20px;
            font-weight: 900; color: #fff; font-size: 15px; z-index: 10; border: 2px solid #34d399;
            box-shadow: 0 0 15px rgba(52, 211, 153, 0.4); letter-spacing: 1px;
        }

        #bottomControl {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 75px;
            background: linear-gradient(to top, rgba(15, 23, 42, 1), rgba(15, 23, 42, 0.8)); 
            display: flex; justify-content: center; gap: 30px; align-items: center; z-index: 20; 
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        .control-group { display: flex; flex-direction: column; gap: 5px; }
        select, input[type=range] {
            background: #0f172a; color: #fff; border: 1px solid #475569;
            padding: 6px 10px; border-radius: 6px; font-weight: bold; font-family: 'Noto Sans KR'; outline: none;
        }
        .action-btn {
            background: linear-gradient(135deg, #ef4444, #991b1b);
            padding: 12px 35px; border-radius: 8px; border: 1px solid #f87171; color: white;
            font-size: 18px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 15px rgba(239,68,68,0.4);
            transition: 0.1s;
        }
        .action-btn:active { transform: scale(0.92); }
        .btn-hit { background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-color: #60a5fa; box-shadow: 0 4px 15px rgba(59,130,246,0.4); }

        #msgOverlay {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            font-size: 36px; font-weight: 900; text-shadow: 0 5px 15px #000, 0 0 20px rgba(0,0,0,0.8); 
            z-index: 15; text-align: center; width: 100%; pointer-events: none;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="lobbyOverlay">
            <div class="lobby-title">KBO PREMIUM MANAGER</div>
            <p style="color:#94a3b8; font-weight:bold; letter-spacing: 1px;">나의 구단을 선택하세요</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>

        <div id="topScoreBoard">
            <div style="text-align:left; width:25%;">
                <div id="uiAwayTeam" style="font-size:12px; color:#94a3b8; font-weight:bold;">AWAY</div>
                <div id="scAway" style="font-size:28px; font-weight:900; color:#cbd5e1;">0</div>
            </div>
            <div style="text-align:center; width:50%;">
                <div id="uiInning" style="font-size:18px; font-weight:900; color:#fbbf24; text-shadow: 0 2px 4px #000;">1회초 (수비)</div>
                <div style="display:flex; justify-content:center; gap:25px; margin-top:5px;">
                    <div class="bso-row"><span style="color:#34d399">B</span> <div class="circle" id="b1"></div><div class="circle" id="b2"></div><div class="circle" id="b3"></div></div>
                    <div class="bso-row"><span style="color:#fbbf24">S</span> <div class="circle" id="s1"></div><div class="circle" id="s2"></div></div>
                    <div class="bso-row"><span style="color:#ef4444">O</span> <div class="circle" id="o1"></div><div class="circle" id="o2"></div></div>
                </div>
            </div>
            <div style="text-align:right; width:25%;">
                <div id="uiHomeTeam" style="font-size:12px; color:#60a5fa; font-weight:bold;">HOME (나)</div>
                <div id="scHome" style="font-size:28px; font-weight:900; color:#fff;">0</div>
            </div>
        </div>

        <div id="turnIndicator">MY TURN: 투구하기</div>
        <div id="msgOverlay">방향키로 조준하고 투구하세요</div>
        <canvas id="gameCanvas" width="900" height="520"></canvas>

        <div id="bottomControl">
            <div id="pitchControls" style="display:flex; gap:20px; align-items:center;">
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">투수 교체</label>
                    <select id="pitcherSelect" onchange="syncPitcher()"></select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구종</label>
                    <select id="ballSelect"></select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구속 (<span id="speedVal">145</span>km/h)</label>
                    <input type="range" id="speedSlider" min="120" max="160" value="145" oninput="document.getElementById('speedVal').innerText=this.value">
                </div>
                <button class="action-btn" onclick="actionBtnClick()">⚾ 투구 (Space)</button>
            </div>
            <div id="batControls" style="display:none; gap:20px; align-items:center;">
                <div style="font-size:15px; font-weight:900; color:#cbd5e1; letter-spacing:1px;">공이 들어오는 타이밍에 맞춰 타격하세요!</div>
                <button class="action-btn btn-hit" onclick="actionBtnClick()">💥 스윙 (Space)</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");

        // DB 셋업
        const kboDB = {
            "한화": [{n:"류현진", b:["포심", "체인지업", "커브"], s:148}, {n:"문동주", b:["포심", "슬라이더"], s:160}],
            "SSG": [{n:"김광현", b:["포심", "슬라이더"], s:152}, {n:"문승원", b:["포심", "커브"], s:150}],
            "KIA": [{n:"양현종", b:["포심", "체인지업"], s:150}, {n:"정해영", b:["포심", "슬라이더"], s:153}],
            "LG": [{n:"임찬규", b:["포심", "체인지업"], s:147}, {n:"유영찬", b:["포심", "슬라이더"], s:154}],
            "삼성": [{n:"원태인", b:["포심", "체인지업"], s:150}, {n:"오승환", b:["포심", "슬라이더"], s:149}],
            "두산": [{n:"곽빈", b:["포심", "커브"], s:155}, {n:"김택연", b:["포심", "슬라이더"], s:156}],
            "KT": [{n:"고영표", b:["체인지업", "커브"], s:145}, {n:"박영현", b:["포심", "슬라이더"], s:153}],
            "롯데": [{n:"반즈", b:["포심", "슬라이더"], s:150}, {n:"김원중", b:["포심", "포크"], s:152}],
            "NC": [{n:"신민혁", b:["포심", "체인지업"], s:147}, {n:"이용찬", b:["포심", "포크"], s:149}],
            "키움": [{n:"후라도", b:["포심", "커터"], s:152}, {n:"조상우", b:["포심", "슬라이더"], s:156}]
        };

        let myTeam = "", currentPitcher = null;
        let isPlayerBatting = false; 
        let state = "LOBBY"; 
        let aimX = 450, aimY = 340;
        let ball = { z: 100, active: false, x:450, y:220, targetX:450, targetY:340, type:'포심', trail:[] };
        let B=0, S=0, O=0, inning=1, scAway=0, scHome=0;
        let isSwinging = false; let swingTimer = 0;
        let floatingTexts = []; let screenShake = 0;

        // 야수 배열 (원근법을 위한 y정렬)
        const fielders = [
            {x: 220, y: 150, s: 0.45, pos:"좌익수"}, {x: 450, y: 135, s: 0.4, pos:"중견수"}, {x: 680, y: 150, s: 0.45, pos:"우익수"},
            {x: 290, y: 240, s: 0.7, pos:"3루수"}, {x: 370, y: 200, s: 0.6, pos:"유격수"}, {x: 530, y: 200, s: 0.6, pos:"2루수"}, {x: 610, y: 240, s: 0.7, pos:"1루수"}
        ];

        // 초기화 로비
        const teamGrid = document.getElementById("teamGrid");
        Object.keys(kboDB).forEach(team => {
            const card = document.createElement("div");
            card.className = "team-card"; card.innerText = team;
            card.onclick = () => selectTeam(team);
            teamGrid.appendChild(card);
        });

        function selectTeam(team) {
            myTeam = team; state = "READY";
            document.getElementById("lobbyOverlay").style.display = "none";
            document.getElementById("uiHomeTeam").innerText = `${team} (나)`;
            
            let opps = Object.keys(kboDB).filter(t => t !== team);
            document.getElementById("uiAwayTeam").innerText = opps[Math.floor(Math.random()*opps.length)] + " (상대)";

            const pSelect = document.getElementById("pitcherSelect");
            pSelect.innerHTML = "";
            kboDB[team].forEach(p => {
                const opt = document.createElement("option"); opt.value = p.n; opt.innerText = p.n; pSelect.appendChild(opt);
            });
            syncPitcher(); setupTurn();
        }

        function syncPitcher() {
            const pName = document.getElementById("pitcherSelect").value;
            currentPitcher = kboDB[myTeam].find(p => p.n === pName);
            const bSelect = document.getElementById("ballSelect");
            bSelect.innerHTML = "";
            currentPitcher.b.forEach(b => {
                const opt = document.createElement("option"); opt.value = b; opt.innerText = b; bSelect.appendChild(opt);
            });
            document.getElementById("speedSlider").max = currentPitcher.s;
            document.getElementById("speedSlider").value = currentPitcher.s - 5;
            document.getElementById('speedVal').innerText = document.getElementById("speedSlider").value;
        }

        // 조작
        document.addEventListener("keydown", (e) => {
            if(state === "READY" && !isPlayerBatting) {
                if(e.key === "ArrowLeft") aimX -= 12; if(e.key === "ArrowRight") aimX += 12;
                if(e.key === "ArrowUp") aimY -= 12; if(e.key === "ArrowDown") aimY += 12;
                aimX = Math.max(350, Math.min(550, aimX)); aimY = Math.max(220, Math.min(440, aimY));
            }
            if(e.key === " ") { e.preventDefault(); actionBtnClick(); }
        });

        function actionBtnClick() {
            if(!isPlayerBatting && state === "READY") throwBall();
            else if (isPlayerBatting && state === "ACTION" && !isSwinging) swingBat();
        }

        function setupTurn() {
            state = "READY"; isSwinging = false; ball.active = false; ball.trail = [];
            document.getElementById("pitchControls").style.display = isPlayerBatting ? "none" : "flex";
            document.getElementById("batControls").style.display = isPlayerBatting ? "flex" : "none";
            document.getElementById("turnIndicator").innerText = isPlayerBatting ? "MY TURN: 공격 (타격)" : "MY TURN: 수비 (투구)";
            document.getElementById("turnIndicator").style.borderColor = isPlayerBatting ? "#60a5fa" : "#f87171";
            
            if(isPlayerBatting) {
                msgDiv.style.display = "block"; msgDiv.innerText = "투수 와인드업 중...";
                setTimeout(aiThrowBall, 1500 + Math.random()*1500);
            } else {
                msgDiv.style.display = "block"; msgDiv.innerText = "조준 후 투구하세요 (Space)"; aimX = 450; aimY = 340;
            }
            updateUI();
        }

        function throwBall() {
            state = "ACTION"; msgDiv.style.display = "none";
            let spd = document.getElementById("speedSlider").value / 60;
            let type = document.getElementById("ballSelect").value;
            ball = { z:100, active:true, targetX:aimX, targetY:aimY, speed: spd, type: type, trail:[] };
        }

        function aiThrowBall() {
            if(state !== "READY" || !isPlayerBatting) return;
            state = "ACTION"; msgDiv.style.display = "none";
            let tx = 390 + Math.random()*120; let ty = 280 + Math.random()*130;
            ball = { z:100, active:true, targetX:tx, targetY:ty, speed: 2.3 + Math.random()*0.4, type: Math.random()>0.5?'포심':'커브', trail:[] };
        }

        function swingBat() {
            isSwinging = true; swingTimer = 15;
            if(ball.z > 5 && ball.z < 25) {
                let inZone = (ball.targetX > 380 && ball.targetX < 520 && ball.targetY > 260 && ball.targetY < 420);
                if(inZone) { processHitResult(true); return; }
            }
        }

        function evaluateResult() {
            ball.active = false;
            const inZone = (ball.targetX > 400 && ball.targetX < 500 && ball.targetY > 280 && ball.targetY < 400);
            
            if(!isPlayerBatting) {
                const aiSwingProb = inZone ? 0.8 : 0.25;
                if(Math.random() < aiSwingProb) {
                    isSwinging = true; swingTimer = 15;
                    if(Math.random() < 0.4) processHitResult(false);
                    else processHitResult(true);
                } else {
                    if(inZone) addStrike("루킹 스트라이크!"); else addBall("볼!");
                }
            } else {
                if(isSwinging) addStrike("헛스윙!");
                else { if(inZone) addStrike("스트라이크!"); else addBall("볼!"); }
            }
        }

        function processHitResult(isHit) {
            state = "RESULT"; ball.active = false; screenShake = 20;
            if(!isHit) { addStrike("헛스윙!"); return; }
            if(Math.random() > 0.6) { addFloat("💥 쾌조의 안타!", "#3b82f6"); advanceRun(1); B=0; S=0; } 
            else { addFloat("⚾ 아웃! (범타)", "#ef4444"); O++; B=0; S=0; checkOuts(); }
            setTimeout(setupTurn, 1600);
        }

        function addStrike(msg) { S++; addFloat(msg, "#fbbf24"); if(S>=3){ S=0; B=0; O++; addFloat("삼진 아웃!!", "#ef4444"); checkOuts(); } setTimeout(setupTurn, 1500); }
        function addBall(msg) { B++; addFloat(msg, "#34d399"); if(B>=4){ S=0; B=0; advanceRun(1); addFloat("볼넷 출루", "#60a5fa"); } setTimeout(setupTurn, 1500); }
        function advanceRun(pts) { if(isPlayerBatting) scHome+=pts; else scAway+=pts; updateUI(); }

        function checkOuts() {
            if(O>=3) {
                O=0; B=0; S=0; isPlayerBatting = !isPlayerBatting;
                if(!isPlayerBatting) inning++;
                addFloat("이닝 교대!", "#f87171");
            }
            updateUI();
        }

        function updateUI() {
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `circle ${B>=i?'b-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `circle ${S>=i?'s-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `circle ${O>=i?'o-on':''}`;
            document.getElementById("uiInning").innerText = `${inning}회${isPlayerBatting ? '말 공격' : '초 수비'}`;
            document.getElementById("scAway").innerText = scAway; document.getElementById("scHome").innerText = scHome;
        }

        function addFloat(txt, color) { floatingTexts.push({ t: txt, c: color, y: 250, a: 1.0 }); }

        // 프리미엄 그래픽 렌더링 엔진
        function drawStadium() {
            // 관중석 및 하늘 조명 그라데이션
            let skyGrad = ctx.createRadialGradient(450, 150, 50, 450, 150, 400);
            skyGrad.addColorStop(0, "#1e3a8a"); skyGrad.addColorStop(1, "#020617");
            ctx.fillStyle = skyGrad; ctx.fillRect(0,0,900,180);
            
            // 외야 펜스
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0,160,900,20);
            ctx.strokeStyle = "#fbbf24"; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0, 160); ctx.lineTo(900, 160); ctx.stroke();

            // 외야 잔디 투톤 스트라이프 (원근감 적용)
            for(let i=0; i<15; i++) {
                ctx.fillStyle = i%2===0 ? "#14532d" : "#166534";
                ctx.beginPath();
                ctx.moveTo(0, 180 + i*8); ctx.lineTo(900, 180 + i*8);
                ctx.lineTo(900, 180 + (i+1)*8); ctx.lineTo(0, 180 + (i+1)*8); ctx.fill();
            }

            // 파울 라인
            ctx.strokeStyle = "rgba(255,255,255,0.6)"; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(450, 470); ctx.lineTo(0, 180); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(450, 470); ctx.lineTo(900, 180); ctx.stroke();

            // 흙 내야 (그라데이션)
            let dirtGrad = ctx.createLinearGradient(0, 200, 0, 520);
            dirtGrad.addColorStop(0, "#7c2d12"); dirtGrad.addColorStop(1, "#451a03");
            ctx.fillStyle = dirtGrad; ctx.beginPath();
            ctx.moveTo(450, 190); ctx.lineTo(760, 320); ctx.lineTo(450, 480); ctx.lineTo(140, 320); ctx.fill();

            // 내야 잔디 다이아몬드
            ctx.fillStyle = "#15803d"; ctx.beginPath();
            ctx.moveTo(450, 230); ctx.lineTo(600, 310); ctx.lineTo(450, 390); ctx.lineTo(300, 310); ctx.fill();

            // 1, 2, 3루 베이스 (화이트 쿼드)
            ctx.fillStyle = "#f8fafc";
            const drawBase = (bx, by) => {
                ctx.beginPath(); ctx.moveTo(bx, by-5); ctx.lineTo(bx+10, by); ctx.lineTo(bx, by+5); ctx.lineTo(bx-10, by); ctx.fill();
            };
            drawBase(600, 310); // 1루
            drawBase(450, 230); // 2루
            drawBase(300, 310); // 3루

            // 투수 마운드 & 홈플레이트
            ctx.fillStyle = "#92400e"; ctx.beginPath(); ctx.ellipse(450, 250, 45, 18, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(440, 247, 20, 4); // 투수판
            
            ctx.beginPath(); ctx.moveTo(430, 450); ctx.lineTo(470, 450); ctx.lineTo(480, 465); ctx.lineTo(450, 480); ctx.lineTo(420, 465); ctx.fill();
        }

        function drawEntities() {
            // 야수들 그림자 & 디테일
            fielders.forEach(f => {
                ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.beginPath(); ctx.ellipse(f.x, f.y+18*f.s, 14*f.s, 5*f.s, 0, 0, Math.PI*2); ctx.fill(); // 그림자
                ctx.fillStyle = "#e2e8f0"; ctx.fillRect(f.x-6*f.s, f.y, 12*f.s, 20*f.s); // 몸통 (홈 유니폼)
                ctx.fillStyle = "#1e293b"; ctx.fillRect(f.x-6*f.s, f.y-6*f.s, 12*f.s, 6*f.s); // 모자
                ctx.fillStyle = "#fbcfe8"; ctx.beginPath(); ctx.arc(f.x, f.y-2*f.s, 4*f.s, 0, Math.PI*2); ctx.fill(); // 얼굴
            });

            // 투수
            ctx.fillStyle = "#cbd5e1"; ctx.fillRect(445, 210, 12, 35); // 몸
            ctx.fillStyle = "#0f172a"; ctx.fillRect(445, 200, 12, 8); // 모자
            ctx.fillStyle = "#fbcfe8"; ctx.beginPath(); ctx.arc(451, 208, 6, 0, Math.PI*2); ctx.fill();

            // 타자 & 역동적 배트
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(340, 350, 28, 95);
            ctx.fillStyle = "#0f172a"; ctx.beginPath(); ctx.arc(354, 335, 14, 0, Math.PI*2); ctx.fill(); // 헬멧
            
            ctx.save(); ctx.translate(368, 370);
            if(isSwinging) {
                ctx.rotate(55 * Math.PI/180); ctx.fillStyle = "#fbbf24"; ctx.fillRect(0, -6, 85, 12);
                swingTimer--; if(swingTimer<=0) isSwinging = false;
            } else {
                ctx.rotate(-50 * Math.PI/180); ctx.fillStyle = "#d97706"; ctx.fillRect(0, -5, 75, 10);
            }
            ctx.restore();
        }

        function drawBallEngine() {
            // 스트라이크 존 그리드 (네온 스타일)
            ctx.strokeStyle = "rgba(56, 189, 248, 0.4)"; ctx.lineWidth = 2;
            ctx.strokeRect(400, 280, 100, 120);
            ctx.strokeStyle = "rgba(56, 189, 248, 0.15)"; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(433, 280); ctx.lineTo(433, 400); ctx.moveTo(466, 280); ctx.lineTo(466, 400);
            ctx.moveTo(400, 320); ctx.lineTo(500, 320); ctx.moveTo(400, 360); ctx.lineTo(500, 360); ctx.stroke();

            // 조준점
            if(!isPlayerBatting && state === "READY") {
                ctx.strokeStyle = "#f43f5e"; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(aimX, aimY, 10, 0, Math.PI*2); ctx.stroke();
                ctx.fillStyle = "rgba(244, 63, 94, 0.3)"; ctx.fill();
            }

            // 투구 물리엔진 & 트레일(잔상) 이펙트
            if(ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100);
                
                let curveAmount = ball.type !== '포심' ? Math.sin(scale * Math.PI) * 60 : 0;
                let curX = 450 + (ball.targetX - 450) * scale + curveAmount;
                let curY = 220 + (ball.targetY - 220) * scale;
                let curRad = 3 + (16 * scale);

                // 트레일 저장
                ball.trail.push({x: curX, y: curY, r: curRad});
                if(ball.trail.length > 8) ball.trail.shift();

                // 트레일 렌더링
                ball.trail.forEach((t, i) => {
                    ctx.fillStyle = `rgba(255, 255, 255, ${i/10})`;
                    ctx.beginPath(); ctx.arc(t.x, t.y, t.r*0.9, 0, Math.PI*2); ctx.fill();
                });

                // 바닥 그림자 (마운드->홈 보간)
                let groundY = 250 + (450 - 250) * scale;
                ctx.fillStyle = "rgba(0,0,0,0.5)";
                ctx.beginPath(); ctx.ellipse(curX, groundY, curRad*1.3, curRad*0.35, 0, 0, Math.PI*2); ctx.fill();

                // 공 본체
                ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(curX, curY, curRad, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#94a3b8"; ctx.lineWidth=1.5; ctx.stroke();

                if(ball.z <= 0) evaluateResult();
            }
        }

        function loop() {
            if(state === "LOBBY") return;
            ctx.save();
            if (screenShake > 0) { ctx.translate((Math.random()-0.5)*screenShake, (Math.random()-0.5)*screenShake); screenShake--; }
            
            ctx.clearRect(0,0,900,520);
            drawStadium();
            drawEntities();
            drawBallEngine();

            // 플로팅 텍스트
            for(let i=floatingTexts.length-1; i>=0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 42px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                ctx.lineWidth = 6; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 450, ft.y);
                ctx.fillText(ft.t, 450, ft.y);
                ft.y -= 2; ft.a -= 0.02; ctx.globalAlpha = 1.0;
                if(ft.a <= 0) floatingTexts.splice(i, 1);
            }
            ctx.restore();
            requestAnimationFrame(loop);
        }
        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""

components.html(premium_baseball_html, height=550, width=950, scrolling=False)
