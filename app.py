import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title="Streamlit Super Brick Breaker", layout="wide")

st.title("🧱 스트리밋 벽돌 깨기: 익스트림 에디션")
st.markdown("""
**[게임 방법]** * 좌우 화살표 키(`←`, `→`)로 패들을 조작하세요.
* 벽돌을 깨면 하늘에서 **아이템(🔴)**이 떨어집니다! 
  * **초록 아이템:** 패들이 길어집니다 (개이득)
  * **빨간 아이템:** 패들이 반토막 납니다 (조심!)
* 모든 벽돌을 깨면 **다음 스테이지**로 넘어가며 공이 더 빨라집니다!
""")

# Enhanced Game HTML/JS
brick_breaker_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Extreme Brick Breaker</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1e1e24;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        #gameContainer {
            position: relative;
        }
        #gameCanvas {
            border: 4px solid #4a90e2;
            background-color: #0b0c10;
            box-shadow: 0 0 25px rgba(74, 144, 226, 0.5);
            border-radius: 8px;
        }
        #gameUi {
            display: flex;
            justify-content: space-between;
            width: 800px;
            margin-bottom: 10px;
            font-size: 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat { color: #66fcf1; }
        #status { color: #ff007f; text-align: center; font-size: 24px; margin-top: 10px;}
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="gameUi">
            <div>Stage: <span id="stage" class="stat">1</span></div>
            <div>Score: <span id="score" class="stat">0</span></div>
            <div>Lives: <span id="lives" class="stat">3</span></div>
        </div>
        <canvas id="gameCanvas" width="800" height="550"></canvas>
        <div id="status">시작하려면 좌우 화살표 키(←, →)를 누르세요!</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreSpan = document.getElementById("score");
        const livesSpan = document.getElementById("lives");
        const stageSpan = document.getElementById("stage");
        const statusDiv = document.getElementById("status");

        // 기본 설정
        const ballRadius = 9;
        const paddleHeight = 15;
        let paddleWidth = 120; // 가변 패들 너비
        const originalPaddleWidth = 120;

        let brickRowCount = 4;
        let brickColumnCount = 9;
        const brickWidth = 75;
        const brickHeight = 22;
        const brickPadding = 10;
        const brickOffsetTop = 40;
        const brickOffsetLeft = 20;

        // 게임 상태 변수
        let x = canvas.width / 2;
        let y = canvas.height - 40;
        let baseSpeed = 4; 
        let dx = baseSpeed;
        let dy = -baseSpeed;
        let paddleX = (canvas.width - paddleWidth) / 2;
        
        let rightPressed = false;
        let leftPressed = false;
        
        let score = 0;
        let lives = 3;
        let stage = 1;
        let gameStarted = false;
        let gameOver = false;

        // 아이템 배열
        let items = [];

        // 벽돌 생성 함수
        let bricks = [];
        function initBricks() {
            bricks = [];
            for (let c = 0; c < brickColumnCount; c++) {
                bricks[c] = [];
                for (let r = 0; r < brickRowCount; r++) {
                    // 아래쪽으로 갈수록 점수가 높은 벽돌 색상 배치
                    let hue = 200 + (r * 35);
                    bricks[c][r] = { x: 0, y: 0, status: 1, color: `hsl(${hue}, 80%, 55%)` };
                }
            }
        }
        initBricks();

        // 키보드 이벤트 리스너
        document.addEventListener("keydown", keyDownHandler, false);
        document.addEventListener("keyup", keyUpHandler, false);

        function keyDownHandler(e) {
            if (e.key == "Right" || e.key == "ArrowRight") { rightPressed = true; startGame(); }
            else if (e.key == "Left" || e.key == "ArrowLeft") { leftPressed = true; startGame(); }
        }

        function keyUpHandler(e) {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        }

        function startGame() {
            if (!gameStarted && !gameOver) {
                gameStarted = true;
                statusDiv.innerText = "🔥 세 부 자 !! 🔥";
            }
        }

        // 충돌 감지 로직 및 아이템 드롭
        function collisionDetection() {
            let activeBricks = 0;
            for (let c = 0; c < brickColumnCount; c++) {
                for (let r = 0; r < brickRowCount; r++) {
                    let b = bricks[c][r];
                    if (b.status == 1) {
                        activeBricks++;
                        if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                            dy = -dy;
                            b.status = 0;
                            score += 10 * stage; // 스테이지별 점수 가중치
                            scoreSpan.innerText = score;

                            // 20% 확률로 아이템 생성
                            if (Math.random() < 0.25) {
                                let itemType = Math.random() > 0.4 ? "GROW" : "SHRINK"; // 좋은거 60%, 나쁜거 40%
                                items.push({
                                    x: b.x + brickWidth / 2,
                                    y: b.y + brickHeight,
                                    type: itemType,
                                    speed: 2.5,
                                    color: itemType === "GROW" ? "#00ff88" : "#ff3333"
                                });
                            }
                        }
                    }
                }
            }

            // 모든 벽돌을 다 깼을 때 -> 다음 스테이지 진행
            if (activeBricks === 0 && gameStarted) {
                stage++;
                stageSpan.innerText = stage;
                baseSpeed += 1; // 공 속도 증가로 난이도 업!
                initBricks();
                resetBallAndPaddle();
                statusDiv.innerText = `🎉 스테이지 ${stage} 시작! 공이 더 빨라졌습니다!`;
            }
        }

        function resetBallAndPaddle() {
            x = canvas.width / 2;
            y = canvas.height - 40;
            dx = baseSpeed * (Math.random() > 0.5 ? 1 : -1);
            dy = -baseSpeed;
            paddleWidth = originalPaddleWidth; // 패들 크기 리셋
            paddleX = (canvas.width - paddleWidth) / 2;
            gameStarted = false;
        }

        // 그리기 함수들
        function drawBall() {
            ctx.beginPath();
            ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
            ctx.fillStyle = "#ffffff";
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#ffffff";
            ctx.fill();
            ctx.closePath();
            ctx.shadowBlur = 0; // 다른 그래픽에 그림자 번짐 방지
        }

        function drawPaddle() {
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 15, paddleWidth, paddleHeight);
            ctx.fillStyle = "#4a90e2";
            ctx.fill();
            ctx.closePath();
        }

        function drawBricks() {
            for (let c = 0; c < brickColumnCount; c++) {
                for (let r = 0; r < brickRowCount; r++) {
                    if (bricks[c][r].status == 1) {
                        let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        bricks[c][r].x = brickX;
                        bricks[c][r].y = brickY;
                        
                        ctx.beginPath();
                        ctx.rect(brickX, brickY, brickWidth, brickHeight);
                        ctx.fillStyle = bricks[c][r].color;
                        ctx.fill();
                        ctx.closePath();
                    }
                }
            }
        }

        function drawAndMoveItems() {
            for (let i = 0; i < items.length; i++) {
                let item = items[i];
                item.y += item.speed;

                // 아이템 그리기 (알약 모양)
                ctx.beginPath();
                ctx.arc(item.x, item.y, 8, 0, Math.PI * 2);
                ctx.fillStyle = item.color;
                ctx.fill();
                ctx.closePath();

                // 패들과 아이템 충돌 검사
                if (item.y > canvas.height - paddleHeight - 25 && item.y < canvas.height - 15) {
                    if (item.x > paddleX && item.x < paddleX + paddleWidth) {
                        // 아이템 효과 적용
                        if (item.type === "GROW") {
                            paddleWidth = Math.min(paddleWidth + 40, 240); // 최대 크기 제한
                            statusDiv.innerText = "✨ 패들 확장! 개이득!";
                        } else if (item.type === "SHRINK") {
                            paddleWidth = Math.max(paddleWidth - 40, 60);  // 최소 크기 제한
                            statusDiv.innerText = "😱 패들 축소! 비상 비상!";
                        }
                        items.splice(i, 1);
                        i--;
                        continue;
                    }
                }

                // 화면 밖으로 나간 아이템 삭제
                if (item.y > canvas.height) {
                    items.splice(i, 1);
                    i--;
                }
            }
        }

        // 메인 게임 루프
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBricks();
            drawBall();
            drawPaddle();
            drawAndMoveItems();
            collisionDetection();

            // 벽면 충돌 처리
            if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
                dx = -dx;
            }
            if (y + dy < ballRadius) {
                dy = -dy;
            }

            // 공이 움직이는 중일 때
            if (gameStarted && !gameOver) {
                // 패들 충돌 판단 구역
                if (y + dy > canvas.height - paddleHeight - 15 - ballRadius) {
                    if (x > paddleX && x < paddleX + paddleWidth) {
                        // 공이 패들의 어느 부위에 부딪혔는지에 따라 반사각 조절 (꿀잼 유발 기술)
                        let hitPos = (x - paddleX) / paddleWidth;
                        dx = baseSpeed * 2 * (hitPos - 0.5);
                        dy = -dy;
                    } 
                    // 바닥에 떨어졌을 때
                    else if (y + dy > canvas.height - ballRadius) {
                        lives--;
                        livesSpan.innerText = lives;
                        items = []; // 떨어지던 아이템 초기화
                        
                        if (lives <= 0) {
                            gameOver = true;
                            statusDiv.innerHTML = "💥 GAME OVER 💥<br>F5를 눌러 다시 도전하세요!";
                        } else {
                            resetBallAndPaddle();
                            statusDiv.innerText = "조작키를 누르면 공이 다시 발사됩니다.";
                        }
                    }
                }

                x += dx;
                y += dy;
            }

            // 패들 키보드 조작
            if (rightPressed && paddleX < canvas.width - paddleWidth) {
                paddleX += 8;
            } else if (leftPressed && paddleX > 0) {
                paddleX -= 8;
            }

            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

# Streamlit에 컴포넌트 띄우기
components.html(brick_breaker_html, height=680, scrolling=False)
