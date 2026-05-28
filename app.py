import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Extreme Brick Breaker", layout="wide")

# 제목만 남기고 하단 텍스트는 제거
st.title("🧱 익스트림 벽돌 깨기: 멀티볼 & 강철 스테이지")

# 게임 로직 HTML/JS
brick_breaker_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Ball Brick Breaker</title>
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
            border: 5px solid #333;
            background-color: #000;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
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
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-size: 28px;
            color: #fff;
            text-shadow: 2px 2px #000;
            pointer-events: none;
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
        <div id="msg">방향키(← →)를 눌러 시작하세요!</div>
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
        const brickOffsetTop = 50;
        const brickOffsetLeft = 20;

        // 게임 상태
        let score = 0;
        let lives = 3;
        let stage = 1;
        let balls = []; // 공 여러 개를 관리하는 배열
        let paddleX = (canvas.width - paddleWidth) / 2;
        let bricks = [];
        let items = [];
        let rightPressed = false;
        let leftPressed = false;
        let gameActive = false;
        let baseSpeed = 4;

        // 벽돌 초기화 (강철 블록 포함)
        function initBricks() {
            bricks = [];
            const rows = 3 + Math.min(stage, 5);
            const cols = 9;
            const unbreakableCount = (stage - 1) * 2; // 스테이지당 2개씩 증가

            // 일반 벽돌 먼저 채우기
            for (let c = 0; c < cols; c++) {
                bricks[c] = [];
                for (let r = 0; r < rows; r++) {
                    bricks[c][r] = { x: 0, y: 0, status: 1, type: 'normal' };
                }
            }

            // 강철 블록 무작위 배치 (2단계부터)
            if (stage > 1) {
                let placed = 0;
                while (placed < unbreakableCount) {
                    let rc = Math.floor(Math.random() * cols);
                    let rr = Math.floor(Math.random() * rows);
                    if (bricks[rc][rr].type === 'normal') {
                        bricks[rc][rr].type = 'unbreakable';
                        bricks[rc][rr].color = '#888a85'; // 금속색
                        placed++;
                    }
                }
            }
        }

        function createBall(isMain = false) {
            return {
                x: isMain ? paddleX + paddleWidth / 2 : paddleX + paddleWidth / 2,
                y: canvas.height - 40,
                dx: baseSpeed * (Math.random() > 0.5 ? 1 : -1),
                dy: -baseSpeed,
                active: true
            };
        }

        // 초기 실행
        initBricks();

        document.addEventListener("keydown", (e) => {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
            
            if (!gameActive && lives > 0) {
                gameActive = true;
                msgDiv.style.display = "none";
                if (balls.length === 0) balls.push(createBall(true));
            }
        });

        document.addEventListener("keyup", (e) => {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 벽돌 그리기
            let activeNormalBricks = 0;
            for (let c = 0; c < bricks.length; c++) {
                for (let r = 0; r < bricks[c].length; r++) {
                    let b = bricks[c][r];
                    if (b.status == 1) {
                        if (b.type === 'normal') activeNormalBricks++;
                        let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        b.x = brickX;
                        b.y = brickY;
                        ctx.beginPath();
                        ctx.rect(brickX, brickY, brickWidth, brickHeight);
                        ctx.fillStyle = b.type === 'unbreakable' ? '#888' : `hsl(${stage * 20 + r * 30}, 70%, 50%)`;
                        ctx.fill();
                        ctx.strokeStyle = "#000";
                        ctx.stroke();
                        ctx.closePath();
                    }
                }
            }

            // 스테이지 클리어 확인
            if (activeNormalBricks === 0 && gameActive) {
                stage++;
                stageSpan.innerText = stage;
                baseSpeed += 0.5;
                gameActive = false;
                balls = [];
                items = [];
                initBricks();
                msgDiv.innerText = "STAGE CLEAR! 다음 단계로..";
                msgDiv.style.display = "block";
            }

            // 패들 그리기
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
            ctx.fillStyle = "#0095DD";
            ctx.fill();
            ctx.closePath();

            // 아이템 관리
            for (let i = 0; i < items.length; i++) {
                let it = items[i];
                it.y += 3;
                ctx.beginPath();
                ctx.arc(it.x, it.y, 10, 0, Math.PI * 2);
                ctx.fillStyle = "#00ff00"; // 공 추가 아이템은 초록색
                ctx.fill();
                ctx.fillStyle = "#fff";
                ctx.fillText("⭐", it.x - 5, it.y + 4);
                ctx.closePath();

                if (it.y > canvas.height - paddleHeight - 15 && it.x > paddleX && it.x < paddleX + paddleWidth) {
                    balls.push(createBall()); // 공 추가!
                    items.splice(i, 1);
                    i--;
                } else if (it.y > canvas.height) {
                    items.splice(i, 1);
                    i--;
                }
            }

            // 공 관리
            for (let i = 0; i < balls.length; i++) {
                let b = balls[i];
                
                ctx.beginPath();
                ctx.arc(b.x, b.y, ballRadius, 0, Math.PI * 2);
                ctx.fillStyle = i === 0 ? "#fff" : "#ffcc00"; // 첫번째 공은 흰색, 추가 공은 노란색
                ctx.fill();
                ctx.closePath();

                if (gameActive) {
                    // 벽 충돌
                    if (b.x + b.dx > canvas.width - ballRadius || b.x + b.dx < ballRadius) b.dx = -b.dx;
                    if (b.y + b.dy < ballRadius) b.dy = -b.dy;

                    // 패들 충돌
                    if (b.y + b.dy > canvas.height - paddleHeight - 10 - ballRadius) {
                        if (b.x > paddleX && b.x < paddleX + paddleWidth) {
                            let relX = (b.x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
                            b.dx = relX * baseSpeed;
                            b.dy = -b.dy;
                        } else if (b.y + b.dy > canvas.height) {
                            balls.splice(i, 1);
                            i--;
                            continue;
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
                                        br.status = 0;
                                        score += 10;
                                        scoreSpan.innerText = score;
                                        if (Math.random() < 0.15) items.push({ x: br.x + brickWidth / 2, y: br.y });
                                    }
                                    breakFound = true;
                                    break;
                                }
                            }
                        }
                        if (breakFound) break;
                    }

                    b.x += b.dx;
                    b.y += b.dy;
                }
            }

            // 모든 공이 사라졌을 때
            if (balls.length === 0 && gameActive) {
                lives--;
                livesSpan.innerText = lives;
                gameActive = false;
                if (lives <= 0) {
                    msgDiv.innerText = "GAME OVER (F5를 눌러 재시작)";
                    msgDiv.style.display = "block";
                } else {
                    msgDiv.innerText = "공을 잃었습니다! 다시 시작하려면 방향키를 누르세요.";
                    msgDiv.style.display = "block";
                }
            }

            // 패들 이동
            if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 7;
            else if (leftPressed && paddleX > 0) paddleX -= 7;

            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

# HTML 컴포넌트 실행
components.html(brick_breaker_html, height=650, scrolling=False)
