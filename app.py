import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="K-치킨 타이쿤 Master", layout="centered")

# 2. 파이썬 문법 에러가 절대 날 수 없도록 안전하게 감싼 게임 코드
game_html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: sans-serif; 
            background-color: #1a1a24; 
            text-align: center; 
            padding: 10px; 
            margin: 0; 
            color: #ffffff; 
        }
        .game-wrapper { 
            background: #252632; 
            padding: 20px; 
            border-radius: 20px; 
            border: 4px solid #3b3d54; 
            display: inline-block; 
            width: 340px; 
        }
        h1 { 
            color: #ffd43b; 
            margin: 0 0 5px 0; 
            font-size: 24px; 
            text-shadow: 2px 2px 0px #e67e22; 
        }
        .game-screen { 
            background-color: #f1f3f5; 
            border: 4px solid #1a1a24; 
            border-radius: 12px; 
            height: 180px; 
            margin: 15px 0; 
            position: relative;
            overflow: hidden;
        }
        .kitchen-zone {
            position: absolute; left: 0; top: 0; width: 90px; height: 100%;
            background-color: #dee2e6; border-right: 4px dashed #495057;
        }
        .kitchen-title { 
            font-size: 11px; color: #495057; font-weight: bold; margin-top: 6px; 
            background: #ced4da; padding: 2px 0;
        }
        .hall-zone { position: absolute; right: 0; top: 0; width: 240px; height: 100%; background-color: #e9ecef;}
        .sprite { position: absolute; font-size: 32px; transition: transform 0.08s ease; }
        .chef { left: 25px; top: 50px; }
        .helper { left: 25px; top: 110px; display: none; }
        .table-seat { position: absolute; font-size: 26px; width: 50px; height: 50px; text-align: center; }
        .seat1 { right: 140px; top: 30px; }
        .seat2 { right: 30px; top: 30px; }
        .seat3 { right: 140px; top: 100px; }
        .seat4 { right: 30px; top: 100px; }
        .money-display { font-size: 26px; font-weight: bold; color: #51cf66; margin: 10px 0; text-shadow: 1px 1px 0px #2b8a3e; }
        .stats { font-size: 12px; color: #adc5dc; margin-bottom: 15px; background: #1c1c24; padding: 6px; border-radius: 8px; display: flex; justify-content: space-around;}
        .fry-btn {
            background-color: #f76707; color: white; border: none; padding: 12px;
            font-size: 16px; font-weight: bold; border-radius: 12px; cursor: pointer;
            border-bottom: 5px solid #d9480f; box-shadow: 0 4px #1a1a24; outline: none;
            width: 100%; box-sizing: border-box;
        }
        .fry-btn:active { border-bottom: 1px solid #d9480f; transform: translateY(4px); box-shadow: 0 1px #1a1a24; }
        .shop-section { margin-top: 20px; text-align: left; }
        .shop-title { font-size: 14px; color: #ffd43b; margin-bottom: 8px; font-weight: bold; }
        .upgrade-card { 
            background: #1c1c24; padding: 10px; margin: 6px 0; border-radius: 10px;
            display: flex; justify-content: space-between; align-items: center; border: 1px solid #3b3d54;
        }
        .upgrade-info { width: 65%; }
        .upgrade-name { font-weight: bold; color: #ffffff; font-size: 12px; }
        .upgrade-desc { color: #868e96; font-size: 11px; }
        .buy-btn { 
            background-color: #37b24d; color: white; border: none; padding:
