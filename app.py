import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="K-치킨 타이쿤: 레트로 픽셀 매장", layout="centered")

# 2. 게임 본문 HTML (파이썬 따옴표 에러 방지를 위해 구조 최적화)
game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pixel Chicken Tycoon</title>
    <style>
        body { font-family: sans-serif; background-color: #2c3e50; text-align: center; padding: 20px; margin: 0; color: #fff; }
        .game-wrapper { background: #34495e; padding: 20px; border-radius: 15px; border: 4px solid #bdc3c7; display: inline-block; width: 360px; }
        h1 { color: #f1c40f; margin: 0 0 5px 0; font-size: 24px; text-shadow: 2px 2px #d35400; }
        
        .game-screen { 
            background-color: #edf2f7; 
            border: 4px solid #2c3e50; 
            border-radius: 10px; 
            height: 180px; 
            margin: 15px 0; 
            position: relative;
            overflow: hidden;
        }
        
        .kitchen-zone {
            position: absolute; left: 0; top: 0; width: 90px; height: 100%;
            background-color: #cbd5e0; border-right: 3px dashed #4a5568;
        }
        .kitchen-title { font-size: 10px; color: #4a5568; font-weight: bold; margin-top: 5px; }
        .hall-zone { position: absolute; right: 0; top: 0; width: 260px; height: 100%; }
        
        .sprite { position: absolute; font-size: 28px; transition: all 0.1s ease; }
        .chef { left: 25px; top: 60px; }
        .helper { left: 25px; top: 110px; display: none; }
        
        .table-seat { position: absolute; font-size: 24px; }
        .seat1 { right: 160px; top: 30px; }
        .seat2 { right: 50px; top: 30px; }
        .seat3 { right: 160px; top: 100px; }
        .seat4 { right: 50px; top: 100px; }
        
        .money-display { font-size: 24px; font-weight: bold; color: #2ecc71; margin: 10px 0; text-shadow: 1px 1px #27ae60; }
        .stats { font-size: 12px; color: #bdc3c7; margin-bottom: 15px; }
        
        .fry-btn {
            background-color: #e67e22; color: white; border: none; padding: 12px 30px;
            font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer;
            border-bottom: 4px solid #d35400; box-shadow: 0 4px #2c3e50; outline: none;
        }
        .fry-btn:active { border-bottom: 1px solid #d35400; transform: translateY(3px); box-shadow: 0 1px #2c3e50; }
        
        .shop-section { margin-top: 20px; text-align: left; }
        .shop-title { font-size: 14px; color: #f1c40f; margin-bottom: 8px; }
        .upgrade-card { 
            background: #2c3e50; padding: 10px; margin: 6px 0; border-radius: 8px;
            display: flex; justify-content: space-between; align-items: center; border: 1px solid #455a64;
        }
        .upgrade-info { font-size: 12px; }
        .upgrade-name { font-weight: bold; color: #fff; margin-bottom:
