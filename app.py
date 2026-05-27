import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="K-치킨 타이쿤: 레트로 픽셀 매장", layout="centered")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pixel Chicken Tycoon</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #2c3e50; text-align: center; padding: 20px; margin: 0; color: #fff; }
        .game-wrapper { background: #34495e; padding: 20px; border-radius: 15px; border: 4px solid #bdc3c7; display: inline-block; width: 400px; }
        h1 { color: #f1c40f; margin: 0 0 5px 0; font-size: 24px; text-shadow: 2px 2px #d35400; }
        
        /* 🏪 이미지 속 레트로 매장 구현 구역 */
        .game-screen { 
            background-color: #edf2f7; 
            border: 4px solid #2c3e50; 
            border-radius: 10px; 
            height: 180px; 
            margin: 15px 0; 
            position: relative;
            overflow: hidden;
        }
        
        /* 주방 구역 인테리어 */
        .kitchen-zone {
            position: absolute; left: 0; top: 0; width: 100px; height: 100%;
            background-color: #cbd5e0; border-right: 3px dashed #4a5568;
        }
        .kitchen-title { font-size: 10px; color: #4a5568; font-weight: bold; margin-top: 5px; }
        
        /* 홀(테이블) 구역 인테리어 */
        .hall-zone { position: absolute; right: 0; top: 0; width: 290px; height: 100%; }
        
        /* 움직이는 도트 캐릭터들 */
        .sprite { position: absolute; font-size: 28px; transition: all 0.5s ease; }
        .chef { left: 30px; top: 70px; }
        .helper { left: 30px; top: 120px; display: none; }
        
        /* 손님 테이블 좌석 */
        .table-seat { position: absolute; font-size: 24px; }
        .seat1 { right: 180px; top: 40px; }
        .seat2 { right: 70px; top: 40px; }
        .seat3 { right: 180px; top: 110px; }
        .seat4 { right: 70px; top: 110px; }
        
        /* 게임 UI 디자인 */
        .money-display { font-size: 24px; font-weight: bold; color: #2ecc71; margin: 10px 0; text-shadow: 1px 1px #27ae60; }
        .stats { font-size: 12px; color: #bdc3c7; margin-bottom: 15px; }
        
        /* 플레이 튀기기 버튼 */
        .fry-btn {
            background-color: #e67e22; color: white; border: none; padding: 12px 30px;
            font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer;
            border-bottom: 4px solid #d35400; box-shadow: 0 4px #2c3e50; outline: none;
        }
        .fry-btn:active { border-bottom: 1px solid #d35400; transform: translateY(3px); box-shadow: 0 1px #2c3e50; }
        
        /* 업그레이드 슬롯 */
        .shop-section { margin-top: 20px; text-align: left; }
        .shop-title { font-size: 14px; color: #f1c40f; margin-bottom: 8px; }
        .upgrade-card { 
            background: #2c3e50; padding: 10px; margin: 6px 0; border-radius: 8px;
            display: flex; justify-content: space-between; align-items: center; border: 1px solid #455a64;
        }
        .upgrade-info { font-size: 12px; }
        .upgrade-name { font-weight: bold; color: #fff; margin-bottom: 2px; }
        .upgrade-desc { color: #95a5a6; font-size: 11px; }
        .buy-btn { 
            background-color: #2ecc71; color: white; border: none; padding: 8px 12px;
            font-size: 12px; font-weight: bold; border-radius: 5px; cursor: pointer;
        }
        .buy-btn:disabled { background-color: #7f8c8d; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="game-wrapper">
        <h1>👾 PIXEL CHICKEN</h1>
        
        <div class="game-screen">
            <div class="kitchen-zone">
                <div class="kitchen-title">KITCHEN</div>
                <div class="sprite chef" id="chef-char">👨‍🍳</div>
                <div class="sprite helper" id="helper-char">🧑‍🍳</div>
            </div>
            
            <div class="hall-zone">
                <div class="table-seat seat1" id="s1">🪑</div>
                <div class="table-seat seat2" id="s2">🪑</div>
                <div class="table-seat seat3" id="s3">🪑</div>
                <div class="table-seat seat4" id="s4">🪑</div>
            </div>
        </div>

        <div class="money-display"><span id="m">0</span> ₩</div>
        <div class="stats">클릭 파워: <span id="pow">1,000</span> | 자동 초당 수익: <span id="auto">0</span></div>
        
        <button class="fry-btn" onclick="fry()">🍗 치킨 튀기기!</button>
        
        <div class="shop-section">
            <div class="shop-title">🛒 SHOP (매장 관리)</div>
            
            <div class="upgrade-card">
                <div class="upgrade-info">
                    <div class="upgrade-name">🧑‍🍳 주방 조수 고용</div>
                    <div class="upgrade-desc">자동으로 초당 +500원 벌기</div>
                </div>
                <button class="buy-btn" id="b1" onclick="buy(1)"><span id="c1">10,000</span>원</button>
            </div>

            <div class="upgrade-card">
                <div class="upgrade-info">
                    <div class="upgrade-name">🪑 테이블 확장 (홀 업그레이드)</div>
                    <div class="upgrade-desc">손님이 더 많이 찾아옵니다 (+자동 2,000원)</div>
                </div>
                <button class="buy-btn" id="b2" onclick="buy(2)"><span id="c2">40,000</span>원</button>
            </div>
        </div>
    </div>

    <script>
        let money = 0; let power = 1000; let autoIncome = 0;
        let cost1 = 10000; let cost2 = 40000;
        
        let hasHelper = false;
        let tableLevel = 0;
        
        // 손님 이모지 후보 리스트
        const guests = ["🙋‍♂️", "🙋🏼‍♀️", "🐱", "🐶", "🧔", "👧"];

        function update() {
            document.getElementById('m').innerText = money.toLocaleString();
            document.getElementById('pow').innerText = power.toLocaleString();
            document.getElementById('auto').innerText = autoIncome.toLocaleString();
            document.getElementById('c1').innerText = cost1.toLocaleString();
            document.getElementById('c2').innerText = cost2.toLocaleString();
            
            document.getElementById('b1').disabled = (money < cost1);
            document.getElementById('b2').disabled = (money < cost2);

            // 주방 조수 고용 시 주방에 🧑‍🍳 캐릭터 등장
            if(hasHelper) {
                document.getElementById('helper-char').style.display = 'block';
            }
        }

        // 치킨 튀기기 (클릭 이벤트)
        function fry() {
            money += power;
            
            // 클릭할 때마다 주방장👨‍🍳이 들썩거리며 역동적으로 일하는 모션 효과
            const chef = document.getElementById('chef-char');
            chef.style.transform = 'scale(1.3) translateY(-10px)';
            setTimeout(() => { chef.style.transform = 'scale(1) translateY(0)'; }, 100);
            
            update();
        }

        // 업그레이드 구매
        function buy(type) {
            if(type === 1 && money >= cost1) {
                money -= cost1; autoIncome += 500; cost1 = Math.floor(cost1 * 1.6);
                hasHelper = true;
            } else if(type === 2 && money >= cost2) {
                money -= cost2; autoIncome += 2000; power += 1500; cost2 = Math.floor(cost2 * 1.8);
                tableLevel++;
            }
            update();
        }

        // [시각 효과 연출] 2초마다 손님들이 매장에 들어왔다 나갔다 자리가 교체됨!
        setInterval(function() {
            for(let i=1; i<=4; i++) {
                const seat = document.getElementById('s' + i);
                // 랜덤 확률로 손님이 자리에 앉거나 다 먹고 떠나
