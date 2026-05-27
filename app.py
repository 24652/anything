import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="K-치킨 요리 타이쿤", 
    layout="centered"
)

# 잘림과 겹침을 방지하기 위해 문장을 아주 짧게 쪼갰습니다.
html_lines = [
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
    "<style>",
    "body { font-family: sans-serif; background-color: #1a1a24; ",
    "text-align: center; padding: 5px; margin: 0; color: #ffffff; ",
    "user-select: none; }",
    ".game-wrapper { background: #252632; padding: 12px; ",
    "border-radius: 16px; border: 3px solid #3b3d54; ",
    "display: inline-block; width: 340px; box-sizing: border-box; }",
    "h1 { color: #ffd43b; margin: 0; font-size: 20px; ",
    "text-shadow: 2px 2px 0px #e67e22; }",
    ".money-display { font-size: 24px; font-weight: bold; ",
    "color: #51cf66; margin: 8px 0; text-shadow: 1px 1px 0px #2b8a3e; }",
    ".kitchen-board { background-color: #ced4da; ",
    "border: 3px solid #1a1a24; border-radius: 10px; ",
    "padding: 8px; margin: 10px 0; display: flex; ",
    "justify-content: space-around; }",
    ".zone { background: #adb5bd; border: 2px solid #495057; ",
    "border-radius: 8px; width: 90px; height: 110px; display: flex; ",
    "flex-direction: column; align-items: center; ",
    "justify-content: center; position: relative; cursor: pointer; }",
    ".zone-title { font-size: 11px; font-weight: bold; color: #212529; ",
    "margin-bottom: 5px; background: #e9ecef; width: 100%; ",
    "position: absolute; top: 0; border-top-left-radius: 5px; ",
    "border-top-right-radius: 5px; }",
    ".item-display { font-size: 36px; margin-top: 15px; ",
    "transition: transform 0.1s; }",
    ".zone:active .item-display { transform: scale(1.2); }",
    ".progress-bar { width: 80%; background-color: #e9ecef; ",
    "height: 8px; border-radius: 4px; overflow: hidden; ",
    "margin-top: 8px; border: 1px solid #495057; }",
    ".progress-fill { height: 100%; width: 0%; ",
    "background-color: #f76707; transition: width 0.1s linear; }",
    ".serve-btn { background-color: #37b24d; color: white; ",
    "border: none; padding: 10px; font-size: 16px; font-weight: bold; ",
    "border-radius: 10px; cursor: pointer; border-bottom: 4px solid #2b8a3e; ",
    "width: 100%; box-sizing: border-box; margin-bottom: 8px; }",
    ".serve-btn:active { border-bottom: 1px solid #2b8a3e; ",
    "transform: translateY(3px); }",
    ".serve-btn:disabled { background-color: #495057; ",
    "border-bottom: none; cursor: not-allowed; transform: none; }",
    ".status-msg { font-size: 12px; color: #ffd43b; ",
    "min-height: 18px; margin-bottom: 5px; font-weight: bold; }",
    ".shop-section { background: #1c1c24;
