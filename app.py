import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="K-치킨 타이쿤 Master", layout="centered")

# 코드가 잘리지 않도록 아주 짧은 단위로 안전하게 나누었습니다.
html_lines = [
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
    "<style>",
    "body { font-family: sans-serif; background-color: #1a1a24; text-align: center; padding: 5px; margin: 0; color: #ffffff; }",
    ".game-wrapper { background: #252632; padding: 12px; border-radius: 16px; border: 3px solid #3b3d54; display: inline-block; width: 330px; box-sizing: border-box; }",
    "h1 { color: #ffd43b; margin: 0; font-size: 20px; text-shadow: 2px 2px 0px #e67e22; }",
    ".sub-text { font-size: 10px; color: #a6a7b7; margin-bottom: 8px; }",
    ".game-screen { background-color: #f1f3f5; border: 3px solid #1a1a24; border-radius: 10px; height: 140px; margin: 8px 0; position: relative; overflow: hidden; }",
    ".kitchen-zone { position: absolute; left: 0; top: 0; width: 80px; height: 100%; background-color: #dee2e6; border-right: 3px dashed #495057; }",
    ".kitchen-title { font-size: 10px; color: #495057; font-weight: bold; margin-top: 3px; background: #ced4da; padding: 1px 0; }",
    ".hall-zone { position: absolute; right: 0; top: 0; width: 240px; height: 100%; background-color: #e9ecef; }",
    ".sprite { position: absolute; font-size: 26px; transition: transform 0.08s ease; }",
    ".chef { left: 20px; top: 35px; }",import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="K-치킨 요리 타이쿤", layout="centered")

html_lines = [
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
    "<style>",
    "body { font-family: sans-serif; background-color: #1a1a24; text-align: center; padding: 5px; margin: 0; color: #ffffff; user-select: none; }",
    ".game-wrapper { background: #252632; padding: 12px; border-radius: 16px; border: 3px solid #3b3d54; display: inline-block; width: 340px; box-sizing: border-box; }",
    "h1 { color: #ffd43b; margin: 0; font-size: 20px; text-shadow: 2px 2px 0px #e67e22; }",
    ".money-display { font-size: 24px; font-weight: bold; color: #51cf66; margin: 8px 0; text-shadow: 1px 1px 0px #2b8a3e; }",
    
    # 🍳 주방 조리대 그래픽 존
    ".kitchen-board { background-color: #ced4da; border: 3px solid #1a1a24; border-radius: 10px; padding: 8px; margin: 10px 0; display: flex; justify-content: space-around; }",
    ".zone { background: #adb5bd; border: 2px solid #495057; border-radius: 8px; width: 90px; height: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; cursor: pointer; }",
    ".zone-title { font-size: 11px; font-weight: bold; color: #212529; margin-bottom: 5px; background: #e9ecef; width: 100%; position: absolute; top: 0; border-top-left-radius: 5px; border-top-right-radius: 5px; }",
    ".item-display { font-size: 36px; margin-top: 15px; transition: transform 0.1s; }",
    ".zone:active .item-display { transform: scale(1.2); }",
    
    # ⏳ 진행 상태바 CSS
    ".progress-bar { width: 80%; background-color: #e9ecef; height: 8px; border-radius: 4px; overflow: hidden; margin-top: 8px; border: 1px solid #495057; }",
    ".progress-fill { height: 100%; width: 0%; background-color: #f76707; transition: width 0.1s linear; }",
    
    # 🛒 하단 서빙 및 업그레이드 구역
    ".serve-btn { background-color: #37b24d; color: white; border: none; padding: 10px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; border-bottom: 4px solid #2b8a3e; width: 100%; box-sizing: border-box; margin-bottom: 8px; }",
    ".serve-btn:active { border-bottom: 1px solid #2b8a3e; transform: translateY(3px); }",
    ".serve-btn:disabled { background-color: #495057; border-bottom: none; cursor: not-allowed; transform: none; }",
    ".status-msg { font-size: 12px; color: #ffd43b; min-height: 18px; margin-bottom: 5px; font-weight: bold; }",
    ".shop-section { background: #1c1c24; padding: 8px; border-radius: 8px; text-align: left; border: 1px solid #3b3d54; }",
    ".shop-title { font-size: 12px; color: #ffd43b; font-weight: bold; margin-bottom: 4px; }",
    ".upgrade-text { font-size: 11px; color: #adc5dc; display: flex; justify-content: space-between; align-items: center; }",
    ".buy-btn { background-color: #fd7e14; color: white; border: none; padding: 4px 8px; font-size: 10px; font-weight: bold; border-radius: 4px; cursor: pointer; }",
    ".buy-btn:disabled { background-color: #495057; color: #868e96; cursor: not-allowed; }",
    "</style></head>",
    
    "<body><div class='game-wrapper'>",
    "<h1>🍳 K-치킨 요리사</h1>",
    "<div class='money-display'><span id='money'>0</span> ₩</div>",
    "<div class='status-msg' id='msg'>생닭을 터치하여 반죽을 묻히세요!</div>",
    
    # 🏪 3단계 리얼 조리대 시스템
    "<div class='kitchen-board'>",
    
    # 1단계: 준비 구역 (생닭 -> 반죽고기)
    "<div class='zone' onclick='clickPrep()'>",
    "<div class='zone-title'>1. 준비대</div>",
    "<div class='item-display' id='prep-item'>🍗</div>",
    "</div>",
    
    # 2단계: 튀김기 구역 (기름에 튀기기 진행)
    "<div class='zone' onclick='clickFry()'>",
    "<div class='zone-title'>2. 튀김기</div>",
    "<div class='item-display' id='fry-item'>❔</div>",
    "<div class='progress-bar'><div class='progress-fill' id='bar'></div></div>",
    "</div>",
    
    # 3단계: 가판대 구역 (완성된 치킨 보관)
    "<div class='zone'>",
    "<div class='zone-title'>3. 접시</div>",
    "<div class='item-display' id='plate-item'>🪹</div>",
    "</div>",
    
    "</div>",
    
    # 서빙 완료 버튼 및 업그레이드 상점
    "<button class='serve-btn' id='serve' onclick='serveChicken()' disabled>🥡 손님에게 서빙하기</button>",
    "<div class='shop-section'>",
    "<div class='shop-title'>⚙️ 기술 연구소</div>",
    "<div class='upgrade-text'>",
    "<span>🔥 강력한 튀김기 (튀김 속도 단축)</span>",
    "<button class='buy-btn' id='up-btn' onclick='upgradeFry()'>연구비: <span id='cost'>3,000</span>원</button>",
    "</div></div>",
    
    "</div>",
    
    "<script>",
    # 내부 게임 데이터 스크립트
    "let money = 0;",
    "let chickenState = 'raw'; ", # raw(생닭) -> battered(반죽) -> frying(튀기는중) -> cooked(완성) -> plate(접시)
    "let fryProgress = 0;",
    "let fryInterval = null;",
    "let frySpeed = 5; ", # 기본 튀김 속도
    "let upgradeCost = 3000;",
    "let chickenPrice = 2500;",
    
    "function msg(t) { document.getElementById('msg').innerText = t; }",
    
    "function updateUI() {",
    "  document.getElementById('money').innerText = money.toLocaleString();",
    "  document.getElementById('cost').innerText = upgradeCost.toLocaleString();",
    "  document.getElementById('up-btn').disabled = (money < upgradeCost);",
    "  document.getElementById('serve').disabled = (chickenState !== 'plate');",
    "}",
    
    # 1. 준비대 마우스 클릭 액션
    "function clickPrep() {",
    "  if (chickenState === 'raw') {",
    "    chickenState = 'battered';",
    "    document.getElementById('prep-item').innerText = '🥣';",
    "    msg('반죽 완료! 2번 튀금기로 옮겨서 튀기세요.');",
    "  }",
    "}",
    
    # 2. 튀김기 마우스 클릭 액션
    "function clickFry() {",
    "  if (chickenState === 'battered') {",
    "    chickenState = 'frying';",
    "    document.getElementById('prep-item').innerText = '🪹';",
    "    document.getElementById('fry-item').innerText = '🫧';",
    "    msg('치킨이 노릇하게 튀겨지는 중입니다...');",
    "    fryProgress = 0;",
    "    ",
    "    fryInterval = setInterval(function() {",
    "      fryProgress += frySpeed;",
    "      if (fryProgress > 100) { fryProgress = 100; }",
    "      document.getElementById('bar').style.width = fryProgress + '%';",
    "      ",
    "      if (fryProgress >= 100) {",
    "        clearInterval(fryInterval);",
    "        chickenState = 'cooked';",
    "        document.getElementById('fry-item').innerText = '✨';",
    "        msg('바삭하게 완성! 튀김기를 클릭해 접시로 옮기세요.');",
    "      }",
    "    }, 100);",
    "  } else if (chickenState === 'cooked') {",
    "    chickenState = 'plate';",
    "    document.getElementById('fry-item').innerText = '❔';",
    "    document.getElementById('bar').style.width = '0%';",
    "    document.getElementById('plate-item').innerText = '🍗';",
    "    msg('접시에 담겼습니다! 서빙 버튼을 눌러 판매하세요.');",
    "    updateUI();",
    "  }",
    "}",
    
    # 3. 서빙 및 정산 버튼 액션
    "function serveChicken() {",
    "  if (chickenState === 'plate') {",
    "    money += chickenPrice;",
    "    chickenState = 'raw';",
    "    document.getElementById('plate-item').innerText = '🪹';",
    "    document.getElementById('prep-item').innerText = '🍗';",
    "    msg('치킨 배달 완료! (+ ' + chickenPrice.toLocaleString() + '원) 다음 닭을 준비하세요.');",
    "    updateUI();",
    "  }",
    "}",
    
    # 4. 튀김기 업그레이드 상점 기능
    "function upgradeFry() {",
    "  if (money >= upgradeCost) {",
    "    money -= upgradeCost;",
    "    frySpeed += 3;",
    "    chickenPrice += 1000;",
    "    upgradeCost = Math.floor(upgradeCost * 2.2);",
    "    msg('튀김기 화력 강화 성공! 튀김 속도 및 판매 단가 상승!');",
    "    updateUI();",
    "  }",
    "}",
    
    "updateUI();",
    "</script></body></html>"
]

full_html = "".join(html_lines)
components.html(full_html, height=450)
    ".seat2 { right: 30px; top: 20px; }",
    ".seat3 { right: 130px; top: 75px; }",
    ".seat4 { right: 30px; top: 75px; }",
    ".money-display { font-size: 22px; font-weight: bold; color: #51cf66; margin: 5px 0; text-shadow: 1px 1px 0px #2b8a3e; }",
    ".stats { font-size: 11px; color: #adc5dc; margin-bottom: 8px; background: #1c1c24; padding: 4px; border-radius: 6px; display: flex; justify-content: space-around; }",
    ".fry-btn { background-color: #f76707; color: white; border: none; padding: 10px; font-size: 15px; font-weight: bold; border-radius: 10px; cursor: pointer; border-bottom: 4px solid #d9480f; box-shadow: 0 3px #1a1a24; outline: none; width: 100%; box-sizing: border-box; }",
    ".fry-btn:active { border-bottom: 1px solid #d9480f; transform: translateY(3px); box-shadow: 0 1px #1a1a24; }",
    ".shop-section { margin-top: 12px; text-align: left; }",
    ".shop-title { font-size: 12px; color: #ffd43b; margin-bottom: 4px; font-weight: bold; }",
    ".upgrade-card { background: #1c1c24; padding: 6px 10px; margin: 4px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #3b3d54; }",
    ".upgrade-info { width: 65%; }",
    ".upgrade-name { font-weight: bold; color: #ffffff; font-size: 11px; }",
    ".upgrade-desc { color: #868e96; font-size: 9px; }",
    ".buy-btn { background-color: #37b24d; color: white; border: none; padding: 6px 10px; font-size: 11px; font-weight: bold; border-radius: 5px; cursor: pointer; }",
    ".buy-btn:disabled { background-color: #495057; color: #868e96; cursor: not-allowed; }",
    "@keyframes floatUp { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(-30px); opacity: 0; } }",
    ".floating-text { position: absolute; color: #40c057; font-weight: bold; font-size: 14px; animation: floatUp 0.6s ease-out forwards; pointer-events: none; z-index: 10; }",
    "</style></head>",
    "<body><div class='game-wrapper'><h1>🍗 타이쿤 마스터</h1><div class='sub-text'>레트로 도트 치킨 가게</div>",
    "<div class='game-screen' id='screen'><div class='kitchen-zone'><div class='kitchen-title'>주방</div><div class='sprite chef' id='chef-char'>👨‍🍳</div><div class='sprite helper' id='helper-char'>🧑‍🍳</div></div>",
    "<div class='hall-zone'><div class='table-seat seat1' id='s1'>🪑</div><div class='table-seat seat2' id='s2'>🪑</div><div class='table-seat seat3' id='s3'>🪑</div><div class='table-seat seat4' id='s4'>🪑</div></div></div>",
    "<div class='money-display'><span id='m'>0</span> ₩</div>",
    "<div class='stats'><div>🖱️ 클릭: <span id='pow'>1,000</span></div><div>⏰ 초당: <span id='auto'>0</span></div></div>",
    "<button class='fry-btn' onclick='fry()'>🍗 치킨 튀겨서 서빙하기!</button>",
    "<div class='shop-section'><div class='shop-title'>🛒 업그레이드 상점</div>",
    "<div class='upgrade-card'><div class='upgrade-info'><div class='upgrade-name'>🧑‍🍳 주방 알바 고용</div><div class='upgrade-desc'>자동 튀기기 (초당 +500)</div></div><button class='buy-btn' id='b1' onclick='buy(1)'><span id='c1'>10,000원</span></button></div>",
    "<div class='upgrade-card'><div class='upgrade-info'><div class='upgrade-name'>🌶️ 특제 소스 개발</div><div class='upgrade-desc'>단가 상승 (+1,500/클릭)</div></div><button class='buy-btn' id='b2' onclick='buy(2)'><span id='c2'>30,000원</span></button></div></div></div>",
    "<script>",
    "let money = 0; let power = 1000; let autoIncome = 0; let cost1 = 10000; let cost2 = 30000; let hasHelper = false;",
    "const guests = ['👨‍💼', '👩‍⚕️', '🐱', '🐶', '🦊', '👧'];",
    "function update() {",
    "document.getElementById('m').innerText = money.toLocaleString();",
    "document.getElementById('pow').innerText = power.toLocaleString();",
    "document.getElementById('auto').innerText = autoIncome.toLocaleString();",
    "document.getElementById('c1').innerText = cost1.toLocaleString() + '원';",
    "document.getElementById('c2').innerText = cost2.toLocaleString() + '원';",
    "document.getElementById('b1').disabled = (money < cost1);",
    "document.getElementById('b2').disabled = (money < cost2);",
    "if(hasHelper) { document.getElementById('helper-char').style.display = 'block'; }",
    "}",
    "function fry() {",
    "  money += power;",
    "  const chef = document.getElementById('chef-char');",
    "  chef.style.transform = 'scale(1.2) translateY(-5px)';",
    "  setTimeout(function() { chef.style.transform = 'scale(1) translateY(0)'; }, 80);",
    "  createFloatingText();",
    "  update();",
    "}",
    "function createFloatingText() {",
    "  const screen = document.getElementById('screen');",
    "  const text = document.createElement('div');",
    "  text.className = 'floating-text';",
    "  text.innerText = '+' + power.toLocaleString() + '원';",
    "  text.style.left = (15 + Math.random() * 15) + 'px';",
    "  text.style.top = (30 + Math.random() * 15) + 'px';",
    "  screen.appendChild(text);",
    "  setTimeout(function() { text.remove(); }, 600);",
    "}",
    "function buy(type) {",
    "  if(type === 1 && money >= cost1) {",
    "    money -= cost1; autoIncome += 500; cost1 = Math.floor(cost1 * 1.5); hasHelper = true;",
    "  } else if(type === 2 && money >= cost2) {",
    "    money -= cost2; power += 1500; cost2 = Math.floor(cost2 * 1.6);",
    "  }",
    "  update();",
    "}",
    "setInterval(function() {",
    "  for(let i=1; i<=4; i++) {",
    "    const seat = document.getElementById('s' + i);",
    "    if(Math.random() > 0.45) {",
    "      const idx = Math.floor(Math.random() * guests.length);",
    "      seat.innerText = guests[idx] + '🍗';",
    "    } else { seat.innerText = '🪑'; }",
    "  }",
    "}, 1800);",
    "setInterval(function() { if(autoIncome > 0) { money += autoIncome; update(); } }, 1000);",
    "update();",
    "</script></body></html>"
]

full_html = "".join(html_lines)
components.html(full_html, height=480)
