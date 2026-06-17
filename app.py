import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Real Pitcher Manager", layout="wide")

integrated_pro_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Real Pitcher Manager</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; justify-content: center; align-items: center;
            background-color: #05070a; color: #fff; font-family: 'Noto Sans KR', sans-serif;
            height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 850px; height: 480px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.9); border-radius: 20px;
            overflow: hidden; border: 3px solid #1e293b;
        }
        canvas { display: block; background: #000; }

        /* 팀 선택 화면 */
        #teamSelectOverlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 100;
        }
        .team-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin-top: 20px; }
        .team-card {
            background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
            padding: 15px; border-radius: 12px; cursor: pointer; text-align: center;
            transition: 0.2s; font-weight: 700; font-size: 14px;
        }
        .team-card:hover { background: #3b82f6; transform: translateY(-5px); }

        /* 게임 UI */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px);
            border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
            display: flex; justify-content: space-between; padding: 10px 25px; z-index: 10;
        }
        .bso-row { display: flex; align-items: center; gap: 5px; margin-bottom: 2px; }
        .circle { width: 12px; height: 12px; border-radius: 50%; background: #334155; }
        .b-on { background: #34d399; box-shadow: 0 0 8px #34d399; }
        .s-on { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
        .o-on { background: #ef4444; box-shadow: 0 0 8px #ef4444; }

        /* 컨트롤 패널 */
        #bottomControl {
            position: absolute; bottom: 0; left: 0; width: 100%;
            background: rgba(15, 23, 42, 0.95); display: flex; justify-content: space-around;
            align-items: center; padding: 15px 0; z-index: 20; border-top: 2px solid #334155;
        }
        .control-group { display: flex; flex-direction: column; gap: 5px; }
        select, input[type=range] {
            background: #1e293b; color: white; border: 1px solid #475569;
            padding: 8px; border-radius: 6px; font-weight: bold;
        }
        .pitch-btn {
            background: linear-gradient(to bottom, #ef4444, #b91c1c);
            padding: 15px 40px; border-radius: 10px; border: none; color: white;
            font-size: 18px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .pitch-btn:active { transform: scale(0.95); }

        #msgOverlay {
            position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%);
            font-size: 32px; font-weight: 900; text-shadow: 0 4px 10px #000; z-index: 15; text-align: center;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="teamSelectOverlay">
            <h1 style="margin-bottom:10px;">KBO LEAGUE PITCHER MANAGER</h1>
            <p style="color:#94a3b8">플레이할 구단을 선택하세요</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>

        <div id="topScoreBoard">
            <div style="text-align:left;">
                <div id="uiMyTeam" style="font-size:12px; color:#60a5fa;">한화 이글스</div>
                <div id="uiPitcher" style="font-size:18px; font-weight:900;">류현진</div>
            </div>
            <div style="text-align:center;">
                <div id="uiInning" style="font-size:16px; font-weight:900; color:#fbbf24;">1회말 수비</div>
                <div style="display:flex; gap:20px; margin-top:5px;">
                    <div class="bso-row">B <div class="circle" id="b1"></div><div class="circle" id="b2"></div><div class="circle" id="b3"></div></div>
                    <div class="bso-row">S <div class="circle" id="s1"></div><div class="circle" id="s2"></div></div>
                    <div class="bso-row">O <div class="circle" id="o1"></div><div class="circle" id="o2"></div></div>
                </div>
            </div>
            <div style="text-align:right;">
                <div id="uiAwayTeam" style="font-size:12px; color:#f87171;">상대 팀</div>
                <div id="uiBatter" style="font-size:18px; font-weight:900;">타자</div>
            </div>
        </div>

        <div id="msgOverlay">방향키로 조준하고 투구하세요!</div>
        <canvas id="gameCanvas" width="850" height="480"></canvas>

        <div id="bottomControl">
            <div class="control-group">
                <label style="font-size:11px; color:#94a3b8;">투수 교체</label>
                <select id="pitcherSelect" onchange="syncPitcher()"></select>
            </div>
            <div class="control-group">
                <label style="font-size:11px; color:#94a3b8;">구종 선택</label>
                <select id="ballSelect"></select>
            </div>
            <div class="control-group">
                <label style="font-size:11px; color:#94a3b8;">구속 설정 (<span id="speedVal">145</span>km)</label>
                <input type="range" id="speedSlider" min="120" max="160" value="145" oninput="document.getElementById('speedVal').innerText=this.value">
            </div>
            <button class="pitch-btn" onclick="throwBall()">PLAY BALL</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");

        // --- KBO 데이터베이스 ---
        const kboDB = {
            "한화 이글스": { pitchers: [{n:"류현진", b:["포심", "체인지업", "커브"], s:148}, {n:"문동주", b:["포심", "슬라이더", "커브"], s:160}] },
            "SSG 랜더스": { pitchers: [{n:"김광현", b:["포심", "슬라이더", "체인지업"], s:152}, {n:"문승원", b:["포심", "슬라이더"], s:150}] },
            "KIA 타이거즈": { pitchers: [{n:"양현종", b:["포심", "슬라이더", "체인지업"], s:150}, {n:"정해영", b:["포심", "슬라이더"], s:153}] },
            "LG 트윈스": { pitchers: [{n:"임찬규", b:["포심", "체인지업", "커브"], s:147}, {n:"유영찬", b:["포심", "슬라이더"], s:154}] },
            "삼성 라이온즈": { pitchers: [{n:"원태인", b:["포심", "체인지업", "슬라이더"], s:150}, {n:"오승환", b:["포심", "슬라이더"], s:149}] },
            "두산 베어스": { pitchers: [{n:"곽빈", b:["포심", "슬라이더", "커브"], s:155}, {n:"김택연", b:["포심", "슬라이더"], s:156}] },
            "KT 위즈": { pitchers: [{n:"고영표", b:["체인지업", "싱커", "커브"], s:145}, {n:"박영현", b:["포심", "슬라이더"], s:153}] },
            "롯데 자이언츠": { pitchers: [{n:"반즈", b:["포심", "슬라이더", "체인지업"], s:150}, {n:"김원중", b:["포심", "포크"], s:152}] },
            "NC 다이노스": { pitchers: [{n:"신민혁", b:["포심", "체인지업", "컷패스트볼"], s:147}, {n:"이용찬", b:["포심", "포크"], s:149}] },
            "키움 히어로즈": { pitchers: [{n:"후라도", b:["포심", "커터", "싱커", "체인지업"], s:152}, {n:"조상우", b:["포심", "슬라이더"], s:156}] }
        };

        let myTeam = "", currentPitcher = null;
        let aimX = 425, aimY = 320;
        let state = "READY";
        let ball = { z: 100, active: false };
        let B=0, S=0, O=0, inning=1;
        let isSwinging = false;

        // --- 초기화 및 팀 선택 ---
        const teamGrid = document.getElementById("teamGrid");
        Object.keys(kboDB).forEach(team => {
            const card = document.createElement("div");
            card.className = "team-card";
            card.innerText = team;
            card.onclick = () => selectTeam(team);
            teamGrid.appendChild(card);
        });

        function selectTeam(team) {
            myTeam = team;
            document.getElementById("teamSelectOverlay").style.display = "none";
            document.getElementById("uiMyTeam").innerText = team;
            
            const pSelect = document.getElementById("pitcherSelect");
            pSelect.innerHTML = "";
            kboDB[team].pitchers.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.n; opt.innerText = p.n;
                pSelect.appendChild(opt);
            });
            syncPitcher();
            nextBatter();
        }

        function syncPitcher() {
            const pName = document.getElementById("pitcherSelect").value;
            currentPitcher = kboDB[myTeam].pitchers.find(p => p.n === pName);
            document.getElementById("uiPitcher").innerText = pName;
            
            const bSelect = document.getElementById("ballSelect");
            bSelect.innerHTML = "";
            currentPitcher.b.forEach(b => {
                const opt = document.createElement("option");
                opt.value = b; opt.innerText = b;
                bSelect.appendChild(opt);
            });
            document.getElementById("speedSlider").max = currentPitcher.s;
            document.getElementById("speedSlider").value = currentPitcher.s - 5;
        }

        function nextBatter() {
            const batters = ["구자욱", "김도영", "홍창기", "최정", "양의지", "노시환", "오스틴", "페라자"];
            document.getElementById("uiBatter").innerText = batters[Math.floor(Math.random()*batters.length)];
        }

        // --- 조작 및 게임 로직 ---
        document.addEventListener("keydown", (e) => {
            if(state !== "READY") return;
            if(e.key === "ArrowLeft") aimX -= 10;
            if(e.key === "ArrowRight") aimX += 10;
            if(e.key === "ArrowUp") aimY -= 10;
            if(e.key === "ArrowDown") aimY += 10;
            aimX = Math.max(300, Math.min(550, aimX));
            aimY = Math.max(200, Math.min(420, aimY));
            if(e.key === " ") throwBall();
        });

        function throwBall() {
            if(state !== "READY") return;
            state = "PITCHING";
            msgDiv.style.display = "none";
            ball = { z:100, active:true, x:425, y:200, targetX:aimX, targetY:aimY, speed: document.getElementById("speedSlider").value / 60 };
        }

        function evaluateResult() {
            ball.active = false;
            const inZone = (ball.targetX > 375 && ball.targetX < 475 && ball.targetY > 260 && ball.targetY < 380);
            
            // AI 타자 로직
            const swingProb = inZone ? 0.7 : 0.2;
            if(Math.random() < swingProb) {
                isSwinging = true;
                if(Math.random() < 0.6) { // 헛스윙
                    addS(); addFloat("헛스윙 스트라이크!", "#fbbf24");
                } else { // 안타 혹은 범타
                    if(Math.random() > 0.8) {
                        addFloat("💥 안타 허용!", "#f87171"); B=0; S=0;
                    } else {
                        addO(); addFloat("⚾ 범타 처리!", "#34d399"); B=0; S=0;
                    }
                }
            } else {
                if(inZone) { addS(); addFloat("루킹 스트라이크!", "#fbbf24"); }
                else { addB(); addFloat("볼!", "#34d399"); }
            }
            
            setTimeout(() => {
                state = "READY"; isSwinging = false;
                msgDiv.style.display = "block"; updateBSO();
            }, 1500);
        }

        function addS() { S++; if(S>=3){ S=0; B=0; addO(); addFloat("삼진!!", "#60a5fa"); } }
        function addB() { B++; if(B>=4){ S=0; B=0; addFloat("볼넷 허용", "#94a3b8"); } }
        function addO() { O++; if(O>=3){ O=0; inning++; addFloat("이닝 교대!", "#fbbf24"); } }
        
        function updateBSO() {
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `circle ${B>=i?'b-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `circle ${S>=i?'s-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `circle ${O>=i?'o-on':''}`;
            document.getElementById("uiInning").innerText = inning + "회말 수비";
        }

        function addFloat(txt, color) {
            msgDiv.innerText = txt; msgDiv.style.color = color; msgDiv.style.display = "block";
        }

        // --- 렌더링 루프 ---
        function draw() {
            ctx.clearRect(0,0,850,480);
            
            // 야구장 배경
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0,0,850,200); // 하늘
            ctx.fillStyle = "#166534"; ctx.fillRect(0,200,850,280); // 잔디
            
            // 흙 및 마운드
            ctx.fillStyle = "#92400e"; ctx.beginPath(); ctx.moveTo(425, 180); ctx.lineTo(750, 480); ctx.lineTo(100, 480); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(375, 430, 100, 10); // 홈플레이트
            
            // 스트라이크 존 가이드
            ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 2;
            ctx.strokeRect(375, 260, 100, 120);

            // 조준 마커
            if(state === "READY") {
                ctx.strokeStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(aimX, aimY, 10, 0, Math.PI*2); ctx.stroke();
            }

            // 투수 & 타자 실루엣
            ctx.fillStyle = "#cbd5e1"; ctx.fillRect(415, 180, 20, 50); // 투수
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(320, 350, 30, 100); // 타자

            // 공 투구 애니메이션
            if(ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100);
                let curX = 425 + (ball.targetX - 425) * scale;
                let curY = 200 + (ball.targetY - 200) * scale;
                ctx.fillStyle = "white"; ctx.beginPath(); ctx.arc(curX, curY, 3 + scale*10, 0, Math.PI*2); ctx.fill();
                if(ball.z <= 0) evaluateResult();
            }

            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

components.html(integrated_pro_baseball_html, height=520, width=900, scrolling=False)
