<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixel Chicken Tycoon Master</title>
    <style>
        body { 
            font-family: 'Malgun Gothic', sans-serif; 
            background-color: #1a1a24; 
            text-align: center; 
            padding: 20px; 
            margin: 0; 
            color: #ffffff; 
        }
        .game-wrapper { 
            background: #252632; 
            padding: 25px; 
            border-radius: 20px; 
            border: 4px solid #3b3d54; 
            display: inline-block; 
            width: 360px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        }
        h1 { 
            color: #ffd43b; 
            margin: 0 0 5px 0; 
            font-size: 26px; 
            text-shadow: 3px 3px 0px #e67e22; 
            letter-spacing: 1px;
        }
        .sub-title {
            font-size: 12px;
            color: #a6a7b7;
            margin-bottom: 15px;
        }
        
        /* 🏪 도트 그래픽 게임 화면 스크린 */
        .game-screen { 
            background-color: #f1f3f5; 
            border: 4px solid #1a1a24; 
            border-radius: 12px; 
            height: 190px; 
            margin: 15px 0; 
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
        }
        
        /* 주방 인테리어 */
        .kitchen-zone {
            position: absolute; left: 0; top: 0; width: 95px; height: 100%;
            background-color: #dee2e6; border-right: 4px dashed #495057;
        }
        .kitchen-title { 
            font-size: 11px; 
            color: #495057; 
            font-weight: bold; 
            margin-top: 6px; 
            background: #ced4da;
            padding: 2px 0;
        }
        
        /* 홀(테이블) 인테리어 */
        .hall-zone { position: absolute; right: 0; top: 0; width: 255px; height: 100%; background-color: #e9ecef;}
        .hall-title { font-size: 11px; color: #495057; font-weight: bold; margin-top: 6px; text-align: right; margin-right: 15px;}

        /* 애니메이션 캐릭터 스프라이트 */
        .sprite { position: absolute; font-size: 32px; transition: transform 0.08s ease; }
        .chef { left: 25px; top: 55px; }
        .helper { left: 25px; top: 115px; display: none; }
        
        /* 테이블 좌석 배치 */
        .table-seat { position: absolute; font-size: 26px; width: 50px; height: 50px; text-align: center; line-height: 50px; transition: all 0.2s; }
        .seat1 { right: 150px; top: 40px; }
        .seat2 { right: 40px; top: 40px; }
        .seat3 { right: 150px; top: 110px; }
        .seat4 { right: 40px; top: 110px; }
        
        /* 게임 스펙 스코어보드 UI */
        .money-display { font-size: 28px; font-weight: bold; color: #51cf66; margin: 15px 0 5px 0; text-shadow: 2px 2px 0px #2b8a3e; }
        .stats { font-size: 12px; color: #adc5dc; margin-bottom: 20px; background: #1c1c24; padding: 8px; border-radius: 8px; display: flex; justify-content: space-around;}
        
        /* 메인 치킨 액션 버튼 */
        .fry-btn {
            background-color: #f76707; color: white; border: none; padding: 14px 40px;
            font-size: 18px; font-weight: bold; border-radius: 12px; cursor: pointer;
            border-bottom: 5px solid #d9480f; box-shadow: 0 5px #1a1a24; outline: none;
            width: 100%; box-sizing: border-box; transition: all 0.05s;
        }
        .fry-btn:active { border-bottom: 1px solid #d9480f; transform: translateY(4px); box-shadow: 0 1px #1a1a24; }
        
        /* 업그레이드 샵 */
        .shop-section { margin-top: 25px; text-align: left; }
        .shop-title { font-size: 15px; color: #ffd43b; margin-bottom: 10px; font-weight: bold; border-left: 4px solid #ffd43b; padding-left: 8px;}
        .upgrade-card { 
            background: #1c1c24; padding: 12px; margin: 8px 0; border-radius: 10px;
            display: flex; justify-content: space-between; align-items: center; border: 1px solid #3b3d54;
        }
        .upgrade-info { width: 65%; }
        .upgrade-name { font-weight: bold; color: #ffffff; font-size: 13px; margin-bottom: 3px; }
        .upgrade-desc { color: #868e96; font-size: 11px; line-height: 1.3; }
        .buy-btn { 
            background-color: #37b24d; color: white; border: none; padding: 10px 14px;
            font-size: 12px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: background 0.2s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .buy-btn:hover { background-color: #2b8a3e; }
        .buy-btn:disabled { background-color: #495057; color: #868e96; cursor: not-allowed; box-shadow: none; }
        
        /* 둥둥 떠다니는 텍스트 이펙트 (+1,000원 효과) */
        @keyframes floatUp {
            0% { transform: translateY(0); opacity: 1; }
            100% { transform: translateY(-40px); opacity: 0; }
        }
        .floating-text {
            position: absolute; color: #40c057; font-weight: bold; font-size: 16px;
            animation: floatUp 0.6s ease-out forwards; pointer-events: none; z-index: 10;
        }
    </style>
</head>
<body>

    <div class="game-wrapper">
        <h1>🍗 타이쿤 마스터</h1>
        <div class="sub-title">최고의 도트 감성 치킨 가게 시뮬레이터</div>
        
        <div class="game-screen" id="screen">
            <div class="kitchen-zone">
                <div class="kitchen-title">주방</div>
                <div class="sprite chef" id="chef-char">👨‍🍳</div>
                <div class="sprite helper" id="helper-char">🧑‍🍳</div>
            </div>
            
            <div class="hall-zone">
                <div class="hall-title">HALL</div>
                <div class="table-seat seat1" id="s1">🪑</div>
                <div class="table-seat seat2" id="s2">🪑</div>
                <div class="table-seat seat3" id="s3">🪑</div>
                <div class="table-seat seat4" id="s4">🪑</div>
            </div>
        </div>

        <div class="money-display"><span id="m">0</span> ₩</div>
        <div class="stats">
            <div>🖱️ 클릭: <span id="pow">1,000</span></div>
            <div>⏰ 초당: <span id="auto">0</span></div>
        </div>
        
        <button class="fry-btn" onclick="fry()">🍗 치킨 튀겨서 서빙하기!</button>
        
        <div class="shop-section">
            <div class="shop-title">🛒 매장 업그레이드 상점</div>
            
            <div class="upgrade-card">
                <div class="upgrade-info">
                    <div class="upgrade-name">🧑‍🍳 주방 파트타임 알바 고용</div>
                    <div class="upgrade-desc">자동으로 닭을 튀깁니다. (초당 +500원)</div>
                </div>
                <button class="buy-btn" id="b1" onclick="buy(1)"><span id="c1">10,000</span></button>
            </div>

            <div class="upgrade-card">
                <div class="upgrade-info">
                    <div class="upgrade-name">🌶️ 특제 황금 소스 개발</div>
                    <div class="upgrade-desc">치킨의 단가가 영구 상승합니다. (+1,500원/클릭)</div>
                </div>
                <button class="buy-btn" id="b2" onclick="buy(2)"><span id="c2">30,000</span></button>
            </div>
        </div>
    </div>

    <script>
        // 초기 게임 세팅 변수값
        let money = 0; 
        let power = 1000; 
        let autoIncome = 0;
        
        let cost1 = 10000; 
        let cost2 = 30000; 
        let hasHelper = false;
        
        // 손님으로 찾아올 이모지 캐릭터들
        const guests = ["👨‍💼", "👩‍⚕️", "🐱", "🐶", "🦊", "👧", "🧑‍💻", "🦁"];

        // 화면을 갱신하는 코어 함수
        function update() {
            document.getElementById('m').innerText = money.toLocaleString();
            document.getElementById('pow').innerText = power.toLocaleString();
            document.getElementById('auto').innerText = autoIncome.toLocaleString();
            document.getElementById('c1').innerText = cost1.toLocaleString() + "원";
            document.getElementById('c2').innerText = cost2.toLocaleString() + "원";
            
            // 보유 금액에 따른 버튼 활성화/비활성화 처리
            document.getElementById('b1').disabled = (money < cost1);
            document.getElementById('b2').disabled = (money < cost2);

            // 주방 보조를 사면 🧑‍🍳 캐릭터가 영구 등장
            if(hasHelper) {
                document.getElementById('helper-char').style.display = 'block';
            }
        }

        // 클릭 액션 (치킨 튀기기 버튼 클릭 시)
        function fry() {
            money += power;
            
            // 1. 주방장 캐릭터 모션 작동
            const chef = document.getElementById('chef-char');
            chef.style.transform = 'scale(1.3) translateY(-8px) rotate(5deg)';
            setTimeout(function() { 
                chef.style.transform = 'scale(1) translateY(0) rotate(0deg)'; 
            }, 80);
            
            // 2. 화면에 돈이 오르는 실시간 둥둥 텍스트 팝업 생성
            createFloatingText();
            
            update();
        }

        // 둥둥 스코어 텍스트 이펙트 함수
        function createFloatingText() {
            const screen = document.getElementById('screen');
            const text = document.createElement('div');
            text.className = 'floating-text';
            text.innerText = '+' + power.toLocaleString() + '원';
            
            // 주방장 머리 위 근처 무작위 위치 설정
            text.style.left = (20 + Math.random() * 20) + 'px';
            text.style.top = (40 + Math.random() * 20) + 'px';
            
            screen.appendChild(text);
            
            // 애니메이션이 끝나면 리소스 소멸 처리
            setTimeout(function() { text.remove(); }, 600);
        }

        // 업그레이드 상점 아이템 구매
        function buy(type) {
            if(type === 1 && money >= cost1) {
                money -= cost1; 
                autoIncome += 500; 
                cost1 = Math.floor(cost1 * 1.5); 
                hasHelper = true;
            } else if(type === 2 && money >= cost2) {
                money -= cost2; 
                power += 1500; 
                cost2 = Math.floor(cost2 * 1.6);
            }
            update();
        }

        // 실시간 손님 순환 루프 시스템 (1.8초마다 좌석 상태 업데이트)
        setInterval(function() {
            for(let i=1; i<=4; i++) {
                const seat = document.getElementById('s' + i);
                
                // 일정한 확률로 손님이 들어오거나 나감
                if(Math.random() > 0.45) {
                    const idx = Math.floor(Math.random() * guests.length);
                    // 손님이 앉아서 치킨을 냠냠 뜯고 있는 그래픽 연출
                    seat.innerText = guests[idx] + "🍗";
                    seat.style.transform = 'scale(1.1)';
                } else {
                    // 빈 의자 상태
                    seat.innerText = "🪑";
                    seat.style.transform = 'scale(1)';
                }
            }
            
            // 알바가 고용된 상태라면 알바도 일하면서 주기적으로 씰룩거림
            if(hasHelper) {
                const helper = document.getElementById('helper-char');
                helper.style.transform = 'translateY(' + (Math.random() * -5) + 'px)';
            }
        }, 1800);

        // 방치형 베이스 연동: 1초마다 자동 수익 축적
        setInterval(function() {
            if(autoIncome > 0) { 
                money += autoIncome; 
                update(); 
            }
        }, 1000);

        // 게임 스타트업 실행
        update();
    </script>
</body>
</html>
