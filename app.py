import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="K-치킨 타이쿤: 레트로 픽셀 매장", layout="centered")

# 2. 파이썬 따옴표 에러를 완벽하게 우회하는 안전한 로드 방식
st.markdown("""
<iframe srcdoc="
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body { font-family: sans-serif; background-color: #2c3e50; text-align: center; padding: 10px; margin: 0; color: #fff; }
        .game-wrapper { background: #34495e; padding: 20px; border-radius: 15px; border: 4px solid #bdc3c7; display: inline-block; width: 320px; }
        h1 { color: #f1c40f; margin: 0 0 5px 0; font-size: 22px; text-shadow: 2px 2px #d35400; }
        .game-screen { background-color: #edf2f7; border: 4px solid #2c3e50; border-radius: 10px; height: 160px; margin: 15px 0; position: relative; overflow: hidden; }
        .kitchen-zone { position: absolute; left: 0; top: 0; width: 80px; height: 100%; background-color: #cbd5e0; border-right: 3px dashed #4a5568; }
        .kitchen-title { font-size: 10px; color: #4a5568; font-weight: bold; margin-top: 5px; }
        .hall-zone { position: absolute; right: 0; top: 0; width: 230px; height: 100%; }
        .sprite { position: absolute; font-size: 26px; }
        .chef { left: 20px; top: 50px; }
        .helper { left: 20px; top: 100px; display: none; }
        .table-seat { position: absolute; font-size: 22px; }
        .seat1 { right: 140px; top: 25px; }
        .seat2 { right: 40px; top: 25px; }
        .seat3 { right: 140px; top: 90px; }
        .seat4 { right: 40px; top: 90px; }
        .money-display { font-size: 22px; font-weight: bold; color: #2ecc71; margin: 10px 0; }
        .stats { font-size: 11px; color: #bdc3c7; margin-bottom: 15px; }
        .fry-btn { background-color: #e67e22; color: white; border: none; padding: 10px 25px; font-size: 15px; font-weight: bold; border-radius: 8px; cursor: pointer; border-bottom: 4px solid #d35400; }
        .fry-btn:active { border-bottom: 1px solid #d35400; transform: translateY(3px); }
        .shop-section { margin-top: 15px; text-align: left; }
        .shop-title { font-size: 13px; color: #f1c40f; margin-bottom: 5px; }
        .upgrade-card { background: #2c3e50; padding: 8px; margin: 5px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .upgrade-name
        
