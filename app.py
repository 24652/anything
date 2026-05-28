import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Extreme Brick Breaker", layout="wide")

# 제목
st.title("🧱 익스트림 벽돌 깨기: 보스 레이드 & 레이저 에디션")

# 게임 로직 HTML/JS
brick_breaker_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Boss & Laser Brick Breaker</title>
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
            font-family: 'Courier New', Courier, monospace;
            height: 100vh;
            overflow: hidden;
        }
        #gameContainer { position: relative; }
        #gameCanvas {
            border: 5px solid #4a90e2;
            background-color: #05070a;
            box-shadow: 0 0 35px rgba(74, 144, 226, 0.4);
            border-radius: 10px;
        }
        #gameUi {
            display: flex;
            justify-content: space-between;
            width: 800px;
            margin-bottom: 10px;
            font-size: 22px;
            font-weight: bold;
        }
        .stat-val { color: #00ffcc; }
        #msg {
            position: absolute;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-size: 26px;
            color: #fff;
            text-shadow: 2px 2px #000;
            pointer-events: none;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="gameUi">
            <div>STAGE: <span id="stage" class="stat-val">1</span></div>
            <div>SCORE: <span id="score" class="stat-val">0</span></div>
            <div>LIVES: <span id="lives" class="stat-val">3</span></div>
        </div>
        <canvas id="gameCanvas" width="800" height="550"></canvas>
        <div id="msg">방향키(← →)를 눌러 시작하세요!<br>[보라 아이템 획득 시 스페이스바 키로 레이저 발사!]</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreSpan = document.getElementById("score");
        const livesSpan = document.getElementById("lives");
        const stageSpan = document.getElementById("stage");
        const msgDiv = document.getElementById("msg");

        // 설정
        const ballRadius = 8;
        const paddleHeight = 15;
        const paddleWidth = 110;
        const brickWidth = 75;
        const brickHeight = 22;
        const brickPadding = 10;
        const brickOffsetTop = 60;
        const brickOffsetLeft = 20;

        // 게임 상태
        let score = 0;
        let lives = 3;
        let stage = 1;
        let balls = [];
        let paddleX = (canvas.width - paddleWidth) / 2;
        let bricks = [];
        let items = [];
        let lasers = [];
        let particles = [];
        let rightPressed = false;
        let leftPressed = false;
        let gameActive = false;
        let baseSpeed = 4.5;
        let laserTimer = 0; // 레이저 지속 시간

        // 벽돌 초기화 (강철 블록 + 보스 블록 포함)
        function initBricks() {
            bricks = [];
            const rows = 4;
            const cols = 9;
            const unbreakableCount = Math.min(stage - 1, 4); 

            for (let c = 0; c < cols; c++) {
                bricks[c] = [];
                for (let r = 0; r < rows; r++) {
                    // 중앙 부근에 보스 배치 (c:4, r:1)
                    if (c === 4 && r === 1) {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'boss', hp: 5 + stage, maxHp: 5 + stage };
                    } else {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'normal' };
                    }
                }
            }

            // 강철 블록 무작위 배치
            if (stage > 1) {
                let placed = 0;
                while (placed < unbreakableCount) {
                    let rc = Math.floor(Math.random() * cols);
                    let rr = Math.floor(Math.random() * rows);
                    if (bricks[rc][rr].type === 'normal') {
                        bricks[rc][rr].type = 'unbreakable';
                        placed++;
                    }
                }
            }
        }

        function createBall() {
            return {
                x: paddleX + paddleWidth / 2,
                y: canvas.height - 40,
                dx: baseSpeed * (Math.random() > 0.5 ? 1 : -1) * 0.7,
                dy: -baseSpeed,
                active: true
            };
        }

        // 파티클 생성
        function createParticles(x, y, color) {
            for (let i = 0; i < 8; i++) {
                particles.push({
                    x: x, y: y,
                    dx: (Math.random() - 0.5) * 4,
                    dy: (Math.random() - 0.5) * 4,
                    alpha: 1,
                    color: color
                });
            }
        }

        initBricks();

        // 키 이벤트
        document.addEventListener("keydown", (e) => {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
            
            if (e.key == " " && laserTimer > 0 && gameActive) { // 스페이스바 레이저 발사
                lasers.push({ x: paddleX + 15, y: canvas.height - 30 });
                lasers.push({ x: paddleX + paddleWidth - 15, y: canvas.height - 30 });
            }

            if (!gameActive && lives > 0) {
                gameActive = true;
                msgDiv.style.display = "none";
                if (balls.length === 0) balls.push(createBall());
            }
        });

        document.addEventListener("keyup", (e) => {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 1. 벽돌 그리기 및 체크
            let activeNormalBricks = 0;
            for (let c = 0; c < bricks.length; c++) {
                for (let r = 0; r < bricks[c].length; r++) {
                    let b = bricks[c][r];
                    if (b.status == 1) {
                        if (b.type !== 'unbreakable') activeNormalBricks++;
                        
                        let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        b.x = brickX;
                        b.y = brickY;
                        
                        ctx.beginPath();
                        ctx.rect(brickX, brickY, brickWidth, brickHeight);
                        
                        if (b.type === 'unbreakable') {
                            ctx.fillStyle = '#666';
                        } else if (b.type === 'boss') {
                            ctx.fillStyle = `rgb(${255 - (b.hp * 20)}, 0, 100)`; // 체력 깎일수록 밝아짐
                        } else {
                            ctx.fillStyle = `hsl(${stage * 35 + r * 25}, 70%, 50%)`;
                        }
                        
                        ctx.fill();
                        ctx.strokeStyle = "#000";
                        ctx.stroke();
                        ctx.closePath();

                        // 보스 체력 바 표시
                        if (b.type === 'boss') {
                            ctx.fillStyle = "#fff";
                            ctx.font = "12px sans-serif";
                            ctx.fillText(`👑HP:${b.hp}`, brickX + 15, brickY + 15);
                        }
                    }
                }
            }

            // 스테이지 클리어
            if (activeNormalBricks === 0 && gameActive) {
                stage++;
                stageSpan.innerText = stage;
                baseSpeed += 0.4;
                gameActive = false;
                balls = []; items = []; lasers = []; laserTimer = 0;
                initBricks();
                msgDiv.innerHTML = `🎉 STAGE ${stage} CLEAR! 🎉<br>더 강력한 보스가 나타납니다!`;
                msgDiv.style.display = "block";
            }

            // 2. 패들 그리기 (레이저 상태면 색상 변경)
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
            ctx.fillStyle = laserTimer > 0 ? "#b000ff" : "#0095DD";
            ctx.fill();
            ctx.closePath();

            if (laserTimer > 0) {
                laserTimer--;
                ctx.fillStyle = "#b000ff";
                ctx.font = "12px sans-serif";
                ctx.fillText(`LASER: ${Math.ceil(laserTimer/60)}s`, paddleX + 20, canvas.height - 30);
            }

            // 3. 레이저 이동 및 충돌
            for (let l = 0; l < lasers.length; l++) {
                let laz = lasers[l];
                laz.y -= 6;
                ctx.fillStyle = "#ff00ff";
                ctx.fillRect(laz.x, laz.y, 4, 12);

                // 레이저가 벽돌 맞췄을 때
                let lazHit = false;
                for (let c = 0; c < bricks.length; c++) {
                    for (let r = 0; r < bricks[c].length; r++) {
                        let br = bricks[c][r];
                        if (br.status == 1 && laz.x > br.x && laz.x < br.x + brickWidth && laz.y > br.y && laz.y < br.y + brickHeight) {
                            lazHit = true;
                            if (br.type === 'normal') {
                                br.status = 0; score += 10; scoreSpan.innerText = score;
                                createParticles(br.x + brickWidth/2, br.y + brickHeight/2, "#ff00ff");
                            } else if (br.type === 'boss') {
                                br.hp--;
                                createParticles(br.x + brickWidth/2, br.y + brickHeight/2, "#ff0000");
                                if (br.hp <= 0) { br.status = 0; score += 100; scoreSpan.innerText = score; }
                            }
                            break;
                        }
                    }
                    if (lazHit) break;
                }
                if (lazHit || laz.y < 0) { lasers.splice(l, 1); l--; }
            }

            // 4. 아이템 관리 (3종 종류별 다른 색상)
            for (let i = 0; i < items.length; i++) {
                let it = items[i];
                it.y += 2.5;
                ctx.beginPath();
                ctx.arc(it.x, it.y, 10, 0, Math.PI * 2);
                ctx.fillStyle = it.type === 'BALL' ? "#00ff00" : (it.type === 'LASER' ? "#b000ff" : "#ff3333");
                ctx.fill();
                ctx.fillStyle = "#fff";
                ctx.font = "10px sans-serif";
                ctx.fillText(it.type === 'BALL' ? "⭐" : (it.type === 'LASER' ? "⚡" : "⏳"), it.x - 5, it.y + 4);
                ctx.closePath();

                // 획득 시
                if (it.y > canvas.height - paddleHeight - 15 && it.x > paddleX && it.x < paddleX + paddleWidth) {
                    if (it.type === 'BALL') balls.push(createBall());
                    else if (it.type === 'LASER') laserTimer = 400; // 약 7초간 레이저 모드
                    else if (it.type === 'SLOW') { balls.forEach(b => { b.dx *= 0.6; b.dy *= 0.6; }); } // 슬로우 기믹
                    items.splice(i, 1); i--;
                } else if (it.y > canvas.height) { items.splice(i, 1); i--; }
            }

            // 5. 파티클 이펙트 처리
            for (let p = 0; p < particles.length; p++) {
                let pt = particles[p];
                pt.x += pt.dx; pt.y += pt.dy; pt.alpha -= 0.02;
                if (pt.alpha <= 0) { particles.splice(p, 1); p--; continue; }
                ctx.save();
                ctx.globalAlpha = pt.alpha;
                ctx.fillStyle = pt.color;
                ctx.fillRect(pt.x, pt.y, 3, 3);
                ctx.restore();
            }

            // 6. 공 관리
            for (let i = 0; i < balls.length; i++) {
                let b = balls[i];
                ctx.beginPath();
                ctx.arc(b.x, b.y, ballRadius, 0, Math.PI * 2);
                ctx.fillStyle = i === 0 ? "#fff" : "#ffcc00";
                ctx.fill();
                ctx.closePath();

                if (gameActive) {
                    if (b.x + b.dx > canvas.width - ballRadius || b.x + b.dx < ballRadius) b.dx = -b.dx;
                    if (b.y + b.dy < ballRadius) b.dy = -b.dy;

                    // 패들 충돌
                    if (b.y + b.dy > canvas.height - paddleHeight - 10 - ballRadius) {
                        if (b.x > paddleX && b.x < paddleX + paddleWidth) {
                            let relX = (b.x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
                            b.dx = relX * baseSpeed; b.dy = -b.dy;
                        } else if (b.y + b.dy > canvas.height) {
                            balls.splice(i, 1); i--; continue;
                        }
                    }

                    // 벽돌 충돌
                    let breakFound = false;
                    for (let c = 0; c < bricks.length; c++) {
                        for (let r = 0; r < bricks[c].length; r++) {
                            let br = bricks[c][r];
                            if (br.status == 1) {
                                if (b.x > br.x && b.x < br.x + brickWidth && b.y > br.y && b.y < br.y + brickHeight) {
                                    b.dy = -b.dy;
                                    if (br.type === 'normal') {
                                        br.status = 0; score += 10; scoreSpan.innerText = score;
                                        createParticles(br.x + brickWidth/2, br.y + brickHeight/2, "#00ffcc");
                                        if (Math.random() < 0.20) {
                                            let types = ['BALL', 'LASER', 'SLOW'];
                                            items.push({ x: br.x + brickWidth / 2, y: br.y, type: types[Math.floor(Math.random()*types.length)] });
                                        }
                                    } else if (br.type === 'boss') {
                                        br.hp--;
                                        createParticles(br.x + brickWidth/2, br.y + brickHeight/2, "#ff0055");
                                        if (br.hp <= 0) {
                                            br.status = 0; score += 100; scoreSpan.innerText = score;
                                            // 보스 처치 시 무조건 아이템 대량 드롭
                                            items.push({ x: br.x + 20, y: br.y, type: 'BALL' });
                                            items.push({ x: br.x + 50, y: br.y, type: 'LASER' });
                                        }
                                    } else if (br.type === 'unbreakable') {
                                        createParticles(br.x + brickWidth/2, br.y + brickHeight/2, "#ffffff");
                                    }
                                    breakFound = true; break;
                                }
                            }
                        }
                        if (breakFound) break;
                    }
                    b.x += b.dx; b.y += b.dy;
                }
            }

            // 라이프 소진 체크
            if (balls.length === 0 && gameActive) {
                lives--; livesSpan.innerText = lives; gameActive = false; laserTimer = 0;
                if (lives <= 0) {
                    msgDiv.innerHTML = "💥 GAME OVER 💥<br>새로고침(F5)을 눌러 다시 도전하세요!";
                    msgDiv.style.display = "block";
                } else {
                    msgDiv.innerText = "공을 놓쳤습니다! 방향키를 누르면 다시 발사됩니다.";
                    msgDiv.style.display = "block";
                }
            }

            // 패들 이동
            if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 7.5;
            else if (leftPressed && paddleX > 0) paddleX -= 7.5;

            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

# 컴포넌트 렌더링
components.html(brick_breaker_html, height=650, scrolling=False)
