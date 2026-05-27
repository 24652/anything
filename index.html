<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K-치킨 프랜차이즈 타이쿤</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            background-color: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .game-container {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            width: 400px;
        }
        h1 { color: #ff6b6b; margin-bottom: 5px; }
        .status { font-size: 18px; margin: 15px 0; font-weight: bold; }
        
        /* 메인 치킨 버튼 */
        .chicken-btn {
            font-size: 70px;
            background: none;
            border: none;
            cursor: pointer;
            transition: transform 0.1s;
            outline: none;
        }
        .chicken-btn:active { transform: scale(0.9); }

        /* 업그레이드 구역 */
        .upgrade-section {
            margin-top: 25px;
            text-align: left;
        }
        .upgrade-btn {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            background-color: #4dabf7;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            cursor: pointer;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
        }
        .upgrade-btn:hover { background-color: #339af0; }
        .upgrade-btn:disabled { background-color: #ced4da; cursor: not-allowed; }

        /* 뉴스 알림 창 */
        .news-box {
            background-color: #fff3bf;
            border: 1px solid #fab005;
            padding: 10px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="game-container">
    <h1>🍗 K-치킨 타이쿤</h1>
    <p style="color: #868e96; margin-top: 0;">동네 상가에서 우주 정복까지!</p>
    
    <hr>
    
    <div class="status">현재 자산: <span id="money">0</span>원</div>
    <div class="status" style="font-size: 14px; color: #495057;">
        클릭당 수익: <span id="click-power">1,000</span>원 | 초당 자동 수익: <span id="auto-income">0</span>원
    </div>

    <button class="chicken-btn" id="chicken-click-btn" onclick="clickChicken()">🍗</button>
    <p style="color: #adb5bd; font-size: 12px;">치킨을 누르면 돈이 벌립니다!</p>

    <div class="news-box" id="news-display">📢 소식: 치킨 마차를 오픈했습니다! 첫 손님이 올까요?</div>

    <div class="upgrade-section">
        <h3>🏪 프랜차이즈 업그레이드</h3>
        <button class="upgrade-btn" id="btn-upgrade1" onclick="buyUpgrade(1)">
            <span>👨‍🍳 알바생 고용 (초당 +500원)</span>
            <span id="cost1">10,000원</span>
        </button>
        <button class="upgrade-btn" id="btn-upgrade2" onclick="buyUpgrade(2)">
            <span>🌶️ 양념치킨 개발 (클릭수익 +2,000원)</span>
            <span id="cost2">30,000원</span>
        </button>
        <button class="upgrade-btn" id="btn-upgrade3" onclick="buyUpgrade(3)">
            <span>🚀 뉴욕 타임스퀘어 광고 (초당 +5,000원)</span>
            <span id="cost3">150,000원</span>
        </button>
    </div>
</div>

<script>
    // 게임 데이터 초기화
    let money = 0;
    let clickPower = 1000;
    let autoIncome = 0;

    let cost1 = 10000;
    let cost2 = 30000;
    let cost3 = 150000;

    // 랜덤 뉴스 리스트
    const newsList = [
        "🔥 유명 유튜버의 내돈내산 극찬 릴스 떡상! 손님이 폭주합니다.",
        "🌧️ 역대급 폭우로 배달 주문이 2배로 증가했습니다!",
        "🐔 신메뉴 '마라 민트초코 치킨' 출시... 호불호가 극명하게 갈립니다.",
        "📺 주말 예능 프로그램에 우리 치킨이 노출되었습니다!",
        "💸 물가 상승으로 인해 닭고기 공급가가 잠시 변동됩니다."
    ];

    // 화면 업데이트 함수
    function updateDisplay() {
        document.getElementById('money').innerText = money.toLocaleString();
        document.getElementById('click-power').innerText = clickPower.toLocaleString();
        document.getElementById('auto-income').innerText = autoIncome.toLocaleString();
        
        document.getElementById('cost1').innerText = cost1.toLocaleString() + "원";
        document.getElementById('cost2').innerText = cost2.toLocaleString() + "원";
        document.getElementById('cost3').innerText = cost3.toLocaleString() + "원";

        // 버튼 활성화/비활성화 체크
        document.getElementById('btn-upgrade1').disabled = (money < cost1);
        document.getElementById('btn-upgrade2').disabled = (money < cost2);
        document.getElementById('btn-upgrade3').disabled = (money < cost3);
    }

    // 치킨 클릭시 돈 벌기
    function clickChicken() {
        money += clickPower;
        updateDisplay();
    }

    // 업그레이드 구매
    function buyUpgrade(type) {
        if (type === 1 && money >= cost1) {
            money -= cost1;
            autoIncome += 500;
            cost1 = Math.floor(cost1 * 1.5); // 구매할 때마다 가격 상승
        } else if (type === 2 && money >= cost2) {
            money -= cost2;
            clickPower += 2000;
            cost2 = Math.floor(cost2 * 1.7);
        } else if (type === 3 && money >= cost3) {
            money -= cost3;
            autoIncome += 5000;
            cost3 = Math.floor(cost3 * 1.6);
        }
        updateDisplay();
    }

    // 초당 자동 수익 지급 (방치형 시스템)
    setInterval(function() {
        if (autoIncome > 0) {
            money += autoIncome;
            updateDisplay();
        }
    }, 1000);

    // 15초마다 랜덤 뉴스 띄우기
    setInterval(function() {
        const randomIndex = Math.floor(Math.random() * newsList.length);
        document.getElementById('news-display').innerText = newsList[randomIndex];
    }, 15000);

    // 최초 실행
    updateDisplay();
</script>

</body>
</html>
