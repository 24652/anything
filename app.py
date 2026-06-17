import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KBO Pro Baseball - Max Limit Edition", layout="centered")
st.title("⚾ KBO 모바일 프로야구 (Limit Break Ver.)")

max_limit_baseball_html = """
<!DOCTYPE html>
<html>
<head>
    <title>KBO Pro Baseball Max Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700;900&display=swap');
        body {
            margin: 0; padding: 0;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background-color: #0b0f19; color: #fff;
            font-family: 'Noto Sans KR', sans-serif;
            height: 100vh; overflow: hidden; user-select: none;
        }
        #gameWrapper {
            position: relative; width: 440px; height: 650px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            border-radius: 16px; overflow: hidden; border: 2px solid #334155;
        }
        #gameCanvas {
            background: linear-gradient(to bottom, #112211 0%, #1e3a1e 40%, #166534 100%);
            display: block;
        }
        /* Glassmorphism UI */
        #topScoreBoard {
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
            width: 90%; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15); border-radius: 12px;
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 15px; box-sizing: border-box; z-index: 10;
        }
        .board-col { display: flex; flex-direction: column; align-items: center; }
        .inning-text { font-size: 15px; font-weight: 900; color: #fbbf24; text-shadow: 0 0 5px rgba(251, 191, 36, 0.5); }
        .score-text { font-size: 24px; font-weight: 900; letter-spacing: 2px; }
        .player-info { font-size: 12px; color: #cbd5e1; margin-top: 4px; }
        .bso-board { display: flex; gap: 8px; font-weight: 700; font-size: 14px; }
        .bso-board div span { display: inline-block; width: 10px; text-align: center; }
        
        #teamSelectScreen {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 30;
        }
        .team-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; width: 85%; margin-top: 20px; }
        .team-btn {
            background: rgba(255,255,255,0.05); color: white; border: 1px solid rgba(255,255,255,0.2);
            padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer;
            transition: all 0.2s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Noto Sans KR';
        }
        .team-btn:hover { background: #3b82f6; border-color: #60a5fa; transform: translateY(-2px); }
        
        #msgOverlay {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; font-size: 20px; font-weight: 900; color: #fff;
            text-shadow: 0px 4px 10px rgba(0,0,0,0.8); pointer-events: none; z-index: 15; width: 100%;
        }
        
        #bottomControls {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            width: 90%; display: flex; gap: 10px; justify-content: center; z-index: 10;
        }
        .modern-btn {
            background: linear-gradient(to bottom, #3b82f6, #1d4ed8); color: white;
            border: 1px solid #60a5fa; padding: 12px 0; border-radius: 8px; font-weight: 900;
            cursor: pointer; flex: 1; text-transform: uppercase; letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4); font-family: 'Noto Sans KR';
        }
        .modern-btn:active { transform: scale(0.97); }
        .btn-pitch-fast { background: linear-gradient(to bottom, #ef4444, #b91c1c); border-color: #f87171; }
        .btn-pitch-breaking { background: linear-gradient(to bottom, #f59e0b, #b45309); border-color: #fbbf24; }
        .btn-bullpen { background: linear-gradient(to bottom, #64748b, #334155); border-color: #94a3b8; flex: 0.5; }

        #adminUi {
            display: none; position: absolute; top: 85px; left: 50%; transform: translateX(-50%);
            background: #db2777; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold; z-index: 20;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="teamSelectScreen">
            <h1 style="margin:0; font-style:italic; text-shadow:0 0 15px rgba(59,130,246,0.8);">PRO BASEBALL</h1>
            <p style="color:#94a3b8; font-size:13px; margin:5px 0 15px 0;">플레이할 구단을 선택하세요</p>
            <div class="team-grid" id="teamGrid"></div>
        </div>

        <div id="topScoreBoard">
            <div class="board-col" style="width: 30%; align-items: flex-start;">
                <div class="inning-text" id="uiInning">1회초 공격</div>
                <div class="player-info" id="uiBatterInfo">타자: 준비중</div>
            </div>
            <div class="board-col" style="width: 40%;">
                <div class="score-text"><span id="scPlayer" style="color:#60a5fa">0</span> : <span id="scCpu" style="color:#f87171">0</span></div>
                <div class="player-info" id="uiPitcherInfo">마운드: 준비중</div>
            </div>
            <div class="board-col" style="width: 30%; align-items: flex-end;">
                <div class="bso-board">
                    <div style="color:#34d399;">B <span id="uiB">0</span></div>
                    <div style="color:#fbbf24;">S <span id="uiS">0</span></div>
                    <div style="color:#ef4444;">O <span id="uiO">0</span></div>
                </div>
            </div>
        </div>

        <div id="adminUi">[ADMIN] [ : 이전 / ] : 다음 이닝</div>
        <div id="msgOverlay">팀을 선택하면 경기가 시작됩니다.</div>
        
        <canvas id="gameCanvas" width="440" height="650"></canvas>
        <div id="bottomControls"></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const msgDiv = document.getElementById("msgOverlay");
        const controls = document.getElementById("bottomControls");
        
        // KBO 데이터
        const kboDB = {
            "삼성 라이온즈": { p: ["원태인", "김태훈", "오승환"], b: ["구자욱", "강민호", "맥키넌", "류지혁", "김영웅", "이재현", "김지찬", "이성규", "김성윤"] },
            "LG 트윈스": { p: ["임찬규", "유영찬", "김진성"], b: ["홍창기", "신민재", "오스틴", "문보경", "박동원", "오지환", "박해민", "구본혁", "이영빈"] },
            "KIA 타이거즈": { p: ["양현종", "전상현", "정해영"], b: ["박찬호", "최원준", "김도영", "최형우", "나성범", "소크라테스", "김선빈", "김태군", "변우혁"] },
            "두산 베어스": { p: ["곽빈", "이병헌", "김택연"], b: ["정수빈", "허경민", "양의지", "김재환", "양석환", "강승호", "라모스", "전민재", "조수행"] },
            "KT 위즈": { p: ["고영표", "김민", "박영현"], b: ["로하스", "강백호", "장성우", "황재균", "오재일", "배정대", "신본기", "심우준", "문상철"] },
            "SSG 랜더스": { p: ["김광현", "노경은", "문승원"], b: ["최정", "에레디아", "한유섬", "박성한", "고명준", "이지영", "최지훈", "추신수", "박지환"] },
            "롯데 자이언츠": { p: ["반즈", "김상수", "김원중"], b: ["황성빈", "윤동희", "레이예스", "전준우", "나승엽", "고승민", "유강남", "박승욱", "노진혁"] },
            "한화 이글스": { p: ["류현진", "한승혁", "주현상"], b: ["페라자", "노시환", "안치홍", "채은성", "문현빈", "최재훈", "이도윤", "장진혁", "황영묵"] },
            "NC 다이노스": { p: ["신민혁", "김영규", "이용찬"], b: ["박민우", "권희동", "데이비슨", "박건우", "서호철", "김형준", "김성욱", "김주원", "도태훈"] },
            "키움 히어로즈": { p: ["후라도", "조상우", "주승우"], b: ["이주형", "도슨", "송성문", "최주환", "김혜성", "고영우", "김재현", "이형종", "장재영"] }
        };

        let myTeam = "", cpuTeam = "";
        let inning = 1, isTop = true;
        let scMy = 0, scCpu = 0;
        let B = 0, S = 0, O = 0;
        let bases = [false, false, false];
        let pIdx = 0, cpuPIdx = 0, bIdx = 0, cpuBIdx = 0;

        let gameActive = false;
        // 공 궤적 트레일 추가
        let ball = { x: 220, y: 220, vx: 0, vy: 0, radius: 2, active: false, trail: [] };
        let isSwinging = false, swingAngle = 0;
        let screenShake = 0;
        let floatingText = [];
        
        let cheatBuffer = ""; let isAdmin = false;

        // 초기화 및 팀 셋업
        const grid = document.getElementById("teamGrid");
        Object.keys(kboDB).forEach(t => {
            let btn = document.createElement("button");
            btn.className = "team-btn"; btn.innerText = t;
            btn.onclick = () => {
                myTeam = t;
                let rem = Object.keys(kboDB).filter(x => x !== t);
                cpuTeam = rem[Math.floor(Math.random() * rem.length)];
                document.getElementById("teamSelectScreen").style.display = "none";
                startGame();
            };
            grid.appendChild(btn);
        });

        function startGame() {
            scMy = 0; scCpu = 0; inning = 1; isTop = true;
            resetHalf(); gameActive = true; updateUI();
        }

        function resetHalf() {
            B = 0; S = 0; O = 0; bases = [false, false, false];
            ball.active = false; isSwinging = false;
            buildBtns();
        }

        function updateUI() {
            document.getElementById("uiInning").innerText = `${inning}회${isTop ? '초 공격' : '말 수비'}`;
            document.getElementById("uiInning").style.color = isTop ? "#60a5fa" : "#f87171";
            document.getElementById("scPlayer").innerText = scMy; document.getElementById("scCpu").innerText = scCpu;
            document.getElementById("uiB").innerText = B; document.getElementById("uiS").innerText = S; document.getElementById("uiO").innerText = O;

            let curP = isTop ? kboDB[cpuTeam].p[cpuPIdx] : kboDB[myTeam].p[pIdx];
            let curB = isTop ? kboDB[myTeam].b[bIdx] : kboDB[cpuTeam].b[cpuBIdx];
            document.getElementById("uiPitcherInfo").innerText = `P: ${curP}`;
            document.getElementById("uiBatterInfo").innerText = `B: ${curB}`;
        }

        function buildBtns() {
            controls.innerHTML = "";
            if (!gameActive) return;
            if (isTop) {
                let btn = document.createElement("button"); btn.className = "modern-btn"; btn.innerText = "💥 배트 스윙 (Space)";
                btn.onclick = () => { if(!ball.active) pitchAI(); else doSwing(); };
                controls.appendChild(btn);
            } else {
                let fBtn = document.createElement("button"); fBtn.className = "modern-btn btn-pitch-fast"; fBtn.innerText = "포심 직구";
                fBtn.onclick = () => pitchPlayer("fast"); controls.appendChild(fBtn);
                
                let bBtn = document.createElement("button"); bBtn.className = "modern-btn btn-pitch-breaking"; bBtn.innerText = "변화구";
                bBtn.onclick = () => pitchPlayer("break"); controls.appendChild(bBtn);

                let bpBtn = document.createElement("button"); bpBtn.className = "modern-btn btn-bullpen"; bpBtn.innerText = "🔄 투수";
                bpBtn.onclick = () => { if(!ball.active){ pIdx = (pIdx+1)%3; addFloat("투수 교체!", "#cbd5e1"); updateUI(); } };
                controls.appendChild(bpBtn);
            }
        }

        function pitchAI() {
            ball.x = 220; ball.y = 220; ball.radius = 3; ball.active = true; ball.trail = [];
            ball.vy = Math.random() > 0.5 ? 7.5 : 5.0; ball.vx = (Math.random() - 0.5) * 1.5;
            msgDiv.style.display = "none";
        }

        function pitchPlayer(type) {
            if (ball.active) return;
            ball.x = 220; ball.y = 220; ball.radius = 3; ball.active = true; ball.trail = [];
            if(type === "fast"){ ball.vy = 8.0; ball.vx = 0; } else { ball.vy = 4.5; ball.vx = 1.2; }
            msgDiv.style.display = "none";
            setTimeout(() => { if (ball.active) doAIswing(); }, type === "fast" ? 380 : 550);
        }

        function doSwing() {
            if (isSwinging || !ball.active) return;
            isSwinging = true; swingAngle = -60;
            let dist = Math.abs(ball.y - 520);
            if (dist < 40) hitProcess(dist, true); else { addFloat("헛스윙!", "#ef4444"); addS(); }
        }

        function doAIswing() {
            isSwinging = true; swingAngle = -60;
            let dist = Math.abs(ball.y - 520);
            if (dist < 38) hitProcess(dist, false); else { addFloat("헛스윙!", "#60a5fa"); addS(); }
        }

        function hitProcess(dist, isMe) {
            ball.active = false; screenShake = 15; // 타격 시 화면 강하게 흔들림 (액션 극대화)
            if (dist < 12) {
                addFloat("💥 HOMERUN 💥", "#fbbf24"); advanceRun(4, isMe);
            } else {
                addFloat("⚾ HIT!", "#34d399"); advanceRun(1, isMe);
            }
            nextB();
        }

        function addS() {
            S++; if(S>=3){ addFloat("삼진 아웃!", "#ef4444"); addO(); nextB(); } updateUI();
        }
        function addO() {
            O++; if(O>=3) turnOver(); updateUI();
        }
        function advanceRun(n, isMe) {
            let r = 0;
            for(let i=0; i<n; i++){ if(bases[2]) r++; bases[2]=bases[1]; bases[1]=bases[0]; bases[0]=(i===0); }
            if(isMe) scMy += r; else scCpu += r; B=0; S=0; updateUI();
        }
        function nextB() {
            B=0; S=0; if(isTop) bIdx=(bIdx+1)%9; else cpuBIdx=(cpuBIdx+1)%9;
            setTimeout(() => { if(gameActive) msgDiv.style.display = "block"; }, 1000);
        }
        function turnOver() {
            if(isTop) {
                isTop = false; resetHalf(); msgDiv.innerHTML = "공수교대<br><span style='font-size:14px;color:#cbd5e1'>직접 투구하세요</span>";
            } else {
                isTop = true; inning++;
                if(inning > 9) {
                    gameActive = false; msgDiv.innerHTML = `경기 종료<br>${scMy > scCpu ? myTeam+' 승리!' : '패배..'}`; controls.innerHTML="";
                } else {
                    resetHalf(); msgDiv.innerHTML = `${inning}회초 공격 시작`;
                }
            }
            msgDiv.style.display = "block"; updateUI();
        }

        function addFloat(txt, col) { floatingText.push({ t: txt, c: col, y: 350, a: 1.0 }); }

        // 단축키 제어
        document.addEventListener("keydown", (e) => {
            let k = e.key.toLowerCase(); cheatBuffer += k;
            if(cheatBuffer.endsWith("joonmin")) { isAdmin = !isAdmin; document.getElementById("adminUi").style.display = isAdmin ? "block" : "none"; }
            if(isAdmin && e.key === "]") { inning++; resetHalf(); updateUI(); }
            if(e.key === " " && isTop) { e.preventDefault(); if(!ball.active) pitchAI(); else doSwing(); }
        });

        // ==========================
        // 고도화된 렌더링 엔진 (실루엣/3D느낌)
        // ==========================
        function drawField() {
            // 잔디 그라데이션 명암
            let grad = ctx.createLinearGradient(0, 200, 0, 600);
            grad.addColorStop(0, "#064e3b"); grad.addColorStop(1, "#166534");
            ctx.fillStyle = grad; ctx.fillRect(0,0,440,650);

            // 내야 흙 영역 (다이아몬드)
            ctx.fillStyle = "#92400e";
            ctx.beginPath(); ctx.moveTo(220, 560); ctx.lineTo(390, 370); ctx.lineTo(220, 180); ctx.lineTo(50, 370); ctx.fill();
            
            // 내야 잔디 라인
            ctx.fillStyle = "#15803d";
            ctx.beginPath(); ctx.moveTo(220, 470); ctx.lineTo(310, 370); ctx.lineTo(220, 270); ctx.lineTo(130, 370); ctx.fill();

            // 베이스 & 주자 램프 연출
            const drawBase = (x, y, active) => {
                ctx.fillStyle = active ? "#ef4444" : "#ffffff";
                ctx.beginPath(); ctx.moveTo(x, y-6); ctx.lineTo(x+6, y); ctx.lineTo(x, y+6); ctx.lineTo(x-6, y); ctx.fill();
            };
            ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.moveTo(220, 550); ctx.lineTo(225, 555); ctx.lineTo(220, 560); ctx.lineTo(215, 555); ctx.fill(); // Home
            drawBase(375, 365, bases[0]); // 1B
            drawBase(220, 195, bases[1]); // 2B
            drawBase(65, 365, bases[2]);  // 3B

            // 스트라이크 타격 존 시각화 (네온 효과)
            ctx.fillStyle = "rgba(56, 189, 248, 0.15)"; ctx.fillRect(160, 490, 120, 50);
            ctx.strokeStyle = "rgba(56, 189, 248, 0.6)"; ctx.lineWidth = 2; ctx.strokeRect(160, 490, 120, 50);
        }

        function drawSilhouette(x, y, isBatter) {
            ctx.fillStyle = "rgba(0, 0, 0, 0.6)"; // 그림자
            ctx.beginPath(); ctx.ellipse(x, y+35, 15, 4, 0, 0, Math.PI*2); ctx.fill();
            
            ctx.fillStyle = isBatter ? (isTop ? "#e2e8f0" : "#94a3b8") : (isTop ? "#94a3b8" : "#e2e8f0");
            // 몸통
            ctx.fillRect(x-6, y+10, 12, 25);
            // 머리
            ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI*2); ctx.fill();
        }

        function gameLoop() {
            ctx.save();
            // 화면 흔들림 효과 적용
            if (screenShake > 0) {
                ctx.translate((Math.random()-0.5)*screenShake, (Math.random()-0.5)*screenShake);
                screenShake--;
            }
            
            drawField();

            // 실루엣 렌더링
            drawSilhouette(220, 200, false); // 투수
            drawSilhouette(185, 510, true);  // 타자 (왼쪽 타석 고정)
            drawSilhouette(220, 575, false); // 포수

            // 투구 및 공 잔상(Trail) 렌더링
            if (ball.active) {
                ball.trail.push({x: ball.x, y: ball.y, r: ball.radius});
                if(ball.trail.length > 8) ball.trail.shift();

                // 잔상 그리기
                for(let i=0; i<ball.trail.length; i++){
                    let pt = ball.trail[i];
                    ctx.beginPath(); ctx.arc(pt.x, pt.y, pt.r, 0, Math.PI*2);
                    ctx.fillStyle = `rgba(255, 255, 255, ${i / ball.trail.length * 0.5})`;
                    ctx.fill();
                }

                ball.x += ball.vx; ball.y += ball.vy; ball.radius += 0.22; // 줌인 3D 원근

                // 본체 공
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
                ctx.fillStyle = "#ffffff"; ctx.fill(); ctx.strokeStyle = "#cbd5e1"; ctx.stroke();

                if (ball.y > 580) { ball.active = false; addFloat("스트라이크", "#f87171"); addS(); }
            }

            // 역동적 배트 스윙 애니메이션
            if (isSwinging) {
                swingAngle += 25;
                ctx.save(); ctx.translate(185, 530); ctx.rotate(swingAngle * Math.PI / 180);
                ctx.fillStyle = "#d97706"; ctx.fillRect(0, -4, 60, 8); // 야구 방망이
                ctx.restore();
                if (swingAngle > 120) isSwinging = false;
            } else {
                ctx.save(); ctx.translate(185, 530); ctx.rotate(-60 * Math.PI / 180);
                ctx.fillStyle = "#d97706"; ctx.fillRect(0, -3, 40, 6); ctx.restore();
            }

            // 플로팅 텍스트 이펙트
            for(let i=floatingText.length-1; i>=0; i--){
                let ft = floatingText[i];
                ctx.font = "italic 900 32px 'Noto Sans KR'"; ctx.textAlign = "center";
                ctx.fillStyle = ft.c; ctx.globalAlpha = ft.a;
                // 텍스트 테두리 처리
                ctx.lineWidth = 4; ctx.strokeStyle = "#000"; ctx.strokeText(ft.t, 220, ft.y);
                ctx.fillText(ft.t, 220, ft.y);
                
                ft.y -= 2; ft.a -= 0.02; ctx.globalAlpha = 1.0;
                if(ft.a <= 0) floatingText.splice(i, 1);
            }

            ctx.restore();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

components.html(max_limit_baseball_html, height=660, scrolling=False)
