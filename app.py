import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="K-치킨 타이쿤 레스토랑", 
    layout="centered"
)

# 파이썬 들여쓰기 에러(IndentationError)를 원천 차단하기 위해 좌측 정렬로 결합합니다.
h = "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
h += "<style>"
h += "body { font-family: 'Arial', sans-serif; background-color: #1a1a24; text-align: center; padding: 5px; margin: 0; color: #ffffff; user-select: none; }"
h += ".game-container { background: linear-gradient(to bottom, #2c3e50, #1a252f); padding: 15px; border-radius: 20px; border: 4px solid #f39c12; display: inline-block; width: 360px; box-sizing: border-box; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }"
h += ".top-hud { display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.6); padding: 8px 12px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #34495e; }"
h += ".hud-title { color: #f1c40f; font-weight: bold; font-size: 14px; text-shadow: 1px 1px 2px #000; }"
h += ".hud-value { color: #2ecc71; font-weight: bold; font-size: 16px; }"

# 🏪 레스토랑 주방 배경 화면 (진짜 게임 화면처럼 연출)
h += ".restaurant-stage { background: #34495e; border: 3px solid #2c3e50; border-radius: 12px; height: 110px; position: relative; margin-bottom: 12px; overflow: hidden; display: flex; align-items: flex-end; justify-content: center; }"
h += ".customer-zone { position: absolute; top: 15px; width: 100%; display: flex; justify-content: center; gap: 20px; font-size: 28px; }"
h += ".speech-bubble { position: absolute; top: -10px; background: white; color: black; font-size: 11px; font-weight: bold; padding: 3px 6px; border-radius: 8px; border: 2px solid #f1c40f; animation: bounce 0.5s infinite alternate; }"
h += "@keyframes bounce { 0% { transform: translateY(0); } 100% { transform: translateY(-4px); } }"

# 🍳 하단 주방 하이테크 조리대 패널 디자인
h += ".kitchen-counter { background: #7f8c8d; border-top: 4px solid #95a5a6; padding: 10px; border-radius: 0 0 10px 10px; width: 100%; box-sizing: border-box; display: flex; justify-content: space-between; gap: 8px; }"
h += ".cooking-slot { background: #2c3e50; border: 3px solid #bdc3c7; border-radius: 10px; width: 100px; height: 120px; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); transition: transform 0.1s; }"
h += ".cooking-slot:active { transform: scale(0.95); }"
h += ".slot-header { position: absolute; top: 0; width: 100%; background: #bdc3c7; color: #2c3e50; font-size: 10px; font-weight: bold; padding: 2px 0; border-top-left-radius: 5px; border-top-right-radius: 5px; text-align: center; }"

# 🍗 실감나는 요리 재료 및 이펙트 그래픽 이미지 (CSS 스타일링)
h += ".food-graphic { width: 55px; height: 55px; border-radius: 50%; margin-top: 15px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; text-shadow: 1px 1px 1px #000; color: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }"
h += ".g-raw { background: radial-gradient(circle, #ffb3b3, #ff4d4d); border: 2px solid #ff0000; }"
h += ".g-mix { background: radial-gradient(circle, #fff3e0, #ffb74d); border: 2px solid #ff9800; color: #d35400; }"
h += ".g-fry { background: radial-gradient(circle, #f1c40f, #f39c12); border: 2px solid #e67e22; animation: bubble 0.15s infinite alternate; box-shadow: 0 0 15px #f1c40f; }"
h += ".g-done { background: radial-gradient(circle, #e67e22, #d35400); border: 2px solid #962d00; }"
h += ".g-empty { background: rgba(255,255,255,0.05); border: 2px dashed #7f8c8d; color: #7f8c8d; box-shadow: none; }"

h += "@keyframes bubble { 0% { transform: scale(1) translateY(0); } 100% { transform: scale(1.06) translateY(-2px); } }"

# ⏳ 타이쿤 요리 게이지바
h += ".cook-progress { width: 80%; background: #16a085; height: 8px; border-radius: 4px; overflow: hidden; margin-top: 8px; border: 1px solid #111; }"
h += ".cook-fill { height: 100%; width: 0%; background: #2ecc71; transition: width 0.1s linear; }"

# 🛎️ 대형 액션 제어 시스템
h += ".action-bar { margin: 12px 0; }"
h += ".btn-serve { background: linear-gradient(to bottom, #2ecc71, #27ae60); color: white; border: none; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 12px; cursor: pointer; width: 100%; box-shadow: 0 5px #1e7e34; text-shadow: 1px 1px 2px #000; }"
h += ".btn-serve:active { transform: translateY(3px); box-shadow: 0 2px #1e7e34; }"
h += ".btn-serve:disabled { background: #7f8c8d; box-shadow: none; cursor: not-allowed; transform: none; color: #bdc3c7; }"

h += ".upgrade-box { background: rgba(0,0,0,0.4); padding: 10px; border-radius: 10px; border: 1px solid #4f5d73; text-align: left; display: flex; justify-content: space-between; align-items: center; }"
h += ".up-title { font-size: 12px; color: #f1c40f; font-weight: bold; }"
h += ".up-desc { font-size: 10px; color: #bdc3c7; margin-top: 2px; }"
h += ".btn-up { background: #e67e22; color: white; border: none; padding: 8px 12px; font-size: 12px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 3px #b56015; }"
h += ".btn-up:active { transform: translateY(1px); box-shadow: 0 2px #b56015; }"
h += ".btn-up:disabled { background: #555; color: #888; box-shadow: none; cursor: not-allowed; }"
h += "</style></head>"

# 🏢 진짜 오락실 게임 스크린 구조 배치
h += "<body><div class='game-container'>"

# 상단 전광판 (HUD)
h += "<div class='top-hud'>"
h += "<div><span class='hud-title'>SCORE</span><br><span class='hud-value' id='score'>0</span></div>"
h += "<div><span class='hud-title'>REVENUE</span><br><span class='hud-value' id='money'>0 ₩</span></div>"
h += "</div>"

# 무대 스테이지 구역 (손님 등장 대기실)
h += "<div class='restaurant-stage'>"
h += "<div class='customer-zone'>"
h += "<div style='position:relative;'>👨‍💼<div class='speech-bubble' id='order-bubble'>후라이드!</div></div>"
h += "<div>👩‍⚕️</div>"
h += "<div>🦊</div>"
h += "</div>"
h += "</div>"

# 주방 하이테크 조리 기구 패널 구역
h += "<div class='kitchen-counter'>"

# 1번 조리대: 도마 테이블
h += "<div class='cooking-slot' onclick='doPrep()'>"
h += "<div class='slot-header'>1. 원육 준비</div>"
h += "<div id='s1-item' class='food-graphic g-raw'>RAW</div>"
h += "</div>"

# 2번 조리대: 초고온 튀김기
h += "<div class='cooking-slot' onclick='doFry()'>"
h += "<div class='slot-header'>2. 고온 튀김기</div>"
h += "<div id='s2-item' class='food-graphic g-empty'>EMPTY</div>"
h += "<div class='cook-progress'><div class='cook-fill' id='gauge'></div></div>"
h += "</div>"

# 3번 조리대: 완성 가판 도마
h += "<div class='cooking-slot'>"
h += "<div class='slot-header'>3. 출하 도마</div>"
h += "<div id='s3-item' class='food-graphic g-empty'>EMPTY</div>"
h += "</div>"

h += "</div>"

# 서빙용 버튼 인터페이스
h += "<div class='action-bar'>"
h += "<button class='btn-serve' id='serve-btn' onclick='doServe()' disabled>🛎️ 완성된 치킨 손님상에 서빙</button>"
h += "</div>"

# 상점 및 연구 시스템
h += "<div class='upgrade-box'>"
h += "<div><div class='up-title'>⚡ 기가와트 듀얼 튀김기 도입</div><div class='up-desc'>조리 시간이 비약적으로 단축됩니다.</div></div>"
h += "<button class='btn-up' id='up-btn' onclick='buyUpgrade()'><span id='cost'>3,000</span>₩</button>"
h += "</div>"

h += "</div>"

# 🕹️ 무결점 자바스크립트 게임 엔진 소스코드
h += "<script>"
h += "let money = 0;"
h += "let score = 0;"
h += "let state = 'raw';"
h += "let progress = 0;"
h += "let timer = null;"
h += "let speed = 6;"
h += "let upCost = 3000;"
h += "let itemPrice = 3000;"

h += "function updateGameUI() {"
h += "  document.getElementById('money').innerText = money.toLocaleString() + ' ₩';"
h += "  document.getElementById('score').innerText = score.toLocaleString();"
h += "  document.getElementById('cost').innerText = upCost.toLocaleString();"
h += "  document.getElementById('up-btn').disabled = (money < upCost);"
h += "  document.getElementById('serve-btn').disabled = (state !== 'plate');"
h += "}"

h += "function doPrep() {"
h += "  if (state === 'raw') {"
h += "    state = 'mix';"
h += "    let s1 = document.getElementById('s1-item');"
h += "    s1.className = 'food-graphic g-mix';"
h += "    s1.innerText = 'BATTER';"
h += "  }"
h += "}"

h += "function doFry() {"
h += "  if (state === 'mix') {"
h += "    state = 'frying';"
h += "    document.getElementById('s1-item').className = 'food-graphic g-empty';"
h += "    document.getElementById('s1-item').innerText = 'EMPTY';"
h += "    let s2 = document.getElementById('s2-item');"
h += "    s2.className = 'food-graphic g-fry';"
h += "    s2.innerText = 'COOKING';"
h += "    progress = 0;"
h += "    timer = setInterval(function() {"
h += "      progress += speed;"
h += "      if(progress > 100) progress = 100;"
h += "      document.getElementById('gauge').style.width = progress + '%';"
h += "      if(progress >= 100) {"
h += "        clearInterval(timer);"
h += "        state = 'cooked';"
h += "        document.getElementById('s2-item').innerText = 'DONE';"
h += "      }"
h += "    }, 100);"
h += "  } else if (state === 'cooked') {"
h += "    state = 'plate';"
h += "    document.getElementById('s2-item').className = 'food-graphic g-empty';"
h += "    document.getElementById('s2-item').innerText = 'EMPTY';"
h += "    document.getElementById('gauge').style.width = '0%';"
h += "    let s3 = document.getElementById('s3-item');"
h += "    s3.className = 'food-graphic g-done';"
h += "    s3.innerText = 'CRISPY';"
h += "    updateGameUI();"
h += "  }"
h += "}"

h += "function doServe() {"
h += "  if (state === 'plate') {"
h += "    money += itemPrice;"
h += "    score += 150;"
h += "    state = 'raw';"
h += "    let s3 = document.getElementById('s3-item');"
h += "    s3.className = 'food-graphic g-empty';"
h += "    s3.innerText = 'EMPTY';"
h += "    let s1 = document.getElementById('s1-item');"
h += "    s1.className = 'food-graphic g-raw';"
h += "    s1.innerText = 'RAW';"
h += "    updateGameUI();"
  # 파이썬 문자열 결합 도중 들여쓰기가 무너지지 않도록 안전 가드를 배치합니다.
h += "  }"
h += "}"

h += "function buyUpgrade() {"
h += "  if (money >= upCost) {"
h += "    money -= upCost;"
h += "    speed += 5;"
h += "    itemPrice += 1500;"
h += "    upCost = Math.floor(upCost * 2.5);"
h += "    updateGameUI();"
h += "  }"
h += "}"

h += "updateGameUI();"
h += "</script></body></html>"

components.html(h, height=480)
