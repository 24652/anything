import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Vertical Brick Breaker", layout="centered")

# 깔끔한 제목
st.title("📱 세로형 익스트림 벽돌 깨기 (스테이지 클리어 버전)")

# 게임 로직 HTML/JS
brick_breaker_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Vertical Extreme Brick Breaker</title>
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        #gameContainer { position: relative; }
        #gameCanvas {
            border: 4px solid #4a90e2;
            background-color: #0c0f14;
            box-shadow: 0 0 25px rgba(74, 144, 226, 0.3);
            border-radius: 12px;
        }
        #gameUi {
            display: flex;
            justify-content: space-between;
            width: 420px;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .stat-val { color: #00ffcc; }
        #msg {
            position: absolute;
            top: 55%;
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
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="gameUi">
            <div>STAGE: <span id="stage" class="stat-val">1</span></div>
            <div>SCORE: <span id="score" class="stat-val">0</span></div>
            <div>LIVES: <span id="lives" class="stat-val">3</span></div>
        </div>
        <canvas id="gameCanvas" width="420" height="600"></canvas>
        <div id="msg">화면이나 방향키(← →)를 눌러 시작하세요!<br>[⚡획득 시 스페이스바로 레이저 발사!]</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreSpan = document.getElementById("score");
        const livesSpan = document.getElementById("lives");
        const stageSpan = document.getElementById("stage");
        const msgDiv = document.getElementById("msg");

        const ballRadius = 7;
        const paddleHeight = 12;
        const paddleWidth = 85;
        const brickWidth = 40;
        const brickHeight = 18;
        const brickPadding = 5;
        const brickOffsetTop = 50;
        const brickOffsetLeft = 12;

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
        let baseSpeed = 4.0;
        let laserTimer = 0;
        let shieldTimer = 0;

        function initBricks() {
            bricks = [];
            const rows = 5;
            const cols = 9; 

            for (let c = 0; c < cols; c++) {
                bricks[c] = [];
                for (let r = 0; r < rows; r++) {
                    let rand = Math.random();
                    if (rand < 0.08 && stage > 1) {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'unbreakable' };
                    } else if (rand < 0.18) {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'exploding' };
                    } else if (rand < 0.25) {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'gold' };
                    } else {
                        bricks[c][r] = { x: 0, y: 0, status: 1, type: 'normal' };
                    }
                }
            }
        }

        function createBall() {
            return {
                x: paddleX + paddleWidth / 2,
                y: canvas.height - 40,
                dx: baseSpeed * (Math.random() - 0.5) * 1.2,
                dy: -baseSpeed,
                active: true
            };
        }

        function createParticles(x, y, color) {
            for (let i = 0; i < 6; i++) {
                particles.push({
                    x: x, y: y,
                    dx: (Math.random() - 0.5) * 3,
                    dy: (Math.random() - 0.5) * 3,
                    alpha: 1,
                    color: color
                });
            }
        }

        function triggerExplosion(col, row) {
            const targets = [
                {c: col-1, r: row}, {c: col+1, r: row},
                {c: col, r: row-1}, {c: col, r: row+1}
            ];
            targets.forEach(t => {
                if (bricks[t.c] && bricks[t.c][t.r] && bricks[t.c][t.r].status === 1) {
                    let targetBrick = bricks[t.c][t.r];
                    if (targetBrick.type !== 'unbreakable') {
                        targetBrick.status = 0;
                        score += 10;
                        createParticles(targetBrick.x + brickWidth/2, targetBrick.y + brickHeight/2, "#ff6600");
                    }
                }
            });
        }

        initBricks();

        // 입력 감지
        document.addEventListener("keydown", (e) => {
            if (e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
            else if (e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
            
            if (e.key == " " && laserTimer > 0 && gameActive) {
                lasers.push({ x: paddleX + 10, y: canvas.height - 25 });
                lasers.push({ x: paddleX + paddleWidth - 10, y: canvas.height - 25 });
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

        canvas.addEventListener("mousemove", (e) => {
            let relativeX = e.clientX - canvas.getBoundingClientRect().left;
            if (relativeX > 0 && relativeX < canvas.width) {
                paddleX = relativeX - paddleWidth / 2;
            }
            if (!gameActive && lives > 0 && e.buttons === 1) {
                gameActive = true;
                msgDiv.style.display = "none";
                if (balls.length === 0) balls.push(createBall());
            }
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (shieldTimer > 0) {
                shieldTimer--;
                ctx.beginPath();
                ctx.strokeStyle = "#00bfff";
                ctx.lineWidth = 4;
                ctx.moveTo(0, canvas.height - 2);
                ctx.lineTo(canvas.width, canvas.height - 2);
                ctx.stroke();
                ctx.lineWidth = 1;
                ctx.closePath();
            }

            // 부숴야 할 남은 블록 개수 카운트 변수
            let breakableBricksLeft = 0;

            for (let c = 0; c < bricks.length; c++) {
                for (let r = 0; r < bricks[c].length; r++) {
                    let b = bricks[c][r];
                    if (b.status == 1) {
                        // 강철 블록이 아니면 무조건 깨야 할 블록으로 체크
                        if (b.type !== 'unbreakable') breakableBricksLeft++;
                        
                        let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                        let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                        b.x = brickX; b.y = brickY;
                        
                        ctx.beginPath();
                        ctx.rect(brickX, brickY, brickWidth, brickHeight);
                        
                        if (b.type === 'unbreakable') ctx.fillStyle = '#555';
                        else if (b.type === 'exploding') ctx.fillStyle = '#ff6600';
                        else if (b.type === 'gold') ctx.fillStyle = '#ffd700';
                        else ctx.fillStyle = `hsl(${stage * 40 + r * 20}, 75%, 55%)`;
                        
                        ctx.fill();
                        ctx.strokeStyle = "#0c0f14";
                        ctx.stroke();
                        ctx.closePath();
                    }
                }
            }

            // 점수와 상관없이 부술 수 있는 블록이 0개가 되면 무조건 스테이지 증가!
            if (breakableBricksLeft === 0 && gameActive) {
                stage++;
                stageSpan.innerText = stage;
                baseSpeed += 0.3; // 스테이지 증가 시 속도 소폭 상승
                gameActive = false;
                balls = []; items = []; lasers = []; laserTimer = 0; shieldTimer = 0;
                initBricks();
                msgDiv.innerHTML = `🎉 STAGE ${stage} START 🎉<br>화면을 클릭해 계속하세요!`;
                msgDiv.style.display = "block";
            }

            // 패들
            ctx.beginPath();
            ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
            ctx.fillStyle = laserTimer > 0 ? "#b000ff" : "#0095DD";
            ctx.fill();
            ctx.closePath();

            // 레이저
            for (let l = 0; l < lasers.length; l++) {
                let laz = lasers[l]; laz.y -= 7;
                ctx.fillStyle = "#ff00ff";
                ctx.fillRect(laz.x, laz.y, 3, 10);

                let lazHit = false;
                for (let c = 0; c < bricks.length; c++) {
                    for (let r = 0; r < bricks[c].length; r++) {
                        let br = bricks[c][r];
                        if (br.status == 1 && laz.x > br.x && laz.x < br.x + brickWidth && laz.y > br.y && laz.y < br.y + brickHeight) {
                            lazHit = true;
                            if (br.type !== 'unbreakable') {
                                br.status = 0;
                                score += br.type === 'gold' ? 50 : 10;
                                scoreSpan.innerText = score;
                                if (br.type === 'exploding') triggerExplosion(c, r);
                            }
                            break;
                        }
                    }
                    if (lazHit) break;
                }
                if (lazHit || laz.y < 0) { lasers.splice(l, 1); l--; }
            }

            if (laserTimer > 0) laserTimer--;

            // 아이템
            for (let i = 0; i < items.length; i++) {
                let it = items[i]; it.y += 2.2;
                ctx.beginPath();
                ctx.arc(it.x, it.y, 9, 0, Math.PI * 2);
                ctx.fillStyle = it.type === 'BALL' ? "#00ff00" : (it.type === 'LASER' ? "#b000ff" : "#00bfff");
                ctx.fill();
                ctx.closePath();

                if (it.y > canvas.height - paddleHeight - 15 && it.x > paddleX && it.x < paddleX + paddleWidth) {
                    if (it.type === 'BALL') balls.push(createBall());
                    else if (it.type === 'LASER') laserTimer = 350;
                    else if (it.type === 'SHIELD') shieldTimer = 500;
                    items.splice(i, 1); i--;
                } else if (it.y > canvas.height) { items.splice(i, 1); i--; }
            }

            // 파티클
            for (let p = 0; p < particles.length; p++) {
                let pt = particles[p]; pt.x += pt.dx; pt.y += pt.dy; pt.alpha -= 0.025;
                if (pt.alpha <= 0) { particles.splice(p, 1); p--; continue; }
                ctx.save(); ctx.globalAlpha = pt.alpha;
                ctx.fillStyle = pt.color;
                ctx.fillRect(pt.x, pt.y, 2.5, 2.5);
                ctx.restore();
            }

            // 공
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

                    if (b.y + b.dy > canvas.height - ballRadius && shieldTimer > 0) {
                        b.dy = -b.dy;
                    }

                    if (b.y + b.dy > canvas.height - paddleHeight - 10 - ballRadius) {
                        if (b.x > paddleX && b.x < paddleX + paddleWidth) {
                            let relX = (b.x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
                            b.dx = relX * baseSpeed * 1.2; b.dy = -b.dy;
                        } else if (b.y + b.dy > canvas.height) {
                            balls.splice(i, 1); i--; continue;
                        }
                    }

                    let breakFound = false;
                    for (let c = 0; c < bricks.length; c++) {
                        for (let r = 0; r < bricks[c].length; r++) {
                            let br = bricks[c][r];
                            if (br.status == 1) {
                                if (b.x > br.x && b.x < br.x + brickWidth && b.y > br.y && b.y < br.y + brickHeight) {
                                    b.dy = -b.dy;
                                    if (br.type !== 'unbreakable') {
                                        br.status = 0;
                                        score += br.type === 'gold' ? 50 : 10;
                                        scoreSpan.innerText = score;
                                        
                                        if (br.type === 'exploding') triggerExplosion(c, r);
                                        
                                        let dropChance = br.type === 'gold' ? 0.60 : 0.15;
                                        if (Math.random() < dropChance) {
                                            let pool = ['BALL', 'LASER', 'SHIELD'];
                                            items.push({ x: br.x + brickWidth/2, y: br.y, type: pool[Math.floor(Math.random()*pool.length)] });
                                        }
                                        createParticles(br.x + brickWidth/2, br.y + brickHeight/2, br.type === 'gold' ? '#ffd700' : '#00ffcc');
                                    } else {
                                        createParticles(br.x + brickWidth/2, br.y + brickHeight/2, '#ffffff');
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

            if (balls.length === 0 && gameActive) {
                lives--; livesSpan.innerText = lives; gameActive = false; laserTimer = 0;
                if (lives <= 0) {
                    msgDiv.innerHTML = "💥 GAME OVER 💥<br>새로고침(F5)으로 재도전!";
                    msgDiv.style.display = "block";
                } else {
                    msgDiv.innerText = "터치나 화살표 키로 재발사!";
                    msgDiv.style.display = "block";
                }
            }

            if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 6;
            else if (leftPressed && paddleX > 0) paddleX -= 6;

            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

components.html(brick_breaker_html, height=670, scrolling=False)
