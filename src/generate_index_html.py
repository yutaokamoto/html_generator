# ライブラリのインポート
import os
import sys

from jinja2 import Environment, FileSystemLoader
from loguru import logger

# パスの設定
WORKING_DIR = os.getcwd()
HTML_DIR = f"{WORKING_DIR}/outputs"
HTML_TEMPLATE_DIR = WORKING_DIR
INDEX_PATH = f"{WORKING_DIR}/index.html"

# ライブラリのインポート元を追加
sys.path.append(WORKING_DIR)

# 自作ライブラリのインポート
from src.utils.prettify_html import HtmlFormatter

# ログの設定
logger.add("app.log", rotation="500 MB", level="DEBUG")  # DEBUGレベル以上を記録

# 日付
target_dates = ["1", "2", "3"]

# HTMLファイル一覧を取得
html_files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]

# ファイル名からパラメータを抽出
param_values = {}
for html_file in html_files:
    params = os.path.splitext(html_file)[0].split("_")
    if "index" in params:
        continue
    for param in params:
        param_name, param_value = param[:3], param[3:]
        if (not any(param_values)) or param_name not in param_values:
            param_values[param_name] = set()
        param_values[param_name].add(param_value)

# 複数の値を取りうるパラメータに限定
param_values = dict(
    sorted(
        {
            param_name: sorted(param_value_cands)
            for param_name, param_value_cands in param_values.items()
            if len(param_value_cands) > 1
        }.items(),
        key=lambda k_and_v: k_and_v[0],
    )
)
param_names = list(param_values.keys())

# ファイルへのリンクを生成
file_links = [f"{HTML_DIR}/{html_file}" for html_file in html_files]

# 行数の計算
matrix_rows = 1
for param_name, values in param_values.items():
    if len(values) > 1:
        matrix_rows *= len(values)

logger.debug(f"param_names: {param_names}")
logger.debug(f"param_values: {param_values}")
logger.debug(f"HTML_DIR: {HTML_DIR}")
logger.debug(f"matrix_rows: {matrix_rows}")

# テンプレート変数の設定
template_vars = {
    "param_names": list(param_names),
    "param_values": param_values,
    "html_directory": HTML_DIR,
    "matrix_rows": matrix_rows,
    "target_dates": target_dates,
}

# Jinja2テンプレートの読み込み
env = Environment(loader=FileSystemLoader(HTML_TEMPLATE_DIR))
template = env.get_template("index_template.html")

# テンプレートのレンダリング
html_content = template.render(template_vars)

# HtmlFormatterのインスタンスを作成
formatter = HtmlFormatter()

# HTMLを整形
prettified_html = formatter.prettify_html(html_content)

# 整形したHTMLをファイルに書き込み
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(prettified_html)


logger.success(f"Successfully generated {INDEX_PATH}")
