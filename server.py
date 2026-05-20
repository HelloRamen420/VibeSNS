#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CYBER NEON TETRIS - ローカルサーバー ＆ 自動起動スクリプト
このスクリプトを実行すると、ローカルサーバーが立ち上がり、自動的にブラウザでテトリスゲームが開きます。
"""

import http.server
import socketserver
import webbrowser
import threading
import sys
import time

PORT = 8000
HOST = "localhost"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """標準のログ出力をシンプルにして、コンソールを綺麗に保ちます。"""
    def log_message(self, format, *args):
        # 静的アセットの過剰なアクセスログを出力しないようにオーバーライド
        pass

def start_server():
    # socketの再利用を許可して、連続起動時の「Address already in use」エラーを防ぐ
    socketserver.TCPServer.allow_reuse_address = True
    
    handler = QuietHandler
    try:
        with socketserver.TCPServer((HOST, PORT), handler) as httpd:
            print("============================================================")
            print(" 🚀 CYBER NEON TETRIS サーバーを起動しました！")
            print("============================================================")
            print(f" 🎮 プレイURL:  \033[1;36mhttp://{HOST}:{PORT}\033[0m")
            print(" 🛑 終了するには: \033[1;31mCtrl + C\033[0m を押してください")
            print("============================================================")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48: # Address already in use
            print(f"\n❌ エラー: ポート {PORT} は既に使用されています。")
            print(f"ブラウザで直接 \033[1;36mhttp://{HOST}:{PORT}\033[0m を開くか、起動中のプロセスを終了してください。\n")
        else:
            print(f"\n❌ サーバー起動エラー: {e}\n")
        sys.exit(1)

def open_browser():
    # サーバーが起動し切るのをコンマ数秒待ってからブラウザを開く
    time.sleep(0.5)
    url = f"http://{HOST}:{PORT}"
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"⚠️ ブラウザの自動起動に失敗しました: {e}")
        print(f"お手数ですが、ブラウザで {url} を手動で開いてください。")

def main():
    try:
        # ブラウザを開くスレッドを先行して待機させ、メインスレッドでサーバーを動かす
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 サーバーを停止しました。プレイしていただきありがとうございました！\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
