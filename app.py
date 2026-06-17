import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Real Pro Baseball", layout="centered")
st.title("⚾ KBO 모바일 프로야구 (Realism Ver.)")

real_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Real Pro Baseball</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center;
            background-color: #0b0f19; color: #fff; font-family: 'Noto Sans KR', sans-serif; height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 440px; height: 650px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8); border-radius: 16px; overflow: hidden; border: 2px solid #334155;
        }
        #gameCanvas { background: #1e3a8a; display: block; }
        
        /* UI Style */
        #topScoreBoard {
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15); border-radius: 12px;
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 15px; box-sizing: border-box; z-index: 10;
        }
        .board-col { display: flex; flex-direction: column; align-items: center; }
        .inning-text { font-size: 15px; font-weight: 900; color: #fbbf24; }
        .score-text { font-size: 24px; font-weight: 900; letter-spacing: 2px; }
        .bso-board { display: flex; flex-direction: column; gap: 2px; font-weight: 700; font-size: 14px; margin-top:4px;}
        .bso-row { display: flex; align-items: center; gap: 4px; }
        .bso-circle { width: 10px; height: 10px; border-radius: 50%; background: #334155; border: 1px solid #1e293b; }
        .b-active { background: #34d399; box-shadow: 0 0 5px #34d399; }
        .s-active { background: #fbbf24; box-shadow: 0 0 5px #fbbf24; }
        .o-active { background: #ef4444; box-shadow: 0 0 5px #ef4444; }
        
        #msgOverlay {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 24px; font-weight: 900; color: #fff;
            text-shadow: 0px 4px 10px rgba(0,0,0,0.8); pointer-events: none; z-index: 15; width: 100%;
        }
        
        #bottomControls {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            width: 90%; display: flex; gap: 10px; justify-content: center; z-index: 10;
        }
        .action-btn {
            background: linear-gradient(to bottom, #3b82f6, #1d4ed8); color: white;
            border: 1px solid #60a5fa; padding: 15px 0; border-radius: 12px; font-weight: 900; font-size: 18px;
            cursor: pointer; flex: 1; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .action-btn:active { transform: scale(0.97); }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="topScoreBoard">
            <div class="board-col" style="width: 30%;">
                <div style="font-size:12px; color:#94a3b8">AWAY</div>
                <div class="score-text" id="scAway" style="color:#cbd5e1">0</div>
            </div>
            <div class="board-col" style="width: 40%;">
                <div class="inning-text" id="uiInning">1회초</div>
                <div class="bso-board">
                    <div class="bso-row"><span style="color:#34d399; width:15px">B</span>
                        <div class="bso-circle" id="b1"></div><div class="bso-circle" id="b2"></div><div class="bso-circle" id="b3"></div>
                    </div>
                    <div class="bso-row"><span style="color:#fbbf24; width:15px">S</span>
                        <div class="bso-circle" id="s1"></div><div class="bso-circle" id="s2"></div>
                    </div>
                    <div class="bso-row"><span style="color:#ef4444; width:15px">O</span>
                        <div class="bso-circle" id="o1"></div><div class="bso-circle" id="o2"></div>
                    </div>
                </div>
            </div>
            <div class="board-col" style="width: 30%;">
                <div style="font-size:12px; color:#94a3b8">HOME</div>
                <div class="score-text" id="scHome" style="color:#60a5fa">0</div>
            </div>
        </div>

        <div id="msgOverlay">터치하여 경기 시작</div>
        <canvas id="gameCanvas" width="440" height="650"></canvas>
        <div id="bottomControls">
            <button class="action-btn" id="mainBtn">경기 시작</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");
        const mainBtn = document.getElementById("mainBtn");

        // 게임 상태
        let state = "READY"; // READY, PITCHING, FLYING, HIT_RESULT
        let inning = 1; let isTop = true;
        let scAway = 0; let scHome = 0;
        let B = 0, S = 0, O = 0;
        let bases = [false, false, false];
        let floatingTexts = [];

        // 3D 투구 변수
        let ball = { z: 100, x: 220, y: 240, targetX: 220, targetY: 380, speed: 1.5, active: false };
        let isSwinging = false; let swingTimer = 0;

        // 스트라이크 존 정의 (x: 170~270, y: 320~450)
        const zone = { x: 170, y: 320, w: 100, h: 130 };

        mainBtn.onclick = () => {
            if (state === "READY") { startHalf(); }
            else if (state === "IDLE") { doPitch(); }
            else if (state === "PITCHING") { doSwing(); }
        };

        document.addEventListener("keydown", (e) => {
            if(e.code === "Space") mainBtn.click();
        });

        function startHalf() {
            state = "IDLE"; B = 0; S = 0; O = 0; bases = [false, false, false];
            updateUI(); mainBtn.innerText = "투구 기다리기"; msgDiv.style.display = "none";
        }

        function updateUI() {
            document.getElementById("uiInning").innerText = `${inning}회${isTop ? '초' : '말'}`;
            document.getElementById("scAway").innerText = scAway; document.getElementById("scHome").innerText = scHome;
            
            // BSO 램프 업데이트
            for(let i=1; i<=3; i++) document.getElementById("b"+i).className = `bso-circle ${B>=i ? 'b-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("s"+i).className = `bso-circle ${S>=i ? 's-active':''}`;
            for(let i=1; i<=2; i++) document.getElementById("o"+i).className = `bso-circle ${O>=i ? 'o-active':''}`;
        }

        function doPitch() {
            state = "PITCHING";
            ball.z = 100; ball.active = true;
            
            // 타겟 설정 (존 안팎으로 랜덤)
            ball.targetX = 140 + Math.random() * 160; 
            ball.targetY = 280 + Math.random() * 210;
            
            mainBtn.innerText = "💥 SWING!";
            msgDiv.style.display = "none";
        }

        function doSwing() {
            if(isSwinging) return;
            isSwinging = true; swingTimer = 20; mainBtn.innerText = "...";
            
            // z값이 15~0 사이일 때 타격 가능 (타이밍)
            if (ball.z < 25 && ball.z > -5) {
                // 배트 닿는 범위(X, Y) 판정
                let hitDist = Math.hypot(ball.targetX - 220, ball.targetY - 380);
                if (hitDist < 70) {
                    processHit(ball.z); return;
                }
            }
            // 헛스윙
            processMiss(true);
        }

        function processMiss(swung) {
            state = "HIT_RESULT"; ball.active = false;
            
            if (swung) {
                addFloat("헛스윙!", "#ef4444"); addStrike();
            } else {
                // 스트라이크 존 통과 여부 판정
                let isStrike = (ball.targetX >= zone.x && ball.targetX <= zone.x + zone.w && 
                                ball.targetY >= zone.y && ball.targetY <= zone.y + zone.h);
                if (isStrike) {
                    addFloat("스트라이크!", "#f87171"); addStrike();
                } else {
                    addFloat("볼!", "#34d399"); addBall();
                }
            }
            setTimeout(resetPitch, 1500);
        }

        function processHit(z) {
            state = "HIT_RESULT"; ball.active = false;
            // 타이밍에 따른 결과 (z가 5~10에 가까울수록 홈런)
            if (z > 5 && z < 15 && Math.random() > 0.4) {
                addFloat("💥 HOMERUN!", "#fbbf24"); advanceRun(4);
            } else {
                addFloat("⚾ 안타!", "#60a5fa"); advanceRun(1);
            }
            B = 0; S = 0; updateUI();
            setTimeout(resetPitch, 1500);
        }

        function addStrike() {
            S++; if(S >= 3) { addFloat("삼진 아웃!", "#ef4444"); addOut(); B=0; S=0; } updateUI();
        }
        function addBall() {
            B++; if(B >= 4) { addFloat("볼넷 (출루)", "#60a5fa"); advanceRun(1, true); B=0; S=0; } updateUI();
        }
        function addOut() {
            O++; if(O >= 3) {
                if(isTop) { isTop = false; } else { isTop = true; inning++; }
                if(inning > 9) { state = "END"; msgDiv.innerText = "경기 종료!"; msgDiv.style.display="block"; return; }
                state = "READY"; msgDiv.innerHTML = "공수교대<br><span style='font-size:16px'>터치하여 시작</span>"; msgDiv.style.display="block";
                mainBtn.innerText = "이닝 시작"; B=0;S=0;O=0;bases=[false,false,false]; updateUI();
                return;
            }
        }
        function advanceRun(amt, isWalk=false) {
            let r = 0;
            if(isWalk) { // 볼넷 밀어내기 로직
                if(bases[0] && bases[1] && bases[2]) r = 1;
                else if(bases[0] && bases[1]) bases[2] = true;
                else if(bases[0]) bases[1] = true;
                bases[0] = true;
            } else {
                for(let i=0; i<amt; i++){ if(bases[2]) r++; bases[2]=bases[1]; bases[1]=bases[0]; bases[0]=(i===0); }
            }
            if(isTop) scAway += r; else scHome += r;
        }

        function resetPitch() {
            if(state === "END" || state === "READY") return;
            state = "IDLE"; mainBtn.innerText = "투구 기다리기";
        }

        function addFloat(txt, color) {
            floatingTexts.push({ t: txt, c: color, y: 300, alpha: 1.0 });
        }

        // --- 렌더링 엔진 ---
        function drawField() {
            // 그라운드 & 하늘
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0,0,440,250); // 밤하늘
            let grad = ctx.createLinearGradient(0,250,0,650);
            grad.addColorStop(0, "#064e3b"); grad.addColorStop(1, "#166534");
            ctx.fillStyle = grad; ctx.fillRect(0,250,440,400);

            // 마운드 (투수석)
            ctx.fillStyle = "#78350f"; ctx.beginPath(); ctx.ellipse(220, 240, 50, 10, 0, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(210, 238, 20, 4); // 투수판

            // 홈 플레이트 흙 영역
            ctx.fillStyle = "#78350f"; ctx.beginPath(); ctx.ellipse(220, 580, 160, 50, 0, 0, Math.PI*2); ctx.fill();
            
            // 홈 플레이트 (백뷰 원근감)
            ctx.fillStyle = "#fff"; ctx.beginPath();
            ctx.moveTo(200, 560); ctx.lineTo(240, 560); ctx.lineTo(250, 575); ctx.lineTo(220, 595); ctx.lineTo(190, 575); ctx.fill();

            // 베이스 주자 표시 (미니맵 스타일)
            ctx.fillStyle = bases[1] ? "#fbbf24" : "#475569"; ctx.fillRect(360, 500, 15, 15); // 2B (우측 상단)
            ctx.fillStyle = bases[0] ? "#fbbf24" : "#475569"; ctx.fillRect(400, 540, 15, 15); // 1B
            ctx.fillStyle = bases[2] ? "#fbbf24" : "#475569"; ctx.fillRect(320, 540, 15, 15); // 3B
        }

        function drawStrikeZone() {
            // 외곽선
            ctx.strokeStyle = "rgba(251, 191, 36, 0.8)"; ctx.lineWidth = 3;
            ctx.strokeRect(zone.x, zone.y, zone.w, zone.h);
            // 9분할 그리드
            ctx.strokeStyle = "rgba(251, 191, 36, 0.3)"; ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(zone.x + zone.w/3, zone.y); ctx.lineTo(zone.x + zone.w/3, zone.y + zone.h);
            ctx.moveTo(zone.x + zone.w*2/3, zone.y); ctx.lineTo(zone.x + zone.w*2/3, zone.y + zone.h);
            ctx.moveTo(zone.x, zone.y + zone.h/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h/3);
            ctx.moveTo(zone.x, zone.y + zone.h*2/3); ctx.lineTo(zone.x + zone.w, zone.y + zone.h*2/3);
            ctx.stroke();
        }

        function drawPlayers() {
            // 투수 (멀리 있음)
            ctx.fillStyle = "#94a3b8"; ctx.fillRect(215, 200, 10, 30);
            ctx.beginPath(); ctx.arc(220, 195, 6, 0, Math.PI*2); ctx.fill();
            
            // 타자 (우타자 기준 화면 왼쪽, 가까움)
            ctx.fillStyle = "#cbd5e1"; ctx.fillRect(110, 350, 40, 120);
            ctx.beginPath(); ctx.arc(130, 330, 20, 0, Math.PI*2); ctx.fill(); // 헬멧
            
            // 배트 스윙 연출
            ctx.save(); ctx.translate(140, 420);
            if(isSwinging) {
                ctx.rotate(Math.PI / 4); ctx.fillStyle = "#d97706"; ctx.fillRect(0, -100, 12, 100);
                swingTimer--; if(swingTimer <= 0) isSwinging = false;
            } else {
                ctx.rotate(-Math.PI / 6); ctx.fillStyle = "#d97706"; ctx.fillRect(0, -90, 10, 90);
            }
            ctx.restore();
        }

        function gameLoop() {
            ctx.clearRect(0,0,440,650);
            drawField();
            drawPlayers();
            drawStrikeZone();

            // 공 렌더링 (3D 원근감 계산)
            if (ball.active) {
                ball.z -= ball.speed;
                let scale = 1 - (ball.z / 100); // 0 (멀다) -> 1 (가깝다)
                let curX = 220 + (ball.targetX - 220) * scale;
                let curY = 240 + (ball.targetY - 240) * scale;
                let curRadius = 2 + (12 * scale); // 다가올수록 커짐

                ctx.beginPath(); ctx.arc(curX, curY, curRadius, 0, Math.PI*2);
                ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = "#94a3b8"; ctx.stroke();

                // 투구 완료 판정
                if (ball.z <= 0) {
                    if (state === "PITCHING") processMiss(false); // 타격 안 했을 때 판정
                }
            }

            // 플로팅 텍스트
            for(let i=floatingTexts.length-1; i>=0; i--) {
                let ft = floatingTexts[i];
                ctx.font = "italic 900 40px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.alpha;
                ctx.lineWidth = 5; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 220, ft.y);
                ctx.fillText(ft.t, 220, ft.y);
                ft.y -= 2; ft.alpha -= 0.03; ctx.globalAlpha = 1.0;
                if(ft.alpha <= 0) floatingTexts.splice(i, 1);
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
        updateUI();
    </script>
</body>
</html>
"""

components.html(real_baseball_html, height=660, scrolling=False)
