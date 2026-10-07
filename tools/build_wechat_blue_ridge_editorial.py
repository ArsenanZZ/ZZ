"""Compatibility entry point for the shared 2026 editorial renderer."""
from build_run50_six_editorials import render as build
from pathlib import Path
def render():
 build("blue-ridge-marathon")
 return (Path(__file__).resolve().parents[1]/"run50/wechat/blue-ridge-marathon-editorial.html").read_text(encoding="utf-8")
if __name__=="__main__":
 render()
