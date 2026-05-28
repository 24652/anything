import streamlit as st
import streamlit.components.v1 as components
import random

# Page configuration
st.set_page_config(page_title="Streamlit Brick Breaker", layout="wide")

# App title and instructions
st.title("🧱 Streamlit 벽돌 깨기 게임")
st.markdown("""
왼쪽/오른쪽 화살표 키를 사용하여 패들을 움직이고 공을 튕겨 모든 벽돌을 깨뜨리세요.
게임은 HTML5 Canvas와 JavaScript를 사용하여 구현되었으며 Streamlit에 내장되어 있습니다.
""")

# Define the Brick Breaker game in HTML and JavaScript
brick_breaker_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Brick Breaker</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #333;
            color: white;
            font-family: sans-serif;
            height: 100vh;
            overflow: hidden; /* Prevent scrolling */
        }
        #gameCanvas {
            border: 4px solid #fff;
            background-color: #000;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
        }
        #gameUi {
            position: absolute;
            top: 20px;
            left: 20px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div id="gameUi">
        <div>Score: <span id="score">0</span></div>
        <div>Lives: <span id="lives">3</span></div>
        <div id="status">Press Left/Right Arrows</div>
    </div>
    <canvas id="gameCanvas" width="800" height="600"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreSpan = document.getElementById("score");
        const livesSpan = document.getElementById("lives");
        const statusDiv = document.getElementById("status");

        // Game constants and variables
        const ballRadius = 10;
        const paddleHeight = 15;
        const paddleWidth = 100;
        const brickRowCount = 5;
        const brickColumnCount = 9;
        const brickWidth = 75;
        const brickHeight = 25;
        const brickPadding = 10;
        const brickOffsetTop = 50;
        const brickOffsetLeft = 30;

        let x = canvas.width / 2;
        let y = canvas.height - 30;
        let dx = 4; // Horizontal ball speed
        let dy = -4; // Vertical ball speed
        let paddleX = (canvas.width - paddleWidth) / 2;
        let rightPressed = false;
        let leftPressed = false;
        let score = 0;
        let lives = 3;
        let gameStarted = false;
        let gameOver = false;

        // Initialize bricks
        let bricks = [];
        for (let c = 0; c < brickColumnCount; c++) {
            bricks[c] = [];
            for (let r = 0; r < brickRowCount; r++) {
                bricks[c][r] = { x: 0, y: 0, status: 1, color: `hsl(${r * 40}, 70%, 60%)` };
            }
        }

        // Event listeners for paddle control
        document.addEventListener("keydown", keyDownHandler, false);
        document.addEventListener("keyup", keyUpHandler, false);

        function keyDownHandler(e) {
            if (e.key == "Right" || e.key == "ArrowRight") {
                rightPressed = true;
                startGame();
            } else if (e.key == "Left" || e.key == "ArrowLeft") {
                leftPressed = true;
                startGame();
            }
        }

        function keyUpHandler(e) {
            if (e.key == "Right" || e.key == "ArrowRight") {
                rightPressed = false;
            } else if (e.key == "Left" || e.key == "ArrowLeft") {
                leftPressed = false;
            }
        }

        function startGame() {
            if (!gameStarted && !gameOver) {
                gameStarted = true;
                statusDiv.innerText = "Game On!";
            }
        }

        // Collision detection for ball and bricks
        function collisionDetection() {
            for (let c = 0; c < brickColumnCount; c++) {
                for (let r = 0; r < brickRowCount; r++) {
                    let b = bricks[c][r];
                    if (b.status == 1) {
                        if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                            dy = -dy;
                            b.status = 0;
                            score++;
                            scoreSpan.innerText = score;
                            if (score == brickRowCount * brickColumnCount) {
                                gameOver = true;
                                statusDiv.innerText = "YOU WIN! Refresh to play again.";
                                // Option: Reset and increase speed for next level
                            }
                        }
                    }
                }
            }
        }

        // Draw game elements
        function drawBall() {
            ctx.beginPath();
            ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
            ctx.fillStyle = "#fff";
            ctx.fill();
            ctx.closePath();
        }

        function drawPaddle() {
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
            ctx.fillStyle = "#0095DD";
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

        // Main game loop
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
            drawBricks();
            drawBall();
            drawPaddle();
            collisionDetection();

            // Ball wall collisions
            if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
                dx = -dx;
            }
            if (y + dy < ballRadius) {
                dy = -dy;
            } else if (y + dy > canvas.width) { // For debugging to see if ball goes past canvas
               // dy = -dy;
            }

            // Game movement (if started)
            if (gameStarted && !gameOver) {
                // Ball and paddle collision
                if (y + dy > canvas.height - paddleHeight - 10 - ballRadius) {
                  if (x > paddleX && x < paddleX + paddleWidth) {
                      dy = -dy;
                      // dy = -4 - (score * 0.1); // Option to increase speed with score
                  } else if (y + dy > canvas.height - ballRadius){
                    lives--;
                    livesSpan.innerText = lives;
                    if (!lives) {
                        gameOver = true;
                        statusDiv.innerText = "GAME OVER. Refresh to play again.";
                    } else {
                        // Reset ball and paddle, but keep bricks
                        x = canvas.width / 2;
                        y = canvas.height - 30;
                        dx = 4;
                        dy = -4;
                        paddleX = (canvas.width - paddleWidth) / 2;
                        gameStarted = false;
                        statusDiv.innerText = "Press Arrows to restart ball.";
                    }
                  }
                }

                x += dx;
                y += dy;
            }

            // Paddle movement
            if (rightPressed && paddleX < canvas.width - paddleWidth) {
                paddleX += 7;
            } else if (leftPressed && paddleX > 0) {
                paddleX -= 7;
            }

            requestAnimationFrame(draw); // Call the next frame
        }

        draw(); // Start the game loop
    </script>
</body>
</html>
"""

# Embed the game using components.html
# Need a generous height to ensure the canvas and UI fit without internal scrollbars.
components.html(brick_breaker_html, height=700, scrolling=False)

# Optional: Add GitHub instructions or link
with st.expander("GitHub에 업로드하고 배포하는 방법"):
    st.markdown("""
    1. 이 코드를 `app.py`라는 파일로 저장하세요.
    2. 같은 폴더에 다음 내용을 포함하는 `requirements.txt` 파일을 만드세요:
       ```text
       streamlit
       ```
    3. 이 두 파일을 GitHub 저장소에 업로드하세요.
    4. [Streamlit Community Cloud](https://streamlit.io/cloud)에 가입하고 GitHub 저장소를 연결하여 배포하세요.
    """)
