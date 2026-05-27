import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="K-치킨 타이쿤 Master", layout="centered")

# 2. 파이썬 삼중 따옴표 에러를 완벽하게 방지하는 단일 라인 문자열 결합 방식
html_lines = [
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
    "<style>",
    "body { font-family: sans-serif; background-color: #1a1a24; text-align: center; padding: 10px; margin: 0; color: #ffffff; }",
    ".game-wrapper { background: #252632; padding: 20px; border-radius: 20px; border: 4px solid #3b3d54; display: inline-block; width: 340px; }",
    "h1 { color: #ffd43b; margin: 0 0 5px 0; font-size: 24px; text-shadow: 2px 2px 0px #e67e22; }",
    ".game-screen { background-color: #f1f3f5; border: 4px solid #1a1a24; border-radius: 12px; height: 180px; margin: 15px 0; position: relative; overflow: hidden; }",
    ".kitchen-zone { position: absolute; left: 0; top: 0; width: 90px; height: 100%; background-color: #dee2e6; border-right: 4px dashed #495057; }",
    ".kitchen-title { font-size: 11px; color: #495057; font-weight: bold; margin-top: 6px; background: #ced4da; padding: 2px 0; }",
    ".hall-zone { position: absolute; right: 0; top: 0; width: 240px; height: 100%; background-color: #e9ecef; }",
    ".sprite { position: absolute; font-size: 32px; transition: transform 0.08s ease; }",
    ".chef { left: 25px; top: 50px; }",
    ".helper { left: 25px; top: 110px; display: none; }",
    ".table-seat { position: absolute; font-size: 26px; width: 50px; height: 50px; text-align: center; }",
    ".seat1 { right: 140px; top: 30px; }",
    ".seat2 { right: 30px; top: 30px; }",
    ".seat3 { right: 140px; top: 100px; }",
    ".seat4 { right: 30px; top: 100px; }",
    ".money-display { font-size: 26px; font-weight: bold; color: #51cf66; margin: 10px 0; text-shadow: 1px 1px 0px #2b8a3e; }",
    ".stats { font-size: 12px; color: #adc5dc; margin-bottom: 15px; background: #1c1c24; padding: 6px; border-radius: 8px; display: flex; justify-content: space-around; }",
    ".fry-btn { background-color: #f76707; color: white; border: none; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 12px; cursor: pointer; border-bottom: 5px solid #d9480f; box-shadow: 0 4px #1a1a24; outline: none; width: 100%; box-sizing: border-box; }",
    ".fry-btn:active { border-bottom: 1px solid #d9480f; transform: translateY(4px); box-shadow: 0 1px #1a1a24; }",
    ".shop-section { margin-top: 20px; text-align: left; }",
    ".shop-title { font-size: 14px; color: #ffd43b; margin-bottom: 8px; font-weight: bold; }",
    ".upgrade-card { background: #1c1c24; padding: 10px; margin: 6px 0; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #3b3d54; }",
    ".upgrade-info { width: 65%; }",
    ".upgrade-name { font-weight: bold; color: #ffffff; font-size: 12px; }",
    ".upgrade-desc { color: #868e96; font-size: 11px; }",
    ".buy-btn { background-color: #37b24d; color: white; border: none; padding: 8px 12px; font-size: 11px; font-weight: bold; border-radius: 6px; cursor: pointer; }",
    ".buy-btn:disabled { background-color: #495057; color: #868e96; cursor: not-allowed; }",
    "@keyframes floatUp { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(-40px); opacity: 0; } }",
    ".floating-text { position: absolute; color: #40c057; font-weight: bold; font-size: 16px; animation: floatUp 0.6s ease-out forwards; pointer-events: none; z-index: 10; }",
    "</style></head>",
    "<body><div class='game-wrapper'><h1>🍗 타이쿤 마스터</h1><div style='font-size:11px; color:#a6a7b7; margin-bottom:10px;'>레트로 도트 치킨 가게</div>",
    "<div class='game-screen' id='screen'><div class='kitchen-zone'><div class='kitchen-title'>주방</div><div class='sprite chef' id='chef-char'>👨‍🍳</div><div class='sprite helper' id='helper-char'>🧑‍🍳</div></div>",
    "<div class='hall-zone'><div class='table-seat seat1' id='s1'>🪑</div><div class='table-seat seat2' id='s2'>🪑</div><div class='table-seat seat3' id='s3'>🪑</div><div class='table-seat seat4' id='s4'>🪑</div></div></div>",
    "<div class='money-display'><span id='m'>0</span> ₩</div>",
    "<div class='stats'><div>🖱️ 클릭: <span id='pow'>1,000</span></div><div>⏰ 초당: <span id='auto'>0</span></div></div>",
    "<button class='fry-btn' onclick='fry()'>🍗 치킨 튀겨서 서빙하기!</button>",
    "<div class='shop-section'><div class='shop-title'>🛒 업그레이드 상점</div>",
    "<div class='upgrade-card'><div class='upgrade-info'><div class='upgrade-name'>🧑‍🍳 주방 알바 고용</div><div class='upgrade-desc'>자동 튀기기 (초당 +500원)</div></div><button class='buy-btn' id='b1' onclick='buy(1)'><span id='c1'>10,000원</span></button></div>",
    "<div class='upgrade-card'><div class='upgrade-info'><div class='upgrade-name'>🌶️ 특제 소스 개발</div><div class='upgrade-desc'>단가 상승 (+1,500원/클릭)</div></div><button class='buy-btn' id='b2' onclick='buy(2)'><span id='c2'>30,000원</span></button></div></div></div>",
    "<script>",
    "let money = 0; let power = 1000; let autoIncome = 0; let cost1 = 10000; let cost2 = 30000; let hasHelper = false;",
    "const guests = ['👨‍💼', '👩‍⚕️', '🐱', '🐶', '🦊', '👧'];",
    "function update() {",
    "document.getElementById('m').innerText = money.toLocaleString(); document.getElementById('pow').innerText = power.toLocaleString(); document.getElementById('auto').innerText = autoIncome.toLocaleString();",
    "document.getElementById('c1').innerText = cost1.toLocaleString() + '원'; document.getElementById('c2').innerText = cost2.toLocaleString() + '원';",
    "document.getElementById('b1').disabled = (money < cost1); document.getElementById('b2').disabled = (money < cost2);",
    "if(hasHelper) { document.getElementById('helper-char').style.display = 'block'; }",
    "}",
    "function fry() { money += power; const chef = document.getElementById('chef-char'); chef.style.transform = 'scale(1.3) translateY(-8px)'; setTimeout(function() { chef.style.transform = 'scale(1) translateY(0)'; }, 80); createFloatingText(); update(); }",
    "function createFloatingText() { const screen = document.getElementById('screen'); const text = document.createElement('div'); text.className = 'floating-text'; text.innerText = '+' + power.toLocaleString() + '원'; text.style.left = (20 + Math.random() * 20) + 'px'; text.style.top = (40 + Math.random() * 20) + 'px'; screen.appendChild(text); setTimeout(function() { text.remove(); }, 600); }",
    "function buy(type) { if(type === 1 && money >= cost1) { money -= cost1; autoIncome += 500; cost1 = Math.floor(cost1 * 1.5); hasHelper = true; } else if(type === 2 && money >= cost2) { money -= cost2; power += 1500; cost2 = Math.floor(cost2 * 1.6); } update(); }",
    "setInterval(function() { for(let i=1; i<=4; i++) { const seat = document.getElementById('s' + i); if(Math.random() > 0.45) { const idx = Math.floor(Math.random() * guests.length); seat.innerText = guests[idx] + '🍗'; } else { seat.innerText = '🪑'; } } }, 1800);",
    "setInterval(function() { if(autoIncome > 0) { money += autoIncome; update(); } }, 1000);",
    "update();",
    "</script></body></html>"
]

# 한 줄씩 합쳐서 하나의 깨끗한 HTML로 변환
full_html = "".join(html_lines)

# 3. Streamlit 컴포넌트로 화면에 최종 출력
components.html(full_html, height=580)
