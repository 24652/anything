import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="K-치킨 레스토랑 타이쿤", 
    layout="centered"
)

# 진짜 오락실/모바일 게임 화면처럼 캔버스 및 레이아웃 설계
h = "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
h += "<style>"
h += "body { font-family: 'Malgun Gothic', sans-serif; "
h += "background-color: #111219; text-align: center; "
h += "padding: 5px; margin: 0; color: #ffffff; user-select: none; }"

# 📱 대형 오락실 게임기 프레임 디자인
h += ".game-container { background: linear-gradient(135deg, #2c3e50, #0f171e); "
h += "padding: 15px; border-radius: 24px; "
h += "border: 5px solid #ff9f43; "
h += "display: inline-block; width: 360px; "
h += "box-sizing: border-box; "
h += "box-shadow: 0 12px 30px rgba(0,0,0,0.7); }"

# 💰 상단 게임 스코어 / 머니 바 디자인
h += ".top-ui-bar { background: rgba(0, 0, 0, 0.4); "
h += "border-radius: 12px; padding: 6px 12px; "
h += "display: flex; justify-content: space-between; "
h += "align-items: center; margin-bottom: 10px; "
h += "border: 1px solid #455a64; }"
h += ".game-title { font-size: 15px; font-weight: bold; color: #ff9f43; "
h += "text-shadow: 1px 1px 2px #000; }"
h += ".money-text { font-size: 20px; font-weight: bold; color: #1dd1a1; "
h += "text-shadow: 1px 1px 3px #000; }"

# 🍳 [메인 그래픽 화면] - 배경 일러스트 효과
h += ".restaurant-screen { "
h += "background: linear-gradient(to bottom, #dff9fb 0%, #c7ecee 40%, #95afc0 41%, #5758bb 100%); "
h += "border: 4px solid #2c3e50; border-radius: 14px; "
h += "height: 180px; position: relative; overflow: hidden; "
h += "box-shadow: inset 0 0 20px rgba(0,0,0,0.5); }"

# 🪟 매장 상단 손님 대기 존
h += ".guest-zone { position: absolute; top: 0; left: 0; width: 100%; "
h += "height: 70px; display: flex; justify-content: center; "
h += "align-items: center; gap: 15px; background: rgba(255,255,255,0.15); "
h += "border-bottom: 3px solid #333; }"
h += ".guest-bubble { background: white; color: #333; "
h += "padding: 4px 8px; border-radius: 10px; font-size: 11px; "
h += "font-weight: bold; position: relative; "
h += "box-shadow: 0 4px 6px rgba(0,0,0,0.2); }"
h += ".guest-bubble::after { content: ''; position: absolute; "
h += "bottom: -6px; left: 50%; margin-left: -6px; "
h += "border-width: 6px 6px 0; border-style: solid; "
h += "border-color: white transparent; display: block; width: 0; }"

# 👨‍🍳 하단 주방 및 리얼 조리 기구 그래픽 디테일
h += ".counter-top { position: absolute; bottom: 0; left: 0; width: 100%; "
h += "height: 105px; background: linear-gradient(to bottom, #7f8c8d, #718093); "
h += "display: flex; justify-content: space-around; align-items: center; "
h += "padding: 0 5px; box-sizing: border-box; }"

h += ".cook-slot { width: 95px; height: 85px; "
h += "background: #353b48; border: 3px solid #2f3640; "
h += "border-radius: 12px; position: relative; cursor: pointer; "
h += "box-shadow: 0 6px 0 #2f3640, inset 0 0 8px #000; "
h += "display: flex; flex-direction: column; "
h += "justify-content: flex-end; align-items: center; "
h += "padding-bottom: 8px; box-sizing: border-box; }"
h += ".cook-slot:active { transform: translateY(4px); box-shadow: 0 2px 0 #2f3640; }"

h += ".slot-name { font-size: 10px; color: #f5f6fa; font-weight: bold; "
h += "position: absolute; top: 2px; width: 100%; text-align: center; "
h += "background: rgba(0,0,0,0.4); padding: 1px 0; border-radius: 4px; }"

# 🍗 실감나는 입체 치킨 에셋 오브젝트 (CSS 아트)
h += ".raw-chicken-asset { width: 38px; height: 26px; "
h += "background: #ffcccc; border-radius: 15px 25px 25px 15px; "
h += "border: 2px solid #ff7675; box-shadow: inset -3px -3px 0 #ff7675; }"

h += ".fryer-oil-asset { width: 44px; height: 34px; "
h += "background: #f1c40f; border-radius: 6px; "
h += "border: 2px solid #d35400; "
h += "box-shadow: inset 0 0 8px #e67e22; "
h += "animation: bubbleEf 0.15s infinite alternate; }"

h += ".cooked-chicken-asset { width: 42px; height: 30px; "
h += "background: linear-gradient(135deg, #e67e22, #d35400); "
h += "border-radius: 20px 10px 20px 10px; "
h += "border: 2px solid #ba4a00; "
h += "box-shadow: 0 4px 6px rgba(0,0,0,0.3), inset -4px -4px 0 #a04000; }"

# 🫧 보글보글 튀김 이펙트 애니메이션
h += "@keyframes bubbleEf { "
h += "  0% { transform: scale(1) translateY(0); background: #f1c40f; }"
h += "  100% { transform: scale(1.06) translateY(-2px); background: #f39c12; }"
h += "}"

# ⏳ 쿠킹 프로그레스 게이지 바
h += ".cook-progress { width: 80%; background: #1e272e; "
h += "height: 8px; border-radius: 4px; overflow: hidden; "
h += "margin-top: 4px; border: 1px solid #718093; }"
h += ".cook-fill { height: 100%; width: 0%; "
h += "background: linear-gradient(to right, #ff9f43, #ff5252); }"

# 🥡 대형 서빙 컨트롤 패널
h += ".control-panel { margin-top: 12px; }"
h += ".serve-mega-btn { "
h += "background: linear-gradient(to bottom, #1dd1a1, #10ac84); "
h += "color: white; border: none; padding: 12px; "
h += "font-size: 16px; font-weight: bold; border-radius: 12px; "
h += "cursor: pointer; width: 100%; box-sizing: border-box; "
h += "box-shadow: 0 5px 0 #10ac84, 0 8px 15px rgba(0,0,0,0.3); "
h += "text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }"
h += ".serve-mega-btn:active { transform: translateY(4px); box-shadow: 0 1px 0 #10ac84; }"
h += ".serve-mega-btn:disabled { background: #718093; box-shadow: none; "
h += "cursor: not-allowed; transform: none; color: #dcdde1; }"

h += ".hint-banner { font-size: 12px; color: #f5f6fa; "
h += "background: #2f3640; padding: 6px; border-radius: 8px; "
h += "margin-bottom: 10px; font-weight: bold; "
h += "border-left: 4px solid #ff9f43; text-align: left; }"

h += ".upgrade-box { background: rgba(0,0,0,0.3); padding: 8px; "
h += "border-radius: 10px; text-align: left; margin-top: 10px; "
h += "border: 1px solid #4b6584; display: flex; "
h += "justify-content: space-between; align-items: center; }"
h += ".up-title { font-size: 11px; color: #dcdde1; font-weight: bold; }"
h += ".up-btn { background: #ff9f43; color: #fff; border: none; "
h += "padding: 6px 12px; font-size: 11px; font-weight: bold; "
h += "border-radius: 6px; cursor: pointer; box-shadow: 0 2px 0 #d35400; }"
h += ".up-btn:disabled { background: #718093; box-shadow: none; cursor: not-allowed; }"
h += "</style></head>"

# 🏪 리얼 주방 시뮬레이터 레이아웃 렌더링
h += "<body><div class='game-container'>"
h += "<div class='top-ui-bar'>"
h += "<div class='game-title'>🏬 명품 치킨 타이쿤</div>"
h += "<div class='money-text'><span id='m-val'>0</span> ₩</div>"
h += "</div>"

h += "<div class='hint-banner' id='guide-bar'>"
h += "📢 안내: 준비대의 생닭 고기를 눌러 반죽하세요!"
h += "</div>"

# 🎮 캔버스형 게임 스크린 무대
h += "<div class='restaurant-screen'>"
h += "<div class='guest-zone'>"
h += "<div class='guest-bubble' id='g-say'>주문: 후라이드 원해요! 🍗</div>"
h += "</div>"

# 카운터 조리대 존
h += "<div class='counter-top'>"

# 슬롯 1: 준비 도마
h += "<div class='cook-slot' onclick='doPrep()'>"
h += "<div class='slot-name'>1. 반죽 준비대</div>"
h += "<div id='s1-asset' class='raw-chicken-asset'></div>"
h += "</div>"

# 슬롯 2: 고압 튀김기
h += "<div class='cook-slot' onclick='doFry()'>"
h += "<div class='slot-name'>2. 고온 튀김기</div>"
h += "<div id='s2-asset' style='display:none;'></div>"
h += "<div class='cook-progress'><div class='cook-fill' id='p-bar'></div></div>"
h += "</div>"

# 슬롯 3: 가판대 접시
h += "<div class='cook-slot'>"
h += "<div class='slot-name'>3. 포장대</div>"
h += "<div id='s3-asset' style='display:none;'></div>"
h += "</div>"

h += "</div></div>"

# 서빙 및 강화 컨트롤러
h += "<div class='control-panel'>"
h += "<button class='serve-mega-btn' id='srv-btn' "
h += "onclick='doServe()' disabled>🥡 손님 테이블로 서빙 전송</button>"
h += "<div class='upgrade-box'>"
h += "<div><div class='up-title'>🔥 디지털 자동 튀김기 커스텀</div>"
h += "<div style='font-size:9px; color:#a5b1c2;'>조리속도가 폭발적으로 상승합니다.</div></div>"
h += "<button class='up-btn' id='u-btn' onclick='doUpgrade()'>"
h += "<span id='u-cost'>3,000</span>₩</button>"
h += "</div></div></div>"

# 🕹️ 고성능 자바스크립트 게임 루프 엔진
h += "<script>"
h += "let money = 0;"
h += "let state = 'raw'; " # raw -> battered -> frying -> cooked -> plate
h += "let progress = 0;"
h += "let timer = null;"
h += "let speed = 6;"
h += "let upCost = 3000;"
h += "let price = 3500;"

h += "function log(txt) { "
h += "  document.getElementById('guide-bar').innerText = '📢 안내: ' + txt; "
h += "}"

h += "function refresh() {"
h += "  document.getElementById('m-val').innerText = money.toLocaleString();"
h += "  document.getElementById('u-cost').innerText = upCost.toLocaleString();"
h += "  document.getElementById('u-btn').disabled = (money < upCost);"
h += "  document.getElementById('srv-btn').disabled = (state !== 'plate');"
h += "}"

h += "function doPrep() {"
h += "  if(state === 'raw') {"
h += "    state = 'battered';"
h += "    let a1 = document.getElementById('s1-asset');"
h += "    a1.style.background = '#fff4e6';"
h += "    a1.style.borderColor = '#f5b041';"
h += "    log('튀김옷 반죽이 완료되었습니다! 2번 튀김기로 옮기세요.');"
h += "  }"
h += "}"

h += "function doFry() {"
h += "  if(state === 'battered') {"
h += "    state = 'frying';"
h += "    document.getElementById('s1-asset').style.display = 'none';"
h += "    let a2 = document.getElementById('s2-asset');"
h += "    a2.style.display = 'block';"
h += "    a2.className = 'fryer-oil-asset';"
h += "    log('지글지글! 기름 온도가 오르고 치킨이 맛있게 튀겨집니다!');"
h += "    progress = 0;"
h += "    "
h += "    timer = setInterval(function() {"
h += "      progress += speed;"
h += "      if(progress > 100) progress = 100;"
h += "      document.getElementById('p-bar').style.width = progress + '%';"
h += "      "
h += "      if(progress >= 100) {"
h += "        clearInterval(timer);"
h += "        state = 'cooked';"
h += "        document.getElementById('s2-asset').className = 'cooked-chicken-asset';"
h += "        log('노릇노릇 완벽히 익었습니다! 클릭하여 3번 포장대로 옮기세요!');"
h += "      }"
h += "    }, 100);"
h += "  } else if(state === 'cooked') {"
h += "    state = 'plate';"
h += "    document.getElementById('s2-asset').style.display = 'none';"
h += "    document.getElementById('p-bar').style.width = '0%';"
h += "    let a3 = document.getElementById('s3-asset');"
h += "    a3.style.display = 'block';"
h += "    a3.className = 'cooked-chicken-asset';"
h += "    log('최종 포장대에 세팅되었습니다! 대형 서빙 버튼을 터치하세요!');"
h += "    refresh();"
h += "  }"
h += "}"

h += "function doServe() {"
h += "  if(state === 'plate') {"
h += "    money += price;"
h += "    state = 'raw';"
h += "    document.getElementById('s3-asset').style.display = 'none';"
h += "    let a1 = document.getElementById('s1-asset');"
h += "    a1.style.display = 'block';"
h += "    a1.style.background = '#ffcccc';"
h += "    a1.style.borderColor = '#ff7675';"
h += "    document.getElementById('g-say').innerText = '감사합니다! 정말 바삭해요! ✨';"
h += "    log('판매 성공! 단가 ' + price.toLocaleString() + '원 정산 완료. 다음 닭을 요리하세요!');"
h += "    setTimeout(function() { "
h += "       document.getElementById('g-say').innerText = '주문: 후라이드 원해요! 🍗'; "
h += "    }, 1500);"
h += "    refresh();"
  "  }"
h += "}"

h += "function doUpgrade() {"
h += "  if(money >= upCost) {"
h += "    money -= upCost;"
h += "    speed += 5;"
h += "    price += 1500;"
h += "    upCost = Math.floor(upCost * 2.1);"
h += "    log('주방 하이테크 화력 업그레이드 완료! 조리 속도 대폭 증가!');"
h += "    refresh();"
h += "  }"
h += "}"

h += "refresh();"
h += "</script></body></html>"

components.html(h, height=520)
