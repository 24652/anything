import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Premium Simulator", layout="wide")

premium_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KBO Premium Baseball V5</title>
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
            display: flex; justify-content: center; gap: 20px; align-items: center; z-index: 20; 
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
            <div class="lobby-title">KBO PREMIUM MANAGER V5</div>
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
            <div id="pitchControls" style="display:flex; gap:15px; align-items:center;">
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">투수 교체</label>
                    <select id="pitcherSelect" onchange="syncPitcher()"></select>
                </div>
                <div class="control-group" style="width: 100px;">
                    <label style="font-size:11px; color:#94a3b8;">체력: <span id="staminaVal">100</span>%</label>
                    <div style="width:100%; height:10px; background:#1e293b; border-radius:5px; border:1px solid #475569; overflow:hidden; margin-top:4px;">
                        <div id="staminaFill" style="width:100%; height:100%; background:#34d399; transition: 0.3s;"></div>
                    </div>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구종</label>
                    <select id="ballSelect"></select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구속 (<span id="speedVal">145</span>km)</label>
                    <input type="range" id="speedSlider" min="110" max="160" value="145" oninput="document.getElementById('speedVal').innerText=this.value">
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

        // 체력(st) 추가 및 다양한 구종 추가 적용
        const kboDB = {
            "한화": [{n:"류현진", b:["포심", "체인지업", "커브", "커터"], s:148, st:100}, {n:"문동주", b:["포심", "슬라이더", "투심"], s:160, st:100}],
            "SSG": [{n:"김광현", b:["포심", "슬라이더", "체인지업"], s:152, st:100}, {n:"문승원", b:["포심", "커브", "스플리터"], s:150, st:100}],
            "KIA": [{n:"양현종", b:["포심", "체인지업", "슬라이더"], s:150, st:100}, {n:"정해영", b:["포심", "슬라이더", "포크볼"], s:153, st:100}],
            "LG": [{n:"임찬규", b:["포심", "체인지업", "커브"], s:147, st:100}, {n:"유영찬", b:["포심", "슬라이더", "스플리터"], s:154, st:100}],
            "삼성": [{n:"원태인", b:["포심", "체인지업", "슬라이더"], s:150, st:100}, {n:"오승환", b:["포심", "슬라이더", "투심"], s:149, st:100}],
            "두산": [{n:"곽빈", b:["포심", "커브", "포크볼"], s:155, st:100}, {n:"김택연", b:["포심", "슬라이더", "체인지업"], s:156, st:100}],
            "KT": [{n:"고영표", b:["투심", "체인지업", "커브"], s:145, st:100}, {n:"박영현", b:["포심", "체인지업", "슬라이더"], s:153, st:100}],
            "롯데": [{n:"반즈", b:["포심", "슬라이더", "투심"], s:150, st:100}, {n:"김원중", b:["포심", "포크볼", "커브"], s:152, st:100}],
            "NC": [{n:"신민혁", b:["포심", "체인지업", "커터"], s:147, st:100}, {n:"이용찬", b:["포심", "포크볼", "슬라이더"], s:149, st:100}],
            "키움": [{n:"후라도", b:["포심", "커터", "투심"], s:152, st:100}, {n:"조상우", b:["포심", "스플리터", "너클볼"], s:156, st:100}] // 조상우에게 특별히 너클볼 부여
        };

        let myTeam = "", currentPitcher = null;
        let isPlayerBatting = false; 
        let state = "LOBBY"; 
        let aimX = 450, aimY = 340;
        let ball = { z: 100, active: false, x:450, y:220, targetX:450, targetY:340, type:'포심', trail:[] };
        let B=0, S=0, O=0, inning=1, scAway=0, scHome=0;
        let isSwinging = false; let swingTimer = 0;
        let floatingTexts = []; let screenShake = 0;

        const fielders = [
            {x: 220, y: 150, s: 0.45}, {x: 450, y: 135, s: 0.4}, {x: 680, y: 150, s: 0.45},
            {x: 290, y: 240, s: 0.7}, {x: 370, y: 200, s: 0.6}, {x: 530, y: 200, s: 0.6}, {x: 610, y: 240, s: 0.7}
        ];

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
            updateStaminaUI();
        }

        function updateStaminaUI() {
            if(!currentPitcher) return;
            let st = currentPitcher.st;
            document.getElementById('staminaVal').innerText = st;
            let fill = document.getElementById('staminaFill');
            fill.style.width = st + '%';
            if(st > 50) fill.style.background = '#34d399'; // 초록
            else if(st > 25) fill.style.background = '#fbbf24'; // 노랑
            else fill.style.background = '#ef4444'; // 빨강
        }

        document.addEventListener("keydown", (e) => {
            if(state === "READY" && !isPlayerBatting) {
                if(e.key === "ArrowLeft") aimX -= 12; if(e.key === "ArrowRight") aimX += 12;
                if(e.key === "ArrowUp") aimY -= 12; if(e.key === "ArrowDown") aimY += 12;
                aimX = Math.max(350, Math.min(550, aimX)); aimY = Math.max(220, Math.min(4
