import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Pro Baseball - Grand Edition", layout="wide")
st.title("⚾ KBO 모바일 프로야구 (가로형 통합 그랜드 에디션)")

integrated_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Pro Baseball Grand Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center;
            background-color: #0b0f19; color: #fff; font-family: 'Noto Sans KR', sans-serif; height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 800px; height: 450px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8); border-radius: 16px; overflow: hidden; border: 2px solid #334155;
        }
        #gameCanvas { display: block; }
        
        /* Glassmorphism Scoreboard */
        #topScoreBoard {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15); border-radius: 12px;
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 20px; box-sizing: border-box; z-index: 10;
        }
        .board-col { display: flex; flex-direction: column; align-items: center; }
        .inning-text { font-size: 16px; font-weight: 900; color: #fbbf24; }
        .score-text { font-size: 26px; font-weight: 900; letter-spacing: 2px; }
        .bso-board { display: flex; gap: 15px; font-weight: 700; font-size: 14px; margin-top: 2px; }
        .bso-row { display: flex; align-items: center; gap: 4px; }
        .bso-circle { width: 12px; height: 12px; border-radius: 50%; background: #334155; border: 1px solid #1e293b; }
        .b-active { background: #34d399; box-shadow: 0 0 6px #34d399; }
        .s-active { background: #fbbf24; box-shadow: 0 0 6px #fbbf24; }
        .o-active { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
        
        #msgOverlay {
            position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 28px; font-weight: 900; color: #fff;
            text-shadow: 0px 4px 12px rgba(0,0,0,0.9); pointer-events: none; z-index: 15; width: 100%;
        }
        
        /* Side Controls Layout */
        #controlPanel {
            position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%);
            width: 90%; display: flex; gap: 12px; justify-content: center; z-index: 10;
        }
        .modern-btn {
            background: linear-gradient(to bottom, #3b82f6, #1d4ed8); color: white;
            border: 1px solid #60a5fa; padding: 10px 24px; border-radius: 8px; font-weight: 900; font-size: 15px;
            cursor: pointer; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.4); font-family: 'Noto Sans KR';
        }
        .modern-btn:active { transform: scale(0.96); }
        .btn-fast { background: linear-gradient(to bottom, #ef4444, #b91c1c); border-color: #f87171; }
        .btn-curve { background: linear-gradient(to bottom, #f59e0b, #b45309); border-color: #fbbf24; }
        .btn-action { background: linear-gradient(to bottom, #10b981, #047857); border-color: #34d399; width: 160px; }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="topScoreBoard">
            <div class="board-col" style="width: 25%; align-items: flex-start;">
                <div style="font-size:11px; color:#94a3b8; font-weight:700;">AWAY (원정)</div>
                <div class="score-text" id="scAway" style="color:#cbd5e1">0</div>
            </div>
            <div class="board-col" style="width: 50%;">
                <div class="inning-text" id="uiInning">1회초 공격</div>
                <div class="bso-board">
                    <div class="bso-row"><span style="color:#34d399; margin-right:2px;">B</span>
                        <div class="bso-circle" id="b1"></div><div class="bso-circle" id="b2"></div><div class="bso-circle" id="b3"></div>
                    </div>
                    <div class="bso-row"><span style="color:#fbbf24; margin-right:2px;">S</span>
                        <div class="bso-circle" id="s1"></div><div class="bso-circle" id="s2"></div>
                    </div>
                    <div class="bso-row"><span style="color:#ef4444; margin-right:2px;">O</span>
                        <div class="bso-circle" id="o1"></div><div class="bso-circle" id="o2"></div>
                    </div>
                </div>
            </div>
            <div class="board-col" style="width: 25%; align-items: flex-end;">
                <div style="font-size:11px; color:#94a3b8; font-weight:700;">HOME (홈)</div>
                <div class="score-text" id="scHome" style="color:#60a5fa">0</div>
            </div>
        </div>

        <div id="msgOverlay">구종을 선택하여 투구하세요!</div>
        <canvas id="gameCanvas" width="800" height="450"></canvas>
        
        <div id="controlPanel">
            <button class="modern-btn btn-fast" id="btnFast" onclick="pitch('fast')">⚡ 포심 직구</button>
            <button class="modern-btn btn-curve" id="btnCurve" onclick="pitch('curve')">🌪️ 커브 변화구</button>
            <button class="modern-btn btn-action" id="btnAction" onclick="handleAction()" style="display:none;"></button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");
        const btnFast = document.getElementById("btnFast");
        const btnCurve = document.getElementById("btnCurve");
        const btnAction = document.getElementById("btnAction");

        // 게임 핵심 상태 변수
        let state = "PLAYING"; // PLAYING, PITCHING, RESULT
        let inning = 1; let isTop = true;
        let scAway = 0; let scHome = 0;
        let B = 0, S = 0, O = 0;
        let bases = [false, false, false];
        let floatingTexts = [];
        let screenShake = 0;

        // 투구 및 타격 변수 (가로형 원근 좌표 세팅)
        let ball = { z: 100, x: 400, y: 170, targetX: 400, targetY: 310, speed: 2.0, active: false, type: 'fast' };
        let isSwinging = false; let swingAngle = 0;

        // 스트라이크 존 설정 (중앙 중심 원근 배치)
        const zone = { x: 350, y: 260, w: 100, h: 110 };

        function updateUI() {
            document.getElementById("uiInning").innerText = `${inning}회${isTop ? '초 공격' : '말 수비'}`;
            document.getElementById("uiInning").style.color = isTop ? "#60a5fa" : "#f87171";
            document.getElementById("scAway").innerText = scAway; 
            document.getElementById("scHome").innerText = scHome;
            
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `bso-circle ${B>=i ? 'b-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `bso-circle ${S>=i ? 's-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `bso-circle ${O>=i ? 'o-active':''}`;
        }

        // 1. 투구 함수 (유저 직접 발동)
        function pitch(type) {
            if (state !== "PLAYING") return;
            state = "PITCHING";
            msgDiv.style.display = "none";
            
            btnFast.style.display = "none";
            btnCurve.style.display = "none";
            btnAction.style.display = "block";
            btnAction.innerText = "💥 타격 (Space)";

            ball.z = 100; ball.active = true; ball.type = type;
            ball.speed = type === 'fast' ? 2.5 : 1.6;
            
            // 실제 존 경계 내부 및 아슬아슬한 외부로 무작위 타겟 지정
            ball.targetX = 310 + Math.random() * 180;
            ball.targetY = 220 + Math.random() * 170;

            // CPU 타자 자동 스윙 타이밍 예약 (수비 이닝일 경우를 위한 로직 구조화)
            if (!isTop) {
                let delay = type === 'fast' ? 450 : 700;
                setTimeout(() => { if(ball.active && Math.random() > 0.4) handleAction(); }, delay);
            }
        }

        // 2. 타격 버튼 또는 스페이스바 액션
        function handleAction() {
            if (state !== "PITCHING" || isSwinging) return;
            isSwinging = true; swingAngle = -60;

            // 적정 타이밍 존 (Z축이 홈플레이트 근처에 도달했을 때)
            if (ball.z < 20 && ball.z > -5) {
                let hitDist = Math.hypot(ball.targetX - 400, ball.targetY - 310);
                if (hitDist < 75) {
                    processHit(ball.z);
                    return;
                }
            }
            processMiss(true); // 타이밍을 맞추지 못함 -> 헛스윙
        }

        // 키보드 단축키 매핑
        document.addEventListener("keydown", (e) => {
            if (e.code === "Space" && state === "PITCHING") {
                e.preventDefault(); handleAction();
            }
        });

        function processMiss(swung) {
            state = "RESULT"; ball.active = false;
            if (swung) {
                addFloat("헛스윙!", "#ef4444"); addStrike();
            } else {
                let isStrike = (ball.targetX >= zone.x && ball.targetX <= zone.x + zone.w && 
                                ball.targetY >= zone.y && ball.targetY <= zone.y + zone.h);
                if (isStrike) { addFloat("스트라이크!", "#f87171"); addStrike(); } 
                else { addFloat("볼!", "#34d399"); addBall(); }
            }
            setTimeout(nextPitch, 1400);
        }

        function processHit(z) {
            state = "RESULT"; ball.active = false; screenShake = 18;
            if (z > 4 && z < 14 && Math.random() > 0.5) {
                addFloat("💥 HOMERUN! 💥", "#fbbf24"); advanceRun(4);
            } else {
                addFloat("⚾ 안타!", "#34d399"); advanceRun(1);
            }
            B = 0; S = 0; updateUI();
            setTimeout(nextPitch, 1400);
        }

        function addStrike() {
            S++; if(S >= 3) { addFloat("아웃! (삼진)", "#ef4444"); addOut(); B = 0; S = 0; } updateUI();
        }
        function addBall() {
            B++; if(B >= 4) { addFloat("볼넷 출루!", "#60a5fa"); advanceRun(1, true); B = 0; S = 0; } updateUI();
        }
        function addOut() {
            O++; if(O >= 3) {
                if(isTop) { isTop = false; } else { isTop = true; inning++; }
                if(inning > 9) {
                    state = "END"; msgDiv.innerHTML = `경기 종료!<br>최종 스코어 ${scAway} : ${scHome}`;
                    msgDiv.style.display = "block"; return;
                }
                addFloat("공수 교대!", "#fbbf24");
                B = 0; S = 0; O = 0; bases = [false, false, false];
            }
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
            if(isTop) scAway += runs; else scHome += runs;
        }

        function nextPitch() {
            if (state === "END") return;
            state = "PLAYING"; isSwinging = false;
            msgDiv.style.display = "block"; msgDiv.innerText = "구종을 선택하여 투구하세요!";
            btnFast.style.display = "inline-block"; btnCurve.style.display = "inline-block";
            btnAction.style.display = "none";
            updateUI();
        }

        function addFloat(txt, col) { floatingTexts.push({ t: txt, c: col, y: 220, a: 1.0 }); }

        // --- 고해상도 그래픽 엔진 (가로형 원근 수비 야수 배치) ---
        function drawField() {
            // 그라운드 및 원근 외야선 그라데이션
            let skyGrad = ctx.createLinearGradient(0,0,0,150);
            skyGrad.addColorStop(0, "#090d16"); skyGrad.addColorStop(1, "#1e1b4b");
            ctx.fillStyle = skyGrad; ctx.fillRect(0,0,800,150);

            let groundGrad = ctx.createLinearGradient(0,150,0,450);
            groundGrad.addColorStop(0, "#14532d"); groundGrad.addColorStop(1, "#166534");
            ctx.fillStyle = groundGrad; ctx.fillRect(0,150,800,300);

            // 야구장 흙 다이아몬드 커버 라인
            ctx.fillStyle = "#7c2d12"; ctx.beginPath();
            ctx.moveTo(400, 150); ctx.lineTo(650, 280); ctx.lineTo(400, 430); ctx.lineTo(150, 280); ctx.fill();

            // 내부 잔디 영역원형
            ctx.fillStyle = "#15803d"; ctx.beginPath();
            ctx.moveTo(400, 210); ctx.lineTo(540, 280); ctx.lineTo(400, 360); ctx.lineTo(260, 280); ctx.fill();

            // 홈 플레이트 본체 고정
            ctx.fillStyle = "#ffffff"; ctx.beginPath();
            ctx.moveTo(390, 410); ctx.lineTo(410, 410); ctx.lineTo(415, 420); ctx.lineTo(400, 432); ctx.lineTo(385, 420); ctx.fill();

            // 주자 상황 전광판 미니맵 (좌측 하단 콤팩트 배치)
            ctx.fillStyle = "#1e293b"; ctx.fillRect(25, 345, 80, 80);
            const drawBaseIndicator = (bx, by, active) => {
                ctx.fillStyle = active ? "#f59e0b" : "#475569";
                ctx.save(); ctx.translate(bx, by); ctx.rotate(Math.PI/4); ctx.fillRect(-7, -7, 14, 14); ctx.restore();
            };
            drawBaseIndicator(80, 385, bases[0]); // 1루
            drawBaseIndicator(65, 360, bases[1]); // 2루
            drawBaseIndicator(50, 385, bases[2]); // 3루
        }

        function drawFielders() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
            const drawSilhouette = (fx, fy, scale) => {
                // 그림자 효과
                ctx.beginPath(); ctx.ellipse(fx, fy + (16 * scale), 10 * scale, 3 * scale, 0, 0, Math.PI * 2); ctx.fill();
                // 유니폼 실루엣
                ctx.fillStyle = "#cbd5e1"; ctx.fillRect(fx - (4 * scale), fy, 8 * scale, 15 * scale);
                ctx.beginPath(); ctx.arc(fx, fy - (3 * scale), 4 * scale, 0, Math.PI * 2); ctx.fill();
            };

            // 외야수 배치 (좌익수, 중견수, 우익수 순)
            drawSilhouette(220, 135, 0.5); 
            drawSilhouette(400, 120, 0.45); 
            drawSilhouette(580, 135, 0.5);

            // 내야수 배치 (유격수, 2루수, 1루수, 3루수, 투수)
            drawSilhouette(320, 185, 0.65);
            drawSilhouette(480, 185, 0.65);
            drawSilhouette(550, 240, 0.75);
            drawSilhouette(250, 240, 0.75);
            drawSilhouette(400, 260, 0.8); // 투수 마운드 위
        }

        function drawStrikeZone() {
            // 메인 스트라이크 존 그리드
            ctx.strokeStyle = "rgba(251, 191, 36, 0.75)"; ctx.lineWidth = 3;
            ctx.strokeRect(zone.x, zone.y, zone.w, zone.h);
            
            ctx.strokeStyle = "rgba(251, 191, 36, 0.25)"; ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(zone.x + zone.w/3, zone.y); ctx.lineTo(zone.x + zone.w/3, zone.y + zone.h);
            ctx.moveTo(zone.x + zone.w*2/3, zone.y); ctx.lineTo(zone.x + zone.w*2/3, zone.y + zone.h);
            ctx.moveTo(zone.x, zone.y + zone.h/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h/3);
            ctx.moveTo(zone.x, zone.y + zone.h*2/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h*2/3);
            ctx.stroke();
        }

        function drawBatter() {
            // 타자 액션 실루엣 (원근감 구현을 위해 대형 크기로 우측/좌측 타석 배치)
            ctx.fillStyle = "#e2e8f0";
            ctx.fillRect(275, 290, 25, 95);
            ctx.beginPath(); ctx.arc(287, 275, 12, 0, Math.PI*2); ctx.fill();

            // 배트 회전 애니메이션 연출
            ctx.save(); ctx.translate(300, 310);
            if(isSwinging) {
                swingAngle += 22;
                ctx.rotate(swingAngle * Math.PI / 180);
                ctx.fillStyle = "#b45309"; ctx.fillRect(0, -6, 75, 12);
                if (swingAngle > 110) isSwinging = false;
            } else {
                ctx.rotate(-50 * Math.PI / 180);
                ctx.fillStyle = "#b45309"; ctx.fillRect(0, -5, 65, 10);
            }
            ctx.restore();
        }

        function gameLoop() {
            ctx.save();
            if (screenShake > 0) {
                ctx.translate((Math.random()-0.5)*screenShake, (Math.random()-0.5)*screenShake);
                screenShake--;
            }

            ctx.clearRect(0, 0, 800, 450);
            drawField();
            drawFielders();
            drawStrikeZone();
            drawBatter();

            // 3D 투구 궤적 및 줌 시각화
            if (ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100);
                
                // 변화구는 스핀 궤적(사인파) 적용
                let curveOffset = ball.type === 'curve' ? Math.sin(scale * Math.PI) * 45 : 0;
                let curX = 400 + (ball.targetX - 400) * scale + curveOffset;
                let curY = 260 + (ball.targetY - 260) * scale;
                let curRad = 2.5 + (13 * scale);

                // 공 본체 잔상 라인 효과
                ctx.beginPath(); ctx.arc(curX, curY, curRad, 0, Math.PI*2);
                ctx.fillStyle = "#ffffff"; ctx.fill();
                ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1.5; ctx.stroke();

                if (ball.z <= 0) processMiss(false);
            }

            // 스코어보드 결과 피드백 메시지 출력 루프
            for(let i=floatingTexts.length-1; i>=0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 36px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                ctx.lineWidth = 5; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 400, ft.y);
                ctx.fillText(ft.t, 400, ft.y);
                ft.y -= 1.5; ft.a -= 0.025; ctx.globalAlpha = 1.0;
                if (ft.a <= 0) floatingTexts.splice(i, 1);
            }

            ctx.restore();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
        updateUI();
    </script>
</body>
</html>
"""

components.html(integrated_baseball_html, height=480, width=820, scrolling=False)
