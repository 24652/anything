import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Pitcher Simulator", layout="wide")
st.title("⚾ KBO 모바일 프로야구 (리얼 투수 매니저 에디션)")

pitcher_sim_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Pitcher Simulator</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center;
            background-color: #0b0f19; color: #fff; font-family: 'Noto Sans KR', sans-serif; height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 800px; height: 460px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8); border-radius: 16px; overflow: hidden; border: 2px solid #334155;
        }
        #gameCanvas { display: block; }
        
        /* UI 전광판 */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15); border-radius: 12px;
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 20px; box-sizing: border-box; z-index: 10;
        }
        .board-col { display: flex; flex-direction: column; align-items: center; }
        .inning-text { font-size: 16px; font-weight: 900; color: #fbbf24; }
        .score-text { font-size: 26px; font-weight: 900; letter-spacing: 2px; }
        .bso-board { display: flex; gap: 15px; font-weight: 700; font-size: 14px; }
        .bso-row { display: flex; align-items: center; gap: 4px; }
        .bso-circle { width: 12px; height: 12px; border-radius: 50%; background: #334155; }
        .b-active { background: #34d399; box-shadow: 0 0 6px #34d399; }
        .s-active { background: #fbbf24; box-shadow: 0 0 6px #fbbf24; }
        .o-active { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
        
        #msgOverlay {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 24px; font-weight: 900; color: #fff;
            text-shadow: 0px 4px 12px rgba(0,0,0,0.9); pointer-events: none; z-index: 15; width: 100%;
        }
        
        /* 투수 컨트롤 패널 */
        #controlPanel {
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            width: 92%; background: rgba(15, 23, 42, 0.9); padding: 10px; border-radius: 12px;
            display: flex; gap: 15px; justify-content: space-between; align-items: center; z-index: 10;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .panel-section { display: flex; flex-direction: column; gap: 4px; color: #94a3b8; font-size: 12px; font-weight: bold; }
        .modern-btn {
            background: linear-gradient(to bottom, #3b82f6, #1d4ed8); color: white;
            border: 1px solid #60a5fa; padding: 10px 16px; border-radius: 6px; font-weight: 900; font-size: 14px;
            cursor: pointer; font-family: 'Noto Sans KR';
        }
        .modern-btn:active { transform: scale(0.96); }
        .select-input {
            background: #1e293b; color: white; border: 1px solid #475569;
            padding: 8px; border-radius: 6px; font-weight: bold; font-family: 'Noto Sans KR';
        }
        .range-slider { width: 110px; accent-color: #3b82f6; }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="topScoreBoard">
            <div class="board-col" style="width: 25%; align-items: flex-start;">
                <div id="uiPitcherName" style="font-size:12px; color:#60a5fa; font-weight:900;">투수: 류현진</div>
                <div class="score-text" id="scAway" style="color:#cbd5e1">0</div>
            </div>
            <div class="board-col" style="width: 50%;">
                <div class="inning-text" id="uiInning">1회초 수비</div>
                <div class="bso-board">
                    <div class="bso-row"><span style="color:#34d399;">B</span>
                        <div class="bso-circle" id="b1"></div><div class="bso-circle" id="b2"></div><div class="bso-circle" id="b3"></div>
                    </div>
                    <div class="bso-row"><span style="color:#fbbf24;">S</span>
                        <div class="bso-circle" id="s1"></div><div class="bso-circle" id="s2"></div>
                    </div>
                    <div class="bso-row"><span style="color:#ef4444;">O</span>
                        <div class="bso-circle" id="o1"></div><div class="bso-circle" id="o2"></div>
                    </div>
                </div>
            </div>
            <div class="board-col" style="width: 25%; align-items: flex-end;">
                <div id="uiBatterName" style="font-size:12px; color:#f87171; font-weight:900;">타자: 이정후</div>
                <div class="score-text" id="scHome" style="color:#60a5fa">0</div>
            </div>
        </div>

        <div id="msgOverlay">방향키로 조준하고 투구하세요!</div>
        <canvas id="gameCanvas" width="800" height="460"></canvas>
        
        <div id="controlPanel">
            <div class="panel-section">
                <span>선수 선택</span>
                <select class="select-input" id="pitcherSelect" onchange="changePitcher()">
                    <option value="류현진">한화 류현진 (직구/체인지업)</option>
                    <option value="김광현">SSG 김광현 (직구/슬라이더)</option>
                    <option value="양현종">KIA 양현종 (직구/슬라이더)</option>
                </select>
            </div>
            <div class="panel-section">
                <span>구종 선택</span>
                <select class="select-input" id="ballTypeSelect">
                    </select>
            </div>
            <div class="panel-section">
                <span>구속 조절 (<span id="speedVal">145</span>km/h)</span>
                <input type="range" min="120" max="158" value="145" class="range-slider" id="speedSlider" oninput="document.getElementById('speedVal').innerText=this.value">
            </div>
            <div class="panel-section" style="color:#60a5fa; font-size:11px; justify-content:center;">
                🕹️ 위치 조절: 키보드 방향키<br>🕹️ 투구 동작: 스페이스바
            </div>
            <button class="modern-btn" style="background:linear-gradient(to bottom, #ef4444, #b91c1c); border-color:#f87171;" onclick="startPitching()">⚾ 플레이 볼!</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");
        const pSelect = document.getElementById("pitcherSelect");
        const tSelect = document.getElementById("ballTypeSelect");
        const sSlider = document.getElementById("speedSlider");

        const pitcherDB = {
            "류현진": { type: ["포심 직구", "서클 체인지업"], maxSpd: 148 },
            "김광현": { type: ["포심 직구", "고속 슬라이더"], maxSpd: 152 },
            "양현종": { type: ["포심 직구", "슬라이더"], maxSpd: 150 }
        };

        const batterPool = ["구자욱", "김도영", "홍창기", "최정", "양의지", "노시환"];

        let state = "PLAYING"; 
        let inning = 1; let isTop = false; // 플레이어가 투수(수비) 고정
        let scAway = 0; let scHome = 0;
        let B = 0, S = 0, O = 0;
        let bases = [false, false, false];
        let floatingTexts = [];
        let screenShake = 0;

        // 조준점 좌표 및 투구 데이터
        let aimX = 400, aimY = 315;
        let ball = { z: 100, x: 400, y: 170, active: false, speedZ: 2 };
        let isSwinging = false; let swingAngle = 0;
        let curBatter = batterPool[0];

        const zone = { x: 350, y: 260, w: 100, h: 110 };

        function changePitcher() {
            let p = pSelect.value;
            document.getElementById("uiPitcherName").innerText = `투수: ${p}`;
            tSelect.innerHTML = "";
            pitcherDB[p].type.forEach(t => {
                let opt = document.createElement("option");
                opt.value = t; opt.innerText = t;
                tSelect.appendChild(opt);
            });
            sSlider.max = pitcherDB[p].maxSpd;
            sSlider.value = pitcherDB[p].maxSpd - 5;
            document.getElementById('speedVal').innerText = sSlider.value;
        }

        function nextBatter() {
            curBatter = batterPool[Math.floor(Math.random() * batterPool.length)];
            document.getElementById("uiBatterName").innerText = `타자: ${curBatter}`;
        }

        function startPitching() {
            if (state !== "PLAYING") return;
            state = "PITCHING";
            msgDiv.style.display = "none";
            
            ball.z = 100; ball.active = true;
            // 구속 기반 Z축 속도 매핑
            ball.speedZ = parseFloat(sSlider.value) / 70;
        }

        // 방향키 조준점 이동 및 스페이스바 투구 제어
        document.addEventListener("keydown", (e) => {
            if (state === "PLAYING") {
                if (e.key === "ArrowLeft") aimX = Math.max(280, aimX - 8);
                if (e.key === "ArrowRight") aimX = Math.min(520, aimX + 8);
                if (e.key === "ArrowUp") aimY = Math.max(190, aimY - 8);
                if (e.key === "ArrowDown") aimY = Math.min(410, aimY + 8);
                if (e.key === " ") { e.preventDefault(); startPitching(); }
            }
        });

        function updateUI() {
            document.getElementById("uiInning").innerText = `${inning}회말 수비`;
            document.getElementById("scAway").innerText = scAway; 
            document.getElementById("scHome").innerText = scHome;
            
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `bso-circle ${B>=i ? 'b-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `bso-circle ${S>=i ? 's-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `bso-circle ${O>=i ? 'o-active':''}`;
        }

        // AI 타자 타격 메커니즘
        function evaluateAIHit() {
            ball.active = false;
            let isStrike = (aimX >= zone.x && aimX <= zone.x + zone.w && aimY >= zone.y && aimY <= zone.y + zone.h);
            
            // 스트라이크존 구석에 찔러넣었는지 여부 (피칭 퀄리티)
            let distFromCenter = Math.hypot(aimX - 400, aimY - 315);
            let edgePitch = isStrike && (distFromCenter > 45); 

            // AI 배트 스윙 결정 확률 계산
            let swingProb = isStrike ? 0.75 : 0.25;
            if (tSelect.value !== "포심 직구" && !isStrike) swingProb = 0.15; // 유인구 효과

            if (Math.random() < swingProb) {
                // 스윙 시도
                isSwinging = true; swingAngle = -60;
                
                // 타격 성공 및 범타/안타 판정 (구속이 빠르거나 보더라인 공이면 실책 유도)
                let contactProb = 0.6;
                if (edgePitch) contactProb -= 0.25;
                if (parseFloat(sSlider.value) > 150) contactProb -= 0.15;

                if (Math.random() < contactProb) {
                    // 안타 혹은 홈런 판정
                    if (Math.random() > 0.85 && isStrike && !edgePitch) {
                        addFloat("💥 홈런 피안타!", "#ef4444"); screenShake = 20; advanceRun(4);
                    } else {
                        addFloat("⚾ 안타 허용!", "#f87171"); screenShake = 10; advanceRun(1);
                    }
                    B = 0; S = 0; nextBatter();
                } else {
                    addFloat("헛스윙 스트라이크!", "#34d399"); S++;
                }
            } else {
                // 지켜봄 (루킹)
                if (isStrike) { addFloat("루킹 스트라이크!", "#60a5fa"); S++; } 
                else { addFloat("볼!", "#fbbf24"); B++; }
            }

            // 아웃카운트 및 볼넷 규칙 처리
            if (S >= 3) { addFloat("삼진 아웃!!", "#34d399"); O++; B = 0; S = 0; nextBatter(); }
            if (B >= 4) { addFloat("볼넷 허용", "#f59e0b"); advanceRun(1, true); B = 0; S = 0; nextBatter(); }
            
            if (O >= 3) {
                inning++; O = 0; B = 0; S = 0; bases = [false, false, false];
                addFloat("이닝 종료! 공수 교대", "#fbbf24");
            }
            
            setTimeout(() => {
                state = "PLAYING"; isSwinging = false;
                msgDiv.style.display = "block"; updateUI();
            }, 1500);
        }

        function advanceRun(amt, isWalk=false) {
            let runs = 0;
            if(isWalk) {
                if(bases[0] && bases[1] && bases[2]) runs = 1;
                else if(bases[0] && bases[1]) bases[2] = true;
                else if(bases[0]) bases[1] = true;
                bases[0] = true;
            } else {
                for(let i=0; i<amt; i++) {
                    if(bases[2]) runs++; bases[2] = bases[1]; bases[1] = bases[0]; bases[0] = (i === 0);
                }
            }
            scAway += runs; // 상대팀 득점 처리
        }

        // --- 캔버스 그래픽 드로잉 함수 ---
        function drawScene() {
            // 구장 그라데이션 배경
            let sky = ctx.createLinearGradient(0,0,0,150);
            sky.addColorStop(0, "#090d16"); sky.addColorStop(1, "#1e1b4b");
            ctx.fillStyle = sky; ctx.fillRect(0,0,800,150);

            let ground = ctx.createLinearGradient(0,150,0,460);
            ground.addColorStop(0, "#115e59"); ground.addColorStop(1, "#065f46");
            ctx.fillStyle = ground; ctx.fillRect(0,150,800,310);

            // 흙 및 라인 렌더링
            ctx.fillStyle = "#7c2d12"; ctx.beginPath();
            ctx.moveTo(400, 150); ctx.lineTo(670, 280); ctx.lineTo(400, 440); ctx.lineTo(130, 280); ctx.fill();

            ctx.fillStyle = "#0f766e"; ctx.beginPath();
            ctx.moveTo(400, 200); ctx.lineTo(550, 280); ctx.lineTo(400, 360); ctx.lineTo(250, 280); ctx.fill();

            // 주자 상황 미니맵 미러링
            ctx.fillStyle = "#0f172a"; ctx.fillRect(25, 355, 75, 75);
            const drawBase = (bx, by, active) => {
                ctx.fillStyle = active ? "#ef4444" : "#475569";
                ctx.save(); ctx.translate(bx, by); ctx.rotate(Math.PI/4); ctx.fillRect(-6, -6, 12, 12); ctx.restore();
            };
            drawBase(75, 392, bases[0]); drawBase(62, 370, bases[1]); drawBase(49, 392, bases[2]);
        }

        function drawFielders() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            const f = (x, y, s) => {
                ctx.beginPath(); ctx.ellipse(x, y+12*s, 8*s, 3*s, 0, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#cbd5e1"; ctx.fillRect(x-3*s, y, 6*s, 12*s);
                ctx.beginPath(); ctx.arc(x, y-2*s, 3*s, 0, Math.PI*2); ctx.fill();
            };
            f(200, 130, 0.5); f(400, 115, 0.45); f(600, 130, 0.5); // 외야
            f(310, 180, 0.65); f(490, 180, 0.65); f(560, 230, 0.75); f(240, 230, 0.75); // 내야
        }

        function drawInteractiveZone() {
            // 스트라이크존 박스
            ctx.strokeStyle = "rgba(251, 191, 36, 0.85)"; ctx.lineWidth = 3;
            ctx.strokeRect(zone.x, zone.y, zone.w, zone.h);
            
            ctx.strokeStyle = "rgba(251, 191, 36, 0.2)"; ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(zone.x + zone.w/3, zone.y); ctx.lineTo(zone.x + zone.w/3, zone.y + zone.h);
            ctx.moveTo(zone.x + zone.w*2/3, zone.y); ctx.lineTo(zone.x + zone.w*2/3, zone.y + zone.h);
            ctx.moveTo(zone.x, zone.y + zone.h/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h/3);
            ctx.moveTo(zone.x, zone.y + zone.h*2/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h*2/3);
            ctx.stroke();

            // 실시간 투구 조준 마커 (플레이 모드일 때만 표시)
            if (state === "PLAYING") {
                ctx.strokeStyle = "#22d3ee"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(aimX, aimY, 8, 0, Math.PI*2); ctx.stroke();
                ctx.fillStyle = "rgba(34, 211, 238, 0.3)"; ctx.fill();
            }
        }

        function drawBatterAndPitcher() {
            // 투수 모션 위치
            ctx.fillStyle = "#e2e8f0"; ctx.fillRect(396, 240, 8, 25);
            ctx.beginPath(); ctx.arc(400, 235, 5, 0, Math.PI*2); ctx.fill();

            // AI 타자 실루엣
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(275, 290, 25, 95);
            ctx.beginPath(); ctx.arc(287, 275, 12, 0, Math.PI*2); ctx.fill();

            ctx.save(); ctx.translate(300, 310);
            if (isSwinging) {
                swingAngle += 24; ctx.rotate(swingAngle * Math.PI / 180);
                ctx.fillStyle = "#92400e"; ctx.fillRect(0, -6, 75, 12);
            } else {
                ctx.rotate(-45 * Math.PI / 180); ctx.fillStyle = "#92400e"; ctx.fillRect(0, -5, 65, 10);
            }
            ctx.restore();
        }

        function gameLoop() {
            ctx.save();
            if (screenShake > 0) {
                ctx.translate((Math.random()-0.5)*screenShake, (Math.random()-0.5)*screenShake);
                screenShake--;
            }

            ctx.clearRect(0,0,800,460);
            drawScene();
            drawFielders();
            drawInteractiveZone();
            drawBatterAndPitcher();

            // 물리 투구 엔진
            if (ball.active) {
                ball.z -= ball.speedZ;
                let scale = 1 - (ball.z / 100);
                
                // 구종 타입에 따른 X축 휨 현상 추가 (변화구 연출)
                let typeStr = tSelect.value;
                let curveX = (typeStr !== "포심 직구") ? Math.sin(scale * Math.PI) * 40 : 0;

                let curX = 400 + (aimX - 400) * scale + curveX;
                let curY = 240 + (aimY - 240) * scale;
                let curRad = 3 + (12 * scale);

                ctx.beginPath(); ctx.arc(curX, curY, curRad, 0, Math.PI*2);
                ctx.fillStyle = "#fff"; ctx.fill();
                ctx.strokeStyle = "#475569"; ctx.stroke();

                if (ball.z <= 0) evaluateAIHit();
            }

            // 결과 메시지 루프
            for(let i=floatingTexts.length-1; i>=0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 36px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                ctx.lineWidth = 5; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 400, ft.y);
                ctx.fillText(ft.t, 400, ft.y);
                ft.y -= 1.5; ft.a -= 0.02; ctx.globalAlpha = 1.0;
                if (ft.a <= 0) floatingTexts.splice(i, 1);
            }

            ctx.restore();
            requestAnimationFrame(gameLoop);
        }

        changePitcher();
        nextBatter();
        gameLoop();
        updateUI();
    </script>
</body>
</html>
"""

components.html(pitcher_sim_html, height=490, width=830, scrolling=False)
