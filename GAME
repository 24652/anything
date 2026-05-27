import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (반드시 코드의 최상단에 위치해야 합니다)
st.set_page_config(page_title="K-치킨 타이쿤", layout="centered")

# 2. 게임 본문 HTML
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chicken Tycoon</title>
    <style>
        body { font-family: sans-serif; background-color: #f8f9fa; text-align: center; padding: 20px; margin: 0; }
        .box { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: inline-block; width: 320px; }
        h1 { color: #ff6b6b; margin: 0 0 10px 0; font-size: 24px; }
        .money-text { font-size: 18px; font-weight: bold; margin: 10px 0; }
        .btn-click { font-size: 50px; background: none; border: none; cursor: pointer; transition: transform 0.1s; outline: none; }
        .btn-click:active { transform: scale(0.9); }
        .up-btn { width: 100%; padding: 10px; margin: 5px 0; background-color: #4dabf7; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; display: flex; justify-content: space-between; }
        .up-btn:disabled { background-color: #ced4da; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🍗 K-치킨 타이쿤</h1>
        <div class="money-text">자산: <span id="m">0</span>원</div>
        <div style="font-size:12px; color:#666; margin-bottom:10px;">초당 자동 수익: <span id="ai">0</span>원</div>
        
        <button class="btn-click" onclick="ck()">🍗</button>
        <div style="font-size:11px; color:#aaa;">치킨을 눌러 돈을 버세요!</div>
        
        <div style="margin-top:20px; text-align:left;">
            <b style="font-size:14px;">🏪 업그레이드</b>
            <button class="up-btn" id="b1" onclick="buy(1)"><span>👨‍🍳 알바 고용 (+500원/초)</span><span id="c1">10,000원</span></button>
            <button class="up-btn" id="b2" onclick="buy(2)"><span>🌶️ 양념 개발 (+2,000원/클릭)</span><span id="c2">30,000원</span></button>
        </div>
    </div>
    <script>
        let money = 0; let power = 1000; let auto = 0;
        let cost1 = 10000; let cost2 = 30000;
        function up() {
            document.getElementById('m').innerText = money.toLocaleString();
            document.getElementById('ai').innerText = auto.toLocaleString();
            document.getElementById('c1').innerText = cost1.toLocaleString() + "원";
            document.getElementById('c2').innerText = cost2.toLocaleString() + "원";
            document.getElementById('b1').disabled = (money < cost1);
            document.getElementById('b2').disabled = (money < cost2);
        }
        function ck() { money += power; up(); }
        function buy(t) {
            if(t===1 && money>=cost1) { money-=cost1; auto+=500; cost1=Math.floor(cost1*1.5); }
            else if(t===2 && money>=cost2) { money-=cost2; power+=2000; cost2=Math.floor(cost2*1.7); }
            up();
        }
        setInterval(function() { if(auto>0) { money+=auto; up(); } }, 1000);
        up();
    </script>
</body>
</html>
"""

# 3. Streamlit에 안전하게 로드
components.html(game_html, height=500)
