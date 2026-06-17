import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Vertical Rhythm Game", layout="centered")

# 깔끔한 제목
st.title("🎵 세로형 모바일 리듬 게임")

# 리듬 게임 HTML/JS
rhythm_game_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Vertical Rhythm Game</title>
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
            border: 4px solid #a932ff;
            background-color: #0b0813;
            box-shadow: 0 0 25px rgba(169, 50, 255, 0.4);
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
            <div>COMBO: <span id="combo" class="stat-val">0</span></div>
            <div>LIVES: <span id="lives" class="stat-val">10</span></div>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <div id="msg">키보드 D, F, J, K 또는 화면을 터치하세요!<br>스페이스바나 클릭 시 음악이 시작됩니다.</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const comboSpan = document.getElementById("combo");
        const livesSpan = document.getElementById("lives");
        const stageSpan = document.getElementById("stage");
        const msgDiv = document.getElementById("msg");
        const adminUi = document.getElementById("adminUi");

        // 게임 설정 변수
        let stage = 1;
        let combo = 0;
        let maxCombo = 0;
        let lives = 10;
        let score = 0;
        let gameActive = false;
        let noteSpeed = 5;
        let notes = [];
        let totalNotesCreated = 0;
        let totalNotesLimit = 40; // 한 스테이지당 내려올 총 노트 개수

        // 판정선 및 라인 세팅
        const lineCount = 4;
        const lineWidth = canvas.width / lineCount;
        const judgmentY = canvas.height - 80; // 판정선 높이
        const noteHeight = 20;

        // 조작 키 맵핑
        const keys = { 'd': 0, 'f': 1, 'j': 2, 'k': 3 };
        let keyStatus = [false, false, false, false];
        let judgmentTexts = []; // 판정 텍스트 이펙트 배열

        // 관리자 모드 관련
        let cheatBuffer = "";
        let isAdmin = false;

        function initStage() {
            notes = [];
            totalNotesCreated = 0;
            totalNotesLimit = 30 + stage * 10;
            noteSpeed = 5 + stage * 0.8;
            lives = 10;
            combo = 0;
            comboSpan.innerText = combo;
            livesSpan.innerText = lives;
            stageSpan.innerText = stage;
        }

        // 무작위 노트 생성 패턴
        function spawnNote() {
            if (totalNotesCreated >= totalNotesLimit) return;
            
            let lane = Math.floor(Math.random() * lineCount);
            let isGold = Math.random() < 0.15; // 15% 확률로 황금 보너스 노트
            notes.push({
                lane: lane,
                y: -noteHeight,
                type: isGold ? 'gold' : 'normal'
            });
            totalNotesCreated++;
        }

        function checkHit(lane) {
            let hitFound = false;
            for (let i = 0; i < notes.length; i++) {
                let n = notes[i];
                if (n.lane === lane) {
                    // 판정선 타겟 거리에 수렴하는지 체크 (오차범위 계산)
                    let distance = Math.abs(n.y - judgmentY);
                    if (distance < 45) {
                        hitFound = true;
