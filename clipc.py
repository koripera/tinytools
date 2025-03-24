"""
クリップボードの内容を監視し、変更があった場合に処理を行うプログラム
"""
import asyncio
import logging
import json
from typing import Optional, Callable
import pyperclip
from pynput import keyboard

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ClipboardMonitor:
    def __init__(self, callback: Callable[[str], str]):
        self.callback = callback
        self.previous_content: str = ""
        self.is_running: bool = False
        self.check_interval: float = 0.5

    async def start_monitoring(self):
        """クリップボードの監視を開始"""
        self.is_running = True
        logging.info("クリップボード監視を開始しました")
        
        try:
            while self.is_running:
                try:
                    current_content = pyperclip.paste()
                    if current_content != self.previous_content:
                        logging.info("クリップボードの変更を検出")
                        # コールバック関数を実行し、結果をクリップボードに設定
                        modified_content = self.callback(current_content)
                        pyperclip.copy(modified_content)
                        self.previous_content = modified_content
                except pyperclip.PyperclipException as e:
                    logging.error(f"クリップボードアクセスエラー: {e}")
                
                await asyncio.sleep(self.check_interval)
                
        except asyncio.CancelledError:
            logging.info("監視を終了します")
        except Exception as e:
            logging.error(f"予期せぬエラーが発生: {e}")

    def stop_monitoring(self):
        """監視を停止"""
        self.is_running = False
        logging.info("監視を停止しました")

class TextProcessor:
    @staticmethod
    def process_text(text: str) -> str:
        """テキストの処理を行う"""
        try:
            # 空白文字の削除
            text = ''.join(text.split())
            
            # 置換ルールを外部から読み込み
            with open('replacements.json', 'r', encoding='utf-8') as f:
                replacements = json.loads(f.read())
            
            for old, new in replacements.items():
                text = text.replace(old, new)
            
            return text.strip()
            
        except Exception as e:
            logging.error(f"テキスト処理中にエラー: {e}")
            return text

async def main():
    processor = TextProcessor()
    monitor = ClipboardMonitor(processor.process_text)
    
    # キーボードリスナーの設定
    def on_press(key):
        try:
            # Ctrl+Cで終了
            if key == keyboard.Key.esc:
                monitor.stop_monitoring()
                return False
        except Exception as e:
            logging.error(f"キー処理中にエラー: {e}")

    # キーボードリスナーの開始
    keyboard.Listener(on_press=on_press).start()
    
    # 監視の開始
    await monitor.start_monitoring()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("プログラムを終了します")


