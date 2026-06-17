import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Almighty Edition", layout="wide")

full_game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #020617; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        #gameWrapper { position: relative; width: 900px; height: 550px; border: 2px solid #334155; overflow: hidden; }
        canvas { display: block; }
        #uiLayer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <canvas id="gameCanvas" width="900" height="550"></canvas>
    </div>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // [게임 상태 변수]
        let stamina = 100;
        let runners = [false, false, false]; // 1, 2, 3루
        let adminMode = false;
        let team = "한화";
        let teamColors = {"한화": "#f97316", "삼성": "#1e40af", "KIA": "#b91c1c", "LG": "#000000", "두산": "#ffffff"};
        
        let pitchTypes = ["포심", "슬라이더", "커브", "포크", "체인지업", "싱커"];
        let B=0, S=0, O=0;

        // [어드민 키 입력]
        window.addEventListener("keydown", (e) => {
            if(e.shiftKey) {
                if(e.key === 's') S = (S+1)%3;
                if(e.key === 'b') B = (B+1)%4;
                if(e.key === 'h') alert("안타 발동!");
                if(e.key === 'r') alert("홈런 발동!");
            }
        });

        function drawField() {
            // 그라운드 및 팀 컬러 유니폼 로직
            ctx.fillStyle = teamColors[team] || "#22c55e";
            ctx.fillRect(0, 0, 900, 550);
            
            // 주자 표시
            ctx.fillStyle = "white";
            if(runners[0]) ctx.fillRect(600, 310, 20, 20); // 1루
            if(runners[1]) ctx.fillRect(450, 230, 20, 20); // 2루
            if(runners[2]) ctx.fillRect(300, 310, 20, 20); // 3루
            
            // 체력바
            ctx.fillStyle = "red";
            ctx.fillRect(50, 50, stamina * 2, 10);
        }

        function loop() {
            ctx.clearRect(0, 0, 900, 550);
            drawField();
            
            // 체력에 따른 제구 흔들림
            if(stamina < 50) {
                ctx.fillStyle = "yellow";
                ctx.fillText("제구 불안정!", 400, 50);
            }
            
            requestAnimationFrame(loop);
        }
        loop();
    </script>
</body>
</html>
"""

components.html(full_game_code, height=600, width=950)
