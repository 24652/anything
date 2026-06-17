import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Vertical Baseball Game", layout="centered")

# 타이틀
st.title("⚾ 세로형 원버튼 야구 게임 (홈런 더비)")

# 야구 게임 HTML/JS
baseball_game_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Vertical Baseball Game</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #0e1117;
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        #gameContainer { position: relative; }
        #gameCanvas {
            border: 4px solid #2ecc71;
            background-color: #1b3a24; /* 야구장 느낌의 녹색 톤 */
            box-shadow: 0 0 25px rgba(46, 204, 113, 0.4);
            border-radius: 12px;
        }
        #gameUi {
            display: flex;
            justify-content: space-between;
            width: 400px;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 700;
        }
        .stat-val { color: #00ffcc; }
        #msg {
            position: absolute;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-size: 18px;
            color: #fff;
            text-shadow: 1px 1px 4px #000;
            pointer-events: none;
            line-height: 1.6;
            width: 80%;
        }
        #adminUi {
            display: none;
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(255, 0, 127, 0.85);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            box-shadow: 0 0 10px rgba(255, 0, 127, 0.5);
            z-index: 10;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="adminUi">[ADMIN MODE] 대괄호 키로 조작 가능 ( [ : 이전 / ] : 다음 )</div>
        <div id="gameUi">
            <div>STAGE: <span id="stage" class="stat-val">1</span></div>
            <div>HOMERUNS: <span id="homeruns" class="stat-val">0</span>/<span id="target" class="stat-val">5</span></div>
            <div>OUTS: <span id="outs" class="stat-val">0</span>/3</div>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <div id="msg">스페이스바를 누르거나 화면을 터치하면<br>투수가 공을 던집니다!</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const homerunsSpan = document.getElementById("homeruns");
        const targetSpan = document.getElementById("target");
        const outsSpan = document.getElementById("outs");
        const stageSpan = document.getElementById("stage");
        const msgDiv = document.getElementById("msg");
        const adminUi = document.getElementById("adminUi");

        // 게임 변수
        let stage = 1;
        let homeruns = 0;
        let targetHomeruns = 5;
        let outs = 0;
        let gameActive = false;
        let gameOver = false;

        // 공 변수
        let ball = { x: 200, y: 150, radius: 8, dy: 0, dx: 0, active: false, type: 'normal' };
        let pitcherY = 150;
        let batterY = 500;
        let strikeZoneY = 500; // 타격 타이밍 중심선
        let strikeZoneHeight = 35; // 타격 가능 오차 범위

        // 배트 휘두르기 애니메이션 변수
        let batAngle = 0;
        let isSwinging = false;

        // 피드백 이펙트
        let feedbackText = "";
        let feedbackAlpha = 0;
        let ballHitAnimation = { x: 0, y: 0, active: false, timer: 0, dx: 0, dy: 0 };

        // 관리자 모드용
        let cheatBuffer = "";
        let isAdmin = false;

        function initStage() {
            homeruns = 0;
            targetHomeruns = 3 + stage * 2;
            outs = 0;
            ball.active = false;
            isSwinging = false;
            gameOver = false;
            
            homerunsSpan.innerText = homeruns;
            targetSpan.innerText = targetHomeruns;
            outsSpan.innerText = outs;
            stageSpan.innerText = stage;
        }

        function throwBall() {
            if (ball.active || gameOver) return;
            
            ball.x = 200;
            ball.y = pitcherY;
            ball.radius = 6;
            ball.active = true;
            
            // 스테이지별 구질 다양화
            let rand = Math.random();
            if (stage >= 3 && rand < 0.3) {
                ball.type = 'changeup'; // 날아오다가 느려지는 공
                ball.dy = 3.5;
            } else if (stage >= 2 && rand < 0.5) {
                ball.type = 'fast'; // 빠른 직구
                ball.dy = 6.5 + (stage * 0.3);
            } else {
                ball.type = 'normal';
                ball.dy = 4.5 + (stage * 0.2);
            }
            ball.dx = (Math.random() - 0.5) * 0.5; // 미세한 좌우 흔들림
            msgDiv.style.display = "none";
        }

        function swingBat() {
            if (isSwinging || gameOver) return;
            isSwinging = true;
            batAngle = -Math.PI / 4; // 휘두르기 시작 각도

            if (ball.active) {
                let distance = Math.abs(ball.y - strikeZoneY);
                
                if (distance <= strikeZoneHeight) {
                    // 타격 성공!
                    ball.active = false;
                    ballHitAnimation.x = ball.x;
                    ballHitAnimation.y = ball.y;
                    ballHitAnimation.active = true;
                    ballHitAnimation.timer = 40;
                    
                    // 홈런 및 안타 판정
                    if (distance <= 10) {
                        feedbackText = "🔥 HOMERUN!!! 🔥";
                        homeruns++;
                        homerunsSpan.innerText = homeruns;
                        ballHitAnimation.dx = (Math.random() - 0.5) * 2;
                        ballHitAnimation.dy = -12; // 하늘 높이 날아감
                    } else {
                        feedbackText = "⚾ HIT! ⚾";
                        ballHitAnimation.dx = (Math.random() > 0.5 ? 5 : -5);
                        ballHitAnimation.dy = -4; // 안타성 타구
                    }
                    feedbackAlpha = 1;

                    // 스테이지 클리어 검사
                    if (homeruns >= targetHomeruns) {
                        stage++;
                        setTimeout(() => {
                            initStage();
                            msgDiv.innerHTML = `🎉 STAGE CLEAR! 🎉<br>STAGE ${stage}가 시작됩니다. 스페이스바를 누르세요!`;
                            msgDiv.style.display = "block";
                        }, 1000);
                    } else {
                        setTimeout(() => { msgDiv.innerText = "다음 공 준비... (스페이스바)"; msgDiv.style.display = "block"; }, 1200);
                    }

                } else {
                    // 헛스윙 아웃
                    triggerOut("STRIKE / OUT!");
                }
            } else {
                // 공도 없는데 휘둘렀을 때
                feedbackText = "TOO EARLY!";
                feedbackAlpha = 1;
            }
        }

        function triggerOut(reason) {
            ball.active = false;
            outs++;
            outsSpan.innerText = outs;
            feedbackText = reason;
            feedbackAlpha = 1;

            if (outs >= 3) {
                gameOver = true;
                msgDiv.innerHTML = "💥 3 OUT! GAME OVER 💥<br>새로고침(F5)을 눌러 다시 시작하세요.";
                msgDiv.style.display = "block";
            } else {
                setTimeout(() => { msgDiv.innerText = "다음 공 준비... (스페이스바)"; msgDiv.style.display = "block"; }, 1200);
            }
        }

        function changeStage(direction) {
            if (direction === 'next') stage++;
            else if (direction === 'prev' && stage > 1) stage--;
            initStage();
            msgDiv.innerHTML = `⚙️ 관리자 권한 이동: STAGE ${stage}<br>스페이스바를 눌러 투구하세요!`;
            msgDiv.style.display = "block";
        }

        initStage();

        // 키 감지
        document.addEventListener("keydown", (e) => {
            let keyLower = e.key.toLowerCase();
            
            // 치트 입력 검사
            cheatBuffer += keyLower;
            if (cheatBuffer.endsWith("joonmin")) {
                isAdmin = !isAdmin;
                adminUi.style.display = isAdmin ? "block" : "none";
                cheatBuffer = "";
            }
            if (cheatBuffer.length > 20) cheatBuffer = cheatBuffer.substring(10);

            if (isAdmin) {
                if (e.key === "]") { changeStage('next'); return; }
                if (e.key === "[") { changeStage('prev'); return; }
            }

            if (e.key === " ") {
                e.preventDefault();
                if (!ball.active && !ballHitAnimation.active) {
                    throwBall();
                } else {
                    swingBat();
                }
            }
        });

        // 모바일/마우스 터치 대응
        canvas.addEventListener("mousedown", (e) => {
            e.preventDefault();
            if (!ball.active && !ballHitAnimation.active) {
                throwBall();
            } else {
                swingBat();
            }
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. 야구장 야외 필드 배경 시각화
            ctx.fillStyle = "#27ae60"; // 내야 잔디 색상
            ctx.beginPath();
            ctx.moveTo(200, 130);
            ctx.lineTo(400, 350);
            ctx.lineTo(200, 580);
            ctx.lineTo(0, 350);
            ctx.fill();

            // 투수 마운드 & 홈플레이트 베이스
            ctx.fillStyle = "#dbaf7d"; // 흙 색상
            ctx.beginPath(); ctx.arc(200, pitcherY, 20, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(200, batterY, 25, 0, Math.PI * 2); ctx.fill();

            // 2. 타격 타이밍 구역 (노란색 띠)
            ctx.fillStyle = "rgba(241, 196, 15, 0.3)";
            ctx.fillRect(0, strikeZoneY - strikeZoneHeight, canvas.width, strikeZoneHeight * 2);
            ctx.strokeStyle = "#f1c40f";
            ctx.strokeRect(0, strikeZoneY - strikeZoneHeight, canvas.width, strikeZoneHeight * 2);

            // 3. 투수 및 타자 그래픽 텍스트화
            ctx.font = "24px sans-serif";
            ctx.fillText("🧎", 188, pitcherY + 8); // 투수
            ctx.fillText("🧍", 160, batterY + 8); // 타자

            // 4. 배트 휘두르기 애니메이션 처리
            if (isSwinging) {
                batAngle += 0.25;
                if (batAngle > Math.PI / 2) {
                    isSwinging = false;
                }
                ctx.save();
                ctx.translate(175, batterY);
                ctx.rotate(batAngle);
                ctx.lineWidth = 6;
                ctx.strokeStyle = "#d35400"; // 나무 배트 색상
                ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(40, 0); ctx.stroke();
                ctx.restore();
            } else {
                // 대기 상태 배트
                ctx.save();
                ctx.translate(175, batterY);
                ctx.rotate(-Math.PI / 4);
                ctx.lineWidth = 6;
                ctx.strokeStyle = "#d35400";
                ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(40, 0); ctx.stroke();
                ctx.restore();
            }

            // 5. 날아오는 공 로직
            if (ball.active) {
                // 체인지업 구종일 때 타이밍 감속 기믹
                if (ball.type === 'changeup' && ball.y > 300 && ball.y < 380) {
                    ball.y += ball.dy * 0.4;
                } else {
                    ball.y += ball.dy;
                }
                ball.x += ball.dx;
                ball.radius += 0.08; // 다가올수록 공이 커지는 원근감 이펙트

                ctx.beginPath();
                ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
                ctx.fillStyle = "#ffffff";
                ctx.fill();
                ctx.strokeStyle = "#ff0000"; // 야구공 실밥 느낌 선
                ctx.stroke();
                ctx.closePath();

                // 배트로 치지 않고 포수 뒤로 완전히 빠졌을 때 (패스트볼/스트라이크)
                if (ball.y > canvas.height - 40) {
                    triggerOut("MISSED / STRIKE!");
                }
            }

            // 6. 타격 성공 후 날아가는 타구 이펙트
            if (ballHitAnimation.active) {
                ballHitAnimation.x += ballHitAnimation.dx;
                ballHitAnimation.y += ballHitAnimation.dy;
                ballHitAnimation.timer--;

                ctx.beginPath();
                ctx.arc(ballHitAnimation.x, ballHitAnimation.y, 5, 0, Math.PI * 2);
                ctx.fillStyle = "#ffff00";
                ctx.fill();
                ctx.closePath();

                if (ballHitAnimation.timer <= 0) ballHitAnimation.active = false;
            }

            // 7. 판정 텍스트 연출
            if (feedbackAlpha > 0) {
                ctx.font = "bold 26px sans-serif";
                ctx.fillStyle = feedbackText.includes("HOMERUN") ? "#e74c3c" : "#3498db";
                ctx.save();
                ctx.globalAlpha = feedbackAlpha;
                ctx.fillText(feedbackText, canvas.width / 2 - ctx.measureText(feedbackText).width / 2, 320);
                ctx.restore();
                feedbackAlpha -= 0.02;
            }

            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

components.html(baseball_game_html, height=670, scrolling=False)
