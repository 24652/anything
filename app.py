import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Real Simulator V3", layout="wide")

full_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KBO Real Simulator V3</title>
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

        /* 상태 전광판 */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px);
            border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
            display: flex; justify-content: space-between; padding: 10px 25px; z-index: 10;
            box-sizing: border-box;
        }
        .bso-row { display: flex; align-items: center; gap: 5px; margin-bottom: 2px; font-weight: bold; font-size: 14px;}
        .circle { width: 12px; height: 12px; border-radius: 50%; background: #334155; }
        .b-on { background: #34d399; box-shadow: 0 0 8px #34d399; }
        .s-on { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
        .o-on { background: #ef4444; box-shadow: 0 0 8px #ef4444; }

        /* 하단 컨트롤 패널 */
        #bottomControl {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 70px;
            background: rgba(15, 23, 42, 0.95); display: flex; justify-content: space-around;
            align-items: center; z-index: 20; border-top: 2px solid #334155;
        }
        .control-group { display: flex; flex-direction: column; gap: 4px; }
        select, input[type=range] {
            background: #1e293b; color: white; border: 1px solid #475569;
            padding: 5px; border-radius: 6px; font-weight: bold;
        }
        .action-btn {
            background: linear-gradient(to bottom, #ef4444, #b91c1c);
            padding: 10px 30px; border-radius: 10px; border: none; color: white;
            font-size: 18px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .action-btn:active { transform: scale(0.95); }
        .btn-hit { background: linear-gradient(to bottom, #3b82f6, #1d4ed8); }

        #msgOverlay {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            font-size: 28px; font-weight: 900; text-shadow: 0 4px 10px #000; z-index: 15; text-align: center;
        }
        #turnIndicator {
            position: absolute; top: 75px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.7); padding: 5px 15px; border-radius: 20px;
            font-weight: bold; color: #34d399; font-size: 14px; z-index: 10; border: 1px solid #34d399;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="topScoreBoard">
            <div style="text-align:left; width:25%;">
                <div style="font-size:12px; color:#94a3b8;">AWAY</div>
                <div id="scAway" style="font-size:24px; font-weight:900; color:#cbd5e1;">0</div>
            </div>
            <div style="text-align:center; width:50%;">
                <div id="uiInning" style="font-size:16px; font-weight:900; color:#fbbf24;">1회초 (수비)</div>
                <div style="display:flex; justify-content:center; gap:20px; margin-top:5px;">
                    <div class="bso-row"><span style="color:#34d399">B</span> <div class="circle" id="b1"></div><div class="circle" id="b2"></div><div class="circle" id="b3"></div></div>
                    <div class="bso-row"><span style="color:#fbbf24">S</span> <div class="circle" id="s1"></div><div class="circle" id="s2"></div></div>
                    <div class="bso-row"><span style="color:#ef4444">O</span> <div class="circle" id="o1"></div><div class="circle" id="o2"></div></div>
                </div>
            </div>
            <div style="text-align:right; width:25%;">
                <div style="font-size:12px; color:#94a3b8;">HOME (나)</div>
                <div id="scHome" style="font-size:24px; font-weight:900; color:#60a5fa;">0</div>
            </div>
        </div>

        <div id="turnIndicator">MY TURN: 투구하기</div>
        <div id="msgOverlay">방향키로 조준하고 투구하세요</div>
        <canvas id="gameCanvas" width="850" height="480"></canvas>

        <div id="bottomControl">
            <div id="pitchControls" style="display:flex; gap:15px; align-items:center;">
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구종</label>
                    <select id="ballSelect">
                        <option value="fast">포심 패스트볼</option>
                        <option value="curve">커브 / 슬라이더</option>
                    </select>
                </div>
                <div class="control-group">
                    <label style="font-size:11px; color:#94a3b8;">구속 (<span id="speedVal">145</span>km)</label>
                    <input type="range" id="speedSlider" min="120" max="155" value="145" oninput="document.getElementById('speedVal').innerText=this.value">
                </div>
                <button class="action-btn" onclick="actionBtnClick()">PITCH (Space)</button>
            </div>
            <div id="batControls" style="display:none; gap:15px; align-items:center;">
                <div style="font-size:14px; font-weight:bold; color:#cbd5e1;">투수가 던지는 타이밍에 맞춰 스윙하세요!</div>
                <button class="action-btn btn-hit" onclick="actionBtnClick()">SWING (Space)</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");

        // 게임 상태
        let isPlayerBatting = false; // False=수비(1회초), True=공격(1회말)
        let state = "READY"; // READY, ACTION, RESULT
        let aimX = 425, aimY = 320;
        let ball = { z: 100, active: false, x:425, y:200, targetX:425, targetY:320, type:'fast' };
        let B=0, S=0, O=0, inning=1, scAway=0, scHome=0;
        let isSwinging = false; let swingTimer = 0;
        let floatingTexts = [];

        // 야수 포지션 (x, y, scale)
        const fielders = [
            {x: 200, y: 130, s: 0.5},  // 좌익수
            {x: 425, y: 115, s: 0.45}, // 중견수
            {x: 650, y: 130, s: 0.5},  // 우익수
            {x: 280, y: 220, s: 0.75}, // 3루수
            {x: 350, y: 180, s: 0.65}, // 유격수
            {x: 500, y: 180, s: 0.65}, // 2루수
            {x: 570, y: 220, s: 0.75}  // 1루수
        ];

        // 키보드 조작
        document.addEventListener("keydown", (e) => {
            if(state === "READY" && !isPlayerBatting) {
                if(e.key === "ArrowLeft") aimX -= 12;
                if(e.key === "ArrowRight") aimX += 12;
                if(e.key === "ArrowUp") aimY -= 12;
                if(e.key === "ArrowDown") aimY += 12;
                aimX = Math.max(330, Math.min(520, aimX));
                aimY = Math.max(200, Math.min(410, aimY));
            }
            if(e.key === " ") {
                e.preventDefault();
                actionBtnClick();
            }
        });

        function actionBtnClick() {
            if(!isPlayerBatting && state === "READY") {
                // 투구하기
                throwBall();
            } else if (isPlayerBatting && state === "ACTION" && !isSwinging) {
                // 타격하기
                swingBat();
            }
        }

        function setupTurn() {
            state = "READY";
            isSwinging = false;
            document.getElementById("pitchControls").style.display = isPlayerBatting ? "none" : "flex";
            document.getElementById("batControls").style.display = isPlayerBatting ? "flex" : "none";
            document.getElementById("turnIndicator").innerText = isPlayerBatting ? "MY TURN: 공격 (타격)" : "MY TURN: 수비 (투구)";
            document.getElementById("turnIndicator").style.color = isPlayerBatting ? "#60a5fa" : "#f87171";
            document.getElementById("turnIndicator").style.borderColor = isPlayerBatting ? "#60a5fa" : "#f87171";
            
            if(isPlayerBatting) {
                msgDiv.style.display = "block";
                msgDiv.innerText = "투수가 투구 준비 중입니다...";
                setTimeout(aiThrowBall, 1500 + Math.random()*1000);
            } else {
                msgDiv.style.display = "block";
                msgDiv.innerText = "방향키로 조준하고 투구하세요";
                aimX = 425; aimY = 320;
            }
            updateUI();
        }

        function throwBall() {
            state = "ACTION"; msgDiv.style.display = "none";
            let spd = document.getElementById("speedSlider").value / 60;
            let type = document.getElementById("ballSelect").value;
            ball = { z:100, active:true, targetX:aimX, targetY:aimY, speed: spd, type: type };
        }

        function aiThrowBall() {
            if(state !== "READY" || !isPlayerBatting) return;
            state = "ACTION"; msgDiv.style.display = "none";
            // AI 랜덤 타겟 (스트라이크 존 근처)
            let tx = 375 + Math.random()*100;
            let ty = 260 + Math.random()*120;
            ball = { z:100, active:true, targetX:tx, targetY:ty, speed: 2.2 + Math.random()*0.5, type: Math.random()>0.5?'fast':'curve' };
        }

        function swingBat() {
            isSwinging = true; swingTimer = 15;
            // 타격 판정 로직 (공이 홈플레이트 z: 5~20 사이에 있을 때)
            if(ball.z > 5 && ball.z < 25) {
                // 스트라이크 존에 들어왔는지 체크
                let inZone = (ball.targetX > 360 && ball.targetX < 490 && ball.targetY > 240 && ball.targetY < 400);
                if(inZone) {
                    processHitResult(true);
                    return;
                }
            }
        }

        function evaluateResult() {
            ball.active = false;
            const inZone = (ball.targetX > 375 && ball.targetX < 475 && ball.targetY > 260 && ball.targetY < 380);
            
            if(!isPlayerBatting) {
                // 플레이어가 수비(투구) 중 -> AI 타자가 칠지 말지 결정
                const aiSwingProb = inZone ? 0.75 : 0.2;
                if(Math.random() < aiSwingProb) {
                    isSwinging = true; swingTimer = 15;
                    if(Math.random() < 0.5) processHitResult(false); // AI 헛스윙
                    else processHitResult(true); // AI 타격
                } else {
                    if(inZone) addStrike("루킹 스트라이크!"); else addBall("볼!");
                }
            } else {
                // 플레이어가 공격(타격) 중 -> 헛스윙이거나 안 쳤음
                if(isSwinging) {
                    addStrike("헛스윙!");
                } else {
                    if(inZone) addStrike("스트라이크!"); else addBall("볼!");
                }
            }
        }

        function processHitResult(isHit) {
            state = "RESULT"; ball.active = false;
            if(!isHit) { addStrike("헛스윙!"); return; }
            
            // 안타/범타 판정
            if(Math.random() > 0.6) {
                addFloat("💥 안타!", "#3b82f6"); advanceRun(1); B=0; S=0;
            } else {
                addFloat("⚾ 아웃! (범타)", "#ef4444"); O++; B=0; S=0; checkOuts();
            }
            setTimeout(setupTurn, 1500);
        }

        function addStrike(msg) { S++; addFloat(msg, "#fbbf24"); if(S>=3){ S=0; B=0; O++; addFloat("삼진 아웃!!", "#ef4444"); checkOuts(); } setTimeout(setupTurn, 1500); }
        function addBall(msg) { B++; addFloat(msg, "#34d399"); if(B>=4){ S=0; B=0; advanceRun(1); addFloat("볼넷 출루", "#60a5fa"); } setTimeout(setupTurn, 1500); }
        
        function advanceRun(pts) { if(isPlayerBatting) scHome+=pts; else scAway+=pts; updateUI(); }

        function checkOuts() {
            if(O>=3) {
                O=0; B=0; S=0;
                isPlayerBatting = !isPlayerBatting; // 공수교대
                if(!isPlayerBatting) inning++; // 1회말 종료 시 2회초로
                addFloat("공수 교대!", "#f87171");
            }
            updateUI();
        }

        function updateUI() {
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `circle ${B>=i?'b-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `circle ${S>=i?'s-on':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `circle ${O>=i?'o-on':''}`;
            document.getElementById("uiInning").innerText = `${inning}회${isPlayerBatting ? '말 (공격)' : '초 (수비)'}`;
            document.getElementById("scAway").innerText = scAway;
            document.getElementById("scHome").innerText = scHome;
        }

        function addFloat(txt, color) { floatingTexts.push({ t: txt, c: color, y: 220, a: 1.0 }); }

        function drawField() {
            // 하늘 & 잔디
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0,0,850,150);
            let grad = ctx.createLinearGradient(0,150,0,480);
            grad.addColorStop(0, "#14532d"); grad.addColorStop(1, "#166534");
            ctx.fillStyle = grad; ctx.fillRect(0,150,850,330);
            
            // 흙 다이아몬드
            ctx.fillStyle = "#7c2d12"; ctx.beginPath();
            ctx.moveTo(425, 170); ctx.lineTo(720, 300); ctx.lineTo(425, 450); ctx.lineTo(130, 300); ctx.fill();
            
            // 내야 잔디
            ctx.fillStyle = "#15803d"; ctx.beginPath();
            ctx.moveTo(425, 210); ctx.lineTo(580, 290); ctx.lineTo(425, 370); ctx.lineTo(270, 290); ctx.fill();

            // 마운드 & 홈
            ctx.fillStyle = "#92400e"; ctx.beginPath(); ctx.ellipse(425, 230, 40, 15, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(415, 227, 20, 3); // 투수판
            ctx.beginPath(); ctx.moveTo(405, 430); ctx.lineTo(445, 430); ctx.lineTo(455, 440); ctx.lineTo(425, 455); ctx.lineTo(395, 440); ctx.fill();
        }

        function drawCharacters() {
            // 야수들 (외야, 내야)
            ctx.fillStyle = "rgba(0,0,0,0.5)";
            fielders.forEach(f => {
                ctx.beginPath(); ctx.ellipse(f.x, f.y+15*f.s, 12*f.s, 4*f.s, 0, 0, Math.PI*2); ctx.fill(); // 그림자
                ctx.fillStyle = "#cbd5e1"; ctx.fillRect(f.x-5*f.s, f.y, 10*f.s, 18*f.s); // 몸
                ctx.beginPath(); ctx.arc(f.x, f.y-3*f.s, 5*f.s, 0, Math.PI*2); ctx.fill(); // 머리
                ctx.fillStyle = "rgba(0,0,0,0.5)";
            });

            // 투수
            ctx.fillStyle = "#e2e8f0"; ctx.fillRect(420, 195, 10, 30);
            ctx.beginPath(); ctx.arc(425, 190, 6, 0, Math.PI*2); ctx.fill();

            // 타자 & 배트 애니메이션
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(320, 330, 25, 90);
            ctx.beginPath(); ctx.arc(332, 315, 12, 0, Math.PI*2); ctx.fill();
            
            ctx.save(); ctx.translate(345, 350);
            if(isSwinging) {
                ctx.rotate(45 * Math.PI/180); ctx.fillStyle = "#b45309"; ctx.fillRect(0, -5, 70, 10);
                swingTimer--; if(swingTimer<=0) isSwinging = false;
            } else {
                ctx.rotate(-45 * Math.PI/180); ctx.fillStyle = "#b45309"; ctx.fillRect(0, -5, 60, 8);
            }
            ctx.restore();
        }

        function drawBallAndZone() {
            // 스트라이크 존 그리드
            ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 1;
            ctx.strokeRect(375, 260, 100, 120);
            ctx.beginPath(); ctx.moveTo(408, 260); ctx.lineTo(408, 380); ctx.moveTo(442, 260); ctx.lineTo(442, 380);
            ctx.moveTo(375, 300); ctx.lineTo(475, 300); ctx.moveTo(375, 340); ctx.lineTo(475, 340); ctx.stroke();

            // 플레이어 조준 마커 (수비 시에만)
            if(!isPlayerBatting && state === "READY") {
                ctx.strokeStyle = "#3b82f6"; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(aimX, aimY, 8, 0, Math.PI*2); ctx.stroke();
            }

            // 공 렌더링 (원근감 + 그림자)
            if(ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100);
                
                let curveX = ball.type === 'curve' ? Math.sin(scale * Math.PI) * 50 : 0;
                let curX = 425 + (ball.targetX - 425) * scale + curveX;
                let curY = 200 + (ball.targetY - 200) * scale;
                let curRad = 3 + (15 * scale);

                // 바닥 그림자 (Y축은 마운드~홈플레이트 바닥 선형 보간)
                let groundY = 230 + (430 - 230) * scale;
                ctx.fillStyle = "rgba(0,0,0,0.4)";
                ctx.beginPath(); ctx.ellipse(curX, groundY, curRad*1.2, curRad*0.3, 0, 0, Math.PI*2); ctx.fill();

                // 공 본체
                ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(curX, curY, curRad, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth=1; ctx.stroke();

                if(ball.z <= 0) evaluateResult();
            }
        }

        function loop() {
            ctx.clearRect(0,0,850,480);
            drawField();
            drawCharacters();
            drawBallAndZone();

            for(let i=floatingTexts.length-1; i>=0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 36px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                ctx.lineWidth = 5; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 425, ft.y);
                ctx.fillText(ft.t, 425, ft.y);
                ft.y -= 1.5; ft.a -= 0.02; ctx.globalAlpha = 1.0;
                if(ft.a <= 0) floatingTexts.splice(i, 1);
            }
            requestAnimationFrame(loop);
        }
        
        setupTurn();
        loop();
    </script>
</body>
</html>
"""

components.html(full_baseball_html, height=520, width=900, scrolling=False)
