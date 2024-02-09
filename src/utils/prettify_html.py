# prettify_html.py

import shutil
import subprocess


class HtmlFormatter:
    def __init__(self):
        self.prettier_path = self.get_prettier_path()

    def get_prettier_path(self):
        # 'prettier' の実行可能ファイルのフルパスを取得
        return shutil.which("prettier")

    def prettify_html(self, input_html):
        if not self.prettier_path:
            print("Prettierが見つかりませんでした。")
            return input_html

        # prettierを呼び出してHTMLを整形
        command = f"{self.prettier_path} --parser html --stdin --stdout"
        result = subprocess.run(
            command, input=input_html, shell=True, text=True, capture_output=True
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print("Prettierでエラーが発生しました:")
            print(result.stderr)
            return input_html
