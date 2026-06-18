import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Ultimate Rule Edition", layout="wide")

# UI 깨짐 방지 및 정상 출력을 위해 크기 규격을 재조정하고 CSS 레이아웃을 보강했습니다.
ultimate_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KBO Ultimate Rule Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center;
            background-color: #020617; color: #fff; font-family: 'Noto Sans KR', sans-serif;
            height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 900px; height: 550px; /* 안정적인 높이 확보 */
            box-shadow: 0 20px 60px rgba(0,0,0,0.95); border-radius: 16px;
            overflow: hidden; border: 2px solid #334155; background: #020617;
        }
        canvas { display: block; cursor: crosshair; background: #000; }

        /* 로비 화면 최적화 (검은 화면 방지) */
        #lobbyOverlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 100; opacity: 1; transition: opacity 0.3s ease;
        }
        .lobby-title { font-size: 34px; font-weight: 900; background: linear-gradient(to right, #f43f5e, #eab308); -webkit-background-clip: text; color: transparent; margin-bottom: 5px; }
        .team-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 25px; width: 85%; }
        .team-card {
            background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
            padding: 18px 10px; border-radius: 10px; cursor: pointer; text-align: center;
            transition: all 0.2s ease; font-weight: 900; font-size: 16px; color: #e2e8f0;
        }
        .team-card:hover { background: rgba(255,255,255,0.2); transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,255,255,0.2); }

        /* 인게임 스코어보드 고정 */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 92%; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px);
            border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);
            display: flex; justify-content: space-between; align-items: center; padding: 10px 25px; z-index: 10;
            box-sizing: border-box;
        }
        .bso-row { display: flex; align-items: center; gap: 6px; font-weight: 900; font-size: 14px;}
        .circle { width: 13px; height: 13px; border-radius: 50%; background: #1e293b; border: 1px solid #334155; }
        .b-on { background: #34d399; box-shadow: 0 0 10px #34d399; }
        .s-on { background: #fbbf24; box-shadow: 0 0 10px #fbbf24; }
        .o-on { background: #ef4444; box-shadow: 0 0 10px #ef4444; }

        #turnIndicator {
            position: absolute; top: 90px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.85); padding: 4px 18px; border-radius: 20px;
            font-weight: 900; color: #fff; font-size: 13px; z-index: 10; border: 2px solid #34d399;
        }

        #bottomControl {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 80px;
            background: linear-gradient(to top, rgba(15, 23, 42, 1), rgba(15, 23, 42, 0.95)); 
            display: flex; justify-content: center; gap: 20px; align-items: center; z-index: 20; 
            border-top: 1px solid rgba(255,255,255,0.15);
        }
        .control-group { display: flex; flex-direction: column; gap: 3px; }
        select, input[type=range] {
            background: #0f172a; color: #fff; border: 1px solid #475569;
            padding: 5px 8px; border-radius: 6px; font-weight: bold; outline: none;
        }
        .action-btn {
            background: linear-gradient(135deg, #ef4444, #991b1b);
            padding: 10px 30px; border-radius: 8px; border: 1px solid #f87171; color: white;
            font-size: 15px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(239,68,68,0.3);
        }
        .btn-hit { background: linear-gradient(135deg, #3b82f6, #1e3a8a); border-color: #60a5fa; box-shadow: 0 4px 12px rgba(59,130,246,0.3); }

        #msgOverlay {
            position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%);
            font-size: 32px; font-weight: 900; text-shadow: 0 4px 12px #000; 
            z-index: 15; text-align: center; width: 100%; pointer-events: none;
        }
        
        #adminLockBtn {
            position: absolute; bottom: 95px; left: 15px; background: #1e293b; border: 1px solid #475569;
            color: #94a3b8; padding: 6px 12px; border-radius: 6px; font-size: 11px; cursor: pointer; z-index: 30;
        }
        #adminPanel {
            position: absolute; bottom: 95px; left: 15px; background: rgba(15, 23, 42, 0.95);
            padding: 12px; border-radius: 8px; border: 1px solid #ef4444; font-size: 11px; z-index: 30;
            line-height: 1.5; color: #cbd5e1; display: none;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="lobbyOverlay">
            <div class="lobby-title">KBO ULTIMATE RULE EDITION</div>
            <p style="color:#94a3b8; font-weight:bold;">구단을 선택하면 대진표가 구성되며 게임이 시작됩니다.</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>

        <div id="topScoreBoard">
            <div style="text-align:left; width:25%;">
                <div id="uiAwayTeam" style="font-size:12px; color:#94a3b8; font-weight:bold;">AWAY</div>
                <div id="scAway" style="font-size:26px; font-weight:900;">0</div>
            </div>
            <div style="text-align:center; width:50%;">
                <div id="uiInning" style="font-size:16px; font-weight:900; color:#fbbf24;">1회초 (수비)</div>
                <div style="display:flex; justify-content:center; gap:20px; margin-top:3px;">
                    <div class="bso-row"><span style="color:#34d399">B</span> <div class="circle" id="b1"></div><div class="circle" id="b2"></div><div class="circle" id="b3"></div></div>
                    <div class="bso-row"><span style="color:#fbbf24">S</span> <div class="circle" id="s1"></div><div class="circle" id="s2"></div></div>
                    <div class="bso-row"><span style="color:#ef4444">O</span> <div class="circle" id="o1"></div><div class="circle" id="o2"></div></div>
                </div>
            </div>
            <div style="text-align:right; width:25%;">
                <div id="uiHomeTeam" style="font-size:12px; color:#60a5fa; font-weight:bold;">HOME (나)</div>
                <div id="scHome" style="font-size:26px; font-weight:900;">0</div>
            </div>
        </div>

        <div id="turnIndicator">MY TURN: 투구하기</div>
        <div id="msgOverlay">구단을 선택해주세요!</div>
        
        <button id="adminLockBtn" onclick="unlockAdmin()">🔒 어드민 모드 인증</button>
        <div id="adminPanel">
            <b style="color:#ef4444; font-size:12px;">⚡ 어드민 활성화 (Shift + Key)</b><br>
            • <span style="color:#fbbf24">S</span>: 스트라이크 &nbsp;&nbsp; • <span style="color:#34d399">B</span>: 볼 추가<br>
            • <span style="color:#60a5fa">H</span>: 1루타 단타 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; • <span style="color:#a855f7">2</span> / <span style="color:#ec4899">3</span>: 2루타 / 3루타<br>
            • <span style="color:#f43f5e">R</span>: 즉시 홈런 폭발
        </div>

        <canvas id="gameCanvas" width="900" height="550"></canvas>

        <div id="bottomControl">
            <div id="pitchControls" style="display:flex; gap:15px; align-items:center;">
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">선수 명단</label>
                    <select id="pitcherSelect" onchange="syncPitcher()"></select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구종 선택</label>
                    <select id="ballSelect"></select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구속 (<span id="speedVal">145</span>km/h)</label>
                    <input type="range" id="speedSlider" min="120" max="162" value="145" oninput="document.getElementById('speedVal').innerText=this.value">
                </div>
                <button class="action-btn" onclick="actionBtnClick()">⚾ 투구 (Space)</button>
            </div>
            <div id="batControls" style="display:none; gap:20px; align-items:center;">
                <div style="font-size:14px; font-weight:900; color:#cbd5e1;">타이밍을 맞춰 배트를 휘두르세요!</div>
                <button class="action-btn btn-hit" onclick="actionBtnClick()">💥 스윙 (Space)</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");

        const kboDB = {
            "한화": { color: "#f97316", players: [{n:"류현진", b:["포심", "체인지업", "커브", "슬라이더"], s:149}, {n:"문동주", b:["포심", "슬라이더", "스플리터", "싱커"], s:161}]},
            "KIA": { color: "#ea580c", players: [{n:"양현종", b:["포심", "체인지업", "슬라이더", "커브"], s:148}, {n:"정해영", b:["포심", "슬라이더"], s:154}]},
            "삼성": { color: "#1d4ed8", players: [{n:"원태인", b:["포심", "체인지업", "커브", "컷패스트볼"], s:151}]},
            "LG": { color: "#a21caf", players: [{n:"임찬규", b:["체인지업", "포심", "커브", "슬라이더"], s:146}]},
            "두산": { color: "#1e293b", players: [{n:"곽빈", b:["포심", "커브", "슬라이더", "체인지업"], s:156}]}
        };

        let myTeam = "", oppTeam = "";
        let currentPitcher = null;
        let isPlayerBatting = false; 
        let state = "LOBBY"; 
        let adminAuthorized = false; 
        
        let aimX = 450, aimY = 340;
        let stamina = 100; 
        let ball = { z: 100, active: false, x:450, y:220, targetX:450, targetY:340, type:'포심', speed:2, trail:[] };
        let hitResultBall = { active: false, x: 450, y: 450, vx: 0, vy: 0, scale: 1, timer: 0 }; 
        
        let B=0, S=0, O=0, inning=1, scAway=0, scHome=0;
        let runners = [false, false, false]; 
        let isSwinging = false; let swingTimer = 0;
        let floatingTexts = []; let screenShake = 0;

        // 스트라이크 존 규격 (걸치기 판정을 위해 마진 계산 포함)
        const zone = { left: 395, right: 505, top: 275, bottom: 405 };

        const fielders = [
            {x: 200, y: 155, s: 0.45}, {x: 450, y: 135, s: 0.4}, {x: 700, y: 155, s: 0.45},
            {x: 270, y: 250, s: 0.68}, {x: 360, y: 205, s: 0.58}, {x: 540, y: 205, s: 0.58}, {x: 630, y: 250, s: 0.68}
        ];

        function unlockAdmin() {
            let pw = prompt("어드민 해제 비밀번호를 입력하세요:");
            if(pw === "JOONMIN") {
                adminAuthorized = true;
                document.getElementById("adminLockBtn").style.display = "none";
                document.getElementById("adminPanel").style.display = "block";
                addFloat("🔒 어드민 모드 오픈!", "#ef4444");
            } else { alert("비밀번호가 틀렸습니다!"); }
        }

        // 마우스 조준 시스템
        canvas.addEventListener("mousedown", (e) => {
            if (state === "READY" && !isPlayerBatting) {
                const rect = canvas.getBoundingClientRect();
                aimX = e.clientX - rect.left; aimY = e.clientY - rect.top;
                // 투구 가능 범위 제한
                aimX = Math.max(300, Math.min(600, aimX));
                aimY = Math.max(180, Math.min(480, aimY));
            }
        });

        // 대기 화면 로드 함수
        const teamGrid = document.getElementById("teamGrid");
        Object.keys(kboDB).forEach(team => {
            const card = document.createElement("div");
            card.className = "team-card"; card.innerText = team;
            card.onclick = () => selectTeam(team);
            teamGrid.appendChild(card);
        });

        function selectTeam(team) {
            myTeam = team; state = "READY";
            document.getElementById("lobbyOverlay").style.style.display = "none";
            document.getElementById("lobbyOverlay").remove(); // 레이어 제거로 검은 화면 완전 해결
            document.getElementById("uiHomeTeam").innerText = `${team} (나)`;
            
            let opps = Object.keys(kboDB).filter(t => t !== team);
            oppTeam = opps[Math.floor(Math.random()*opps.length)];
            document.getElementById("uiAwayTeam").innerText = oppTeam + " (상대)";

            const pSelect = document.getElementById("pitcherSelect");
            pSelect.innerHTML = "";
            kboDB[team].players.forEach(p => {
                const opt = document.createElement("option"); opt.value = p.n; opt.innerText = p.n; pSelect.appendChild(opt);
            });
            syncPitcher(); setupTurn();
        }

        function syncPitcher() {
            const pName = document.getElementById("pitcherSelect").value;
            currentPitcher = kboDB[myTeam].players.find(p => p.n === pName);
            const bSelect = document.getElementById("ballSelect");
            bSelect.innerHTML = "";
            currentPitcher.b.forEach(b => {
                const opt = document.createElement("option"); opt.value = b; opt.innerText = b; bSelect.appendChild(opt);
            });
            document.getElementById("speedSlider").max = currentPitcher.s;
            document.getElementById("speedSlider").value = currentPitcher.s - 4;
            document.getElementById('speedVal').innerText = document.getElementById("speedSlider").value;
            stamina = 100; 
        }

        document.addEventListener("keydown", (e) => {
            if(e.shiftKey && adminAuthorized) {
                e.preventDefault();
                if(e.key.toLowerCase() === "s") { S++; addFloat("ADMIN: 스트라이크", "#fbbf24"); checkOutsUI(); }
                if(e.key.toLowerCase() === "b") { B++; addFloat("ADMIN: 볼 선언", "#34d399"); checkOutsUI(); }
                if(e.key.toLowerCase() === "h") { processHitData(1, "안타!"); }
                if(e.key === "2") { processHitData(2, "2루타!!"); }
                if(e.key === "3") { processHitData(3, "3루타!!!"); }
                if(e.key.toLowerCase() === "r") { processHitData(4, "🎁 대형 홈런 🚀"); }
                updateUI(); return;
            }
            if(e.key === " ") { e.preventDefault(); actionBtnClick(); }
        });

        function actionBtnClick() {
            if(state === "GAMEOVER") return;
            if(!isPlayerBatting && state === "READY") throwBall();
            else if (isPlayerBatting && state === "ACTION" && !isSwinging) swingBat();
        }

        function setupTurn() {
            if(state === "GAMEOVER") return;
            state = "READY"; isSwinging = false; ball.active = false; ball.trail = [];
            document.getElementById("pitchControls").style.display = isPlayerBatting ? "none" : "flex";
            document.getElementById("batControls").style.display = isPlayerBatting ? "flex" : "none";
            document.getElementById("turnIndicator").innerText = isPlayerBatting ? "MY TURN: 공격 (타격)" : "MY TURN: 수비 (투구)";
            
            if(isPlayerBatting) {
                msgDiv.style.display = "block"; msgDiv.innerText = "상대 투수 투구 준비 중...";
                setTimeout(aiThrowBall, 1200 + Math.random()*1200);
            } else {
                msgDiv.style.display = "block"; msgDiv.innerText = "마우스 조준 후 투구(Space)";
            }
            updateUI();
        }

        function throwBall() {
            state = "ACTION"; msgDiv.style.display = "none";
            let spd = document.getElementById("speedSlider").value / 58;
            let type = document.getElementById("ballSelect").value;
            
            stamina = Math.max(0, stamina - 5);
            
            // ⭐ [확률 기반 제구 오차 물리엔진 구현] 체력이 부족하면 조준이 빗나감
            let finalX = aimX; let finalY = aimY;
            let wildPitchChance = (100 - stamina) / 100; 
            
            if(Math.random() < wildPitchChance || stamina < 50) {
                let errorRange = (100 - stamina) * 1.3 + 20;
                finalX += (Math.random() - 0.5) * errorRange;
                finalY += (Math.random() - 0.5) * errorRange;
            }
            
            ball = { z:100, active:true, targetX:finalX, targetY:finalY, speed: spd, type: type, trail:[] };
        }

        function aiThrowBall() {
            if(state !== "READY" || !isPlayerBatting) return;
            state = "ACTION"; msgDiv.style.display = "none";
            let tx = 360 + Math.random()*180; let ty = 240 + Math.random()*180;
            let rTypes = ["포심","슬라이더","커브","포크"];
            ball = { z:100, active:true, targetX:tx, targetY:ty, speed: 2.2 + Math.random()*0.5, type: rTypes[Math.floor(Math.random()*rTypes.length)], trail:[] };
        }

        function swingBat() {
            isSwinging = true; swingTimer = 15;
            if(ball.z > 4 && ball.z < 24) {
                let hitDist = Math.hypot(ball.targetX - 450, ball.targetY - 340);
                if(hitDist < 75) { triggerHitTrajectory(); return; }
            }
        }

        function evaluateResult() {
            ball.active = false;
            let bRad = 12; // 걸치기 판정을 위한 여유 마진

            // ⭐ [야구 규칙 추가 1]: 스트라이크 존 경계선에 조금이라도 걸치면 스트라이크 판정
            const isStrike = (ball.targetX + bRad >= zone.left && ball.targetX - bRad <= zone.right &&
                              ball.targetY + bRad >= zone.top && ball.targetY - bRad <= zone.bottom);
                              
            // ⭐ [야구 규칙 추가 2]: 타자 몸쪽(좌측 핫존) 깊숙하게 들어오면 몸에 맞는 공(데드볼) 판정
            const isHitByPitch = (ball.targetX > 310 && ball.targetX < 365 && ball.targetY > 320 && ball.targetY < 440);

            if (isHitByPitch) {
                processHitData(1, "💥 몸에 맞는 공 (사구 출루)!");
                setTimeout(setupTurn, 1200);
                return;
            }

            if(!isPlayerBatting) {
                const aiSwingProb = isStrike ? 0.75 : 0.18;
                if(Math.random() < aiSwingProb) {
                    isSwinging = true; swingTimer = 15;
                    if(Math.random() < 0.42) { triggerHitTrajectory(); } else { addStrike("헛스윙!"); }
                } else {
                    if(isStrike) addStrike("루킹 스트라이크!"); else addBall("볼!");
                }
            } else {
                if(isSwinging) addStrike("헛스윙!");
                else { if(isStrike) addStrike("스트라이크!", true); else addBall("볼!"); }
            }
        }

        function triggerHitTrajectory() {
            state = "RESULT"; ball.active = false; screenShake = 25;
            let isHomeRun = Math.random() > 0.88;
            let bases = isHomeRun ? 4 : Math.floor(Math.random() * 3) + 1;
            let label = bases === 1 ? "안타!" : (bases === 2 ? "2루타!!" : (bases === 3 ? "3루타!!!" : "💥 홈런!!!!"));
            
            let angle = -Math.PI/2 + (Math.random() - 0.5) * 1.1;
            let force = bases * 4 + 7;
            hitResultBall = {
                active: true, x: 450, y: 440, vx: Math.cos(angle) * force, vy: Math.sin(angle) * force,
                scale: 1, timer: 70, bases: bases, label: label
            };
        }

        function processHitData(bases, title) {
            addFloat(title, bases === 4 ? "#f43f5e" : "#60a5fa");
            let runsScored = 0;
            for(let b = 0; b < bases; b++) {
                if(runners[2]) { runsScored++; runners[2] = false; }
                if(runners[1]) { runners[2] = true; runners[1] = false; }
                if(runners[0]) { runners[1] = true; runners[0] = false; }
                if(b === 0 && bases < 4) { runners[0] = true; }
            }
            if(bases === 4) { runsScored++; } 
            
            if(runsScored > 0) {
                if(isPlayerBatting) scHome += runsScored; else scAway += runsScored;
                addFloat(`+${runsScored}득점!`, "#eab308");
            }
            B = 0; S = 0; updateUI();
        }

        function addStrike(msg, looking = false) { S++; addFloat(msg, looking ? "#fbbf24" : "#f59e0b"); checkOutsUI(); }
        function addBall(msg) { B++; addFloat(msg, "#10b981"); if(B>=4){ S=0; B=0; processHitData(1, "볼넷(Walk) 출루!"); } updateUI(); }

        function checkOutsUI() {
            if(S >= 3) { S = 0; B = 0; O++; addFloat("삼진 아웃!", "#ef4444"); }
            if(O >= 3) {
                O = 0; B = 0; S = 0; runners = [false, false, false];
                // 9회말 공격 종료 시 정규 이닝 세트 스코어 계산 후 강제 종료
                if (inning >= 9 && isPlayerBatting) { endGame(); return; }
                isPlayerBatting = !isPlayerBatting;
                if(!isPlayerBatting) inning++;
                addFloat("💥 공수전환", "#ec4899");
            }
            updateUI();
        }

        function endGame() {
            state = "GAMEOVER";
            let winner = scHome > scAway ? `${myTeam} 승리!` : (scHome < scAway ? `${oppTeam} 승리!` : "무승부!");
            msgDiv.style.display = "block"; msgDiv.style.color = "#fbbf24";
            msgDiv.innerHTML = `🏁 9이닝 정규 경기 종료<br><span style="font-size:24px; color:#fff;">최종 스코어 ${scAway} : ${scHome}<br>${winner}</span>`;
            document.getElementById("pitchControls").style.display = "none";
            document.getElementById("batControls").style.display = "none";
        }

        function updateUI() {
            if(state === "GAMEOVER") return;
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `circle ${B>=i?'b-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `circle ${S>=i?'s-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `circle ${O>=i?'o-on':''}`;
            document.getElementById("uiInning").innerText = `${inning}회${isPlayerBatting ? '말 (공격)' : '초 (수비)'}`;
            document.getElementById("scAway").innerText = scAway; document.getElementById("scHome").innerText = scHome;
        }

        function addFloat(txt, color) { floatingTexts.push({ t: txt, c: color, y: 240, a: 1.0 }); }

        function drawStadium() {
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0,0,900,550);
            
            let skyGrad = ctx.createRadialGradient(450, 150, 40, 450, 150, 420);
            skyGrad.addColorStop(0, "#1e1b4b"); skyGrad.addColorStop(1, "#020617");
            ctx.fillStyle = skyGrad; ctx.fillRect(0,0,900,180);
            ctx.fillStyle = "#1e293b"; ctx.fillRect(0,160,900,20);

            for(let i=0; i<15; i++) {
                ctx.fillStyle = i%2===0 ? "#064e3b" : "#065f46"; ctx.fillRect(0, 180 + i*8, 900, 8);
            }

            ctx.strokeStyle = "rgba(255,255,255,0.55)"; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(450, 470); ctx.lineTo(20, 180); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(450, 470); ctx.lineTo(880, 180); ctx.stroke();

            let dirtGrad = ctx.createLinearGradient(0, 200, 0, 520);
            dirtGrad.addColorStop(0, "#7c2d12"); dirtGrad.addColorStop(1, "#431407");
            ctx.fillStyle = dirtGrad; ctx.beginPath();
            ctx.moveTo(450, 190); ctx.lineTo(770, 325); ctx.lineTo(450, 485); ctx.lineTo(130, 325); ctx.fill();

            ctx.fillStyle = "#047857"; ctx.beginPath();
            ctx.moveTo(450, 230); ctx.lineTo(610, 315); ctx.lineTo(450, 400); ctx.lineTo(290, 315); ctx.fill();

            const drawDiamondBase = (bx, by, occupied) => {
                ctx.fillStyle = occupied ? "#ef4444" : "#ffffff";
                ctx.beginPath(); ctx.moveTo(bx, by-6); ctx.lineTo(bx+11, by); ctx.lineTo(bx, by+6); ctx.lineTo(bx-11, by); ctx.fill();
            };
            drawDiamondBase(610, 315, runners[0]); drawDiamondBase(450, 230, runners[1]); drawDiamondBase(290, 315, runners[2]); 

            ctx.fillStyle = "#9a3412"; ctx.beginPath(); ctx.ellipse(450, 252, 48, 16, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(438, 249, 24, 4);
            ctx.beginPath(); ctx.moveTo(432, 455); ctx.lineTo(468, 455); ctx.lineTo(476, 468); ctx.lineTo(450, 480); ctx.lineTo(424, 468); ctx.fill();
        }

        function drawEntities() {
            let myTeamColor = kboDB[myTeam]?.color || "#cbd5e1";
            let oppTeamColor = kboDB[oppTeam]?.color || "#475569";

            fielders.forEach(f => {
                ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.beginPath(); ctx.ellipse(f.x, f.y+18*f.s, 14*f.s, 5*f.s, 0, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = isPlayerBatting ? myTeamColor : oppTeamColor; ctx.fillRect(f.x-6*f.s, f.y, 12*f.s, 20*f.s);
                ctx.fillStyle = "#ffedd5"; ctx.beginPath(); ctx.arc(f.x, f.y-2*f.s, 4*f.s, 0, Math.PI*2); ctx.fill();
            });

            let pColor = isPlayerBatting ? oppTeamColor : myTeamColor;
            ctx.fillStyle = pColor; ctx.fillRect(444, 210, 13, 33);
            ctx.fillStyle = "#ffedd5"; ctx.beginPath(); ctx.arc(450.5, 209, 6, 0, Math.PI*2); ctx.fill();

            let tColor = isPlayerBatting ? myTeamColor : oppTeamColor;
            ctx.fillStyle = tColor; ctx.fillRect(342, 355, 26, 75);
            ctx.fillStyle = "#0f172a"; ctx.beginPath(); ctx.arc(355, 342, 13, 0, Math.PI*2); ctx.fill();
            
            ctx.save(); ctx.translate(365, 375);
            if(isSwinging) { ctx.rotate(60 * Math.PI/180); ctx.fillStyle = "#eab308"; ctx.fillRect(0, -6, 85, 12); } 
            else { ctx.rotate(-45 * Math.PI/180); ctx.fillStyle = "#b45309"; ctx.fillRect(0, -5, 75, 10); }
            ctx.restore();

            if(!isPlayerBatting) {
                ctx.fillStyle = "rgba(15,23,42,0.6)"; ctx.fillRect(400, 255, 100, 6);
                ctx.fillStyle = stamina > 40 ? "#10b981" : "#ef4444"; ctx.fillRect(400, 255, stamina, 6);
            }
        }

        function drawBallEngine() {
            ctx.strokeStyle = "rgba(56, 189, 248, 0.5)"; ctx.lineWidth = 2; 
            ctx.strokeRect(zone.left, zone.top, zone.right - zone.left, zone.bottom - zone.top);
            
            if(!isPlayerBatting && state === "READY") {
                ctx.strokeStyle = stamina < 50 ? "#eab308" : "#f43f5e"; ctx.lineWidth=3;
                ctx.beginPath(); ctx.arc(aimX, aimY, 12, 0, Math.PI*2); ctx.stroke();
            }

            if(ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100);
                
                let dx = 0; let dy = 0;
                if(ball.type === "슬라이더") dx = Math.sin(scale * Math.PI) * 55;
                if(ball.type === "커브") { dx = Math.sin(scale * Math.PI) * 35; dy = Math.sin(scale * Math.PI) * 45; }
                if(ball.type === "포크") dy = Math.pow(scale, 2) * 55;

                let curX = 450 + (ball.targetX - 450) * scale + dx;
                let curY = 220 + (ball.targetY - 220) * scale + dy;
                let curRad = 3 + (15 * scale);

                ball.trail.push({x: curX, y: curY, r: curRad});
                if(ball.trail.length > 5) ball.trail.shift();
                ball.trail.forEach((t, i) => {
                    ctx.fillStyle = `rgba(255, 255, 255, ${i/10})`; ctx.beginPath(); ctx.arc(t.x, t.y, t.r, 0, Math.PI*2); ctx.fill();
                });

                ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(curX, curY, curRad, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#475569"; ctx.stroke();

                if(ball.z <= 0) evaluateResult();
            }

            if(hitResultBall.active) {
                hitResultBall.x += hitResultBall.vx; hitResultBall.y += hitResultBall.vy; hitResultBall.timer--;
                hitResultBall.scale = 1 + Math.sin((hitResultBall.timer / 70) * Math.PI) * 1.8;

                ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#000";
                ctx.beginPath(); ctx.arc(hitResultBall.x, hitResultBall.y, 5 * hitResultBall.scale, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                if(hitResultBall.timer <= 0) {
                    hitResultBall.active = false;
                    processHitData(hitResultBall.bases, hitResultBall.label);
                    setTimeout(setupTurn, 1000);
                }
            }
        }

        function loop() {
            requestAnimationFrame(loop);
            if(state === "LOBBY") return;

            ctx.save();
            if (screenShake > 0) { ctx.translate((Math.random()-0.5)*screenShake, (Math.random()-0.5)*screenShake); screenShake--; }
            
            ctx.clearRect(0,0,900,550);
            drawStadium(); drawEntities(); drawBallEngine();

            if(isSwinging && swingTimer <= 0) isSwinging = false;

            for(let i = floatingTexts.length - 1; i >= 0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 38px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                ctx.fillText(ft.t, 450, ft.y);
                ft.y -= 1.5; ft.a -= 0.025; ctx.globalAlpha = 1.0;
                if(ft.a <= 0) floatingTexts.splice(i, 1);
            }
            ctx.restore();
        }
        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""

components.html(ultimate_baseball_html, height=580, width=950, scrolling=False)
