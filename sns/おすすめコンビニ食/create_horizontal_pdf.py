#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
横スライド形式（16:9）おすすめコンビニ飯ガイド
pojipoji-bodymake / STAY GOLD 版
ワクワク×ポジティブ×温かみのあるパープル系世界観
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
FONT_BOLD = "HeiseiKakuGo-W5"
FONT_REG  = "HeiseiKakuGo-W5"

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "output", "おすすめコンビニ飯ガイド_横スライド.pdf")

# 16:9 横スライド
W, H = 1440, 810

# ---- カラーパレット（ワクワク×ポジティブ×温かみパープル） ----
C_BG_DARK   = colors.HexColor("#1A1028")   # ディープパープル背景
C_BG_MID    = colors.HexColor("#251A38")   # 中間パープル背景
C_ACCENT    = colors.HexColor("#FF6B81")   # コーラルピンク（メインアクセント）
C_ACCENT2   = colors.HexColor("#FFB347")   # ゴールデンアンバー（サブアクセント）
C_WHITE     = colors.white
C_GRAY      = colors.HexColor("#8B7FA0")   # パープルグレー
C_LIGHT     = colors.HexColor("#D4C5E0")   # ラベンダーライト
C_CARD      = colors.HexColor("#2A1F3D")   # カード背景

C_SEVEN     = colors.HexColor("#007D40")
C_LAWSON    = colors.HexColor("#0068B7")
C_FAMILY    = colors.HexColor("#00A0E9")
C_FAMILY_G  = colors.HexColor("#009A44")


def draw_rounded_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None, lw=0.5):
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(lw)
    else:
        c.setStrokeColor(colors.transparent)
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()


def draw_bg(c, color=None):
    """全面背景"""
    c.setFillColor(color or C_BG_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_page_num(c, num, total):
    """右下に背景付きページ番号を描画"""
    c.saveState()
    text = f"{num} / {total}"
    tx = W - 55
    ty = 14
    draw_rounded_rect(c, tx - 40, ty - 6, 80, 24, 6,
                      fill_color=colors.HexColor("#1A1028CC"))
    c.setFillColor(colors.HexColor("#9988AA"))
    c.setFont(FONT_REG, 13)
    c.drawCentredString(tx, ty, text)
    c.restoreState()


def draw_accent_line(c, y, color=None):
    c.setFillColor(color or C_ACCENT)
    c.rect(0, y, W, 3, fill=1, stroke=0)


# ================================================================
# 全商品データ
# ================================================================

SEVEN_ITEMS = [
    {"name": "7プレミアム 焼鳥もも塩", "cat": "冷凍食品", "p": 20.1, "f": 5.8, "c": 1.9, "kcal": 140, "area": "全国", "img": "seven_yakitori_shio.jpg",
     "desc": "電子レンジで温めるだけの手軽さ。\nもも肉の旨みと塩味のシンプルな味付け。"},
    {"name": "7プレミアム 焼鳥ももたれ", "cat": "冷凍食品", "p": 19.8, "f": 5.7, "c": 5.9, "kcal": 154, "area": "全国", "img": "seven_yakitori_tare.jpg",
     "desc": "甘辛いたれが食欲をそそる定番の味。\nレンジ調理で手軽にたんぱく質補給。"},
    {"name": "7プレミアム 炭火焼鳥4種盛り", "cat": "冷凍食品", "p": 16.1, "f": 8.3, "c": 0.5, "kcal": 141, "area": "全国", "img": "seven_yakitori_4set.jpg",
     "desc": "4種の焼鳥が楽しめるバラエティパック。\n炭火の香ばしさが魅力。"},
    {"name": "たんぱく質が摂れるチキンロール", "cat": "サンドイッチ", "p": 25.3, "f": 8.5, "c": 22.4, "kcal": 260, "area": "全国", "img": "seven_chicken_roll.jpg",
     "desc": "P25.3gでセブンのロール系最強。\n手軽に食べられて栄養バランスも優秀。"},
    {"name": "鶏むね肉の大葉焼鳥 梅だれ", "cat": "惣菜（焼鳥）", "p": 30.5, "f": 4.6, "c": 2.6, "kcal": 174, "area": "埼玉・千葉・東京 他", "img": "seven_ooba_umadare.jpg",
     "desc": "P30.5gはセブン全商品中トップクラス。\n梅だれと大葉でさっぱり食べられる。"},
    {"name": "だしが自慢の豚肉そば", "cat": "麺類（そば）", "p": 23.6, "f": 6.4, "c": 55.0, "kcal": 372, "area": "山梨・長野", "img": "seven_buta_soba.jpg",
     "desc": "信州産そば粉使用の本格そば。\n豚肉たっぷりで高たんぱく。"},
    {"name": "札幌ブラックラーメン", "cat": "麺類（ラーメン）", "p": 23.9, "f": 9.9, "c": 57.1, "kcal": 413, "area": "沖縄", "img": "seven_sapporo_black.jpg",
     "desc": "脂質9.9gでギリギリ条件クリア。\nラーメンで条件を満たす貴重な一品。"},
    {"name": "冷し中華（本州・九州版）", "cat": "麺類", "p": 19.3, "f": 9.8, "c": 81.9, "kcal": 493, "area": "東北・関東・近畿 他", "img": "seven_hiyashi_chuuka.jpg",
     "desc": "チャーシュー・錦糸玉子・ゆで卵入り。\n脂質9.8gで条件をクリア。"},
    {"name": "豚しゃぶサラダ", "cat": "サラダ", "p": 18.2, "f": 5.3, "c": 2.6, "kcal": 131, "area": "北海道", "img": "seven_buta_shabu_salad.jpg",
     "desc": "レモン風味おろしポン酢でさっぱり。\n低カロリー131kcalも魅力。"},
    {"name": "和風だれ鶏つくね弁当", "cat": "弁当", "p": 16.7, "f": 4.6, "c": 60.2, "kcal": 349, "area": "北海道・東北・関東 他", "img": "seven_tsukune_bento.jpg",
     "desc": "もち麦飯使用で食物繊維もプラス。\n脂質4.6gの優秀な弁当。"},
]

LAWSON_ITEMS = [
    {"name": "てっげうめぇ！炭火焼き 黒胡椒", "cat": "チルド惣菜", "p": 22.1, "f": 7.5, "c": 1.5, "kcal": 162, "area": "全国", "img": "lawson_tegue_black.png",
     "desc": "ローソン最強クラスの惣菜。\nP22.1gで黒胡椒のパンチが効いた一品。"},
    {"name": "砂肝のガーリック焼き", "cat": "チルド惣菜", "p": 21.4, "f": 4.9, "c": 7.6, "kcal": 160, "area": "全国", "img": "lawson_sunagimo.png",
     "desc": "F4.9gと脂質が特に低い優秀商品。\nガーリックの香りで食べ応え十分。"},
    {"name": "グリルチキン", "cat": "チルド惣菜", "p": 21.1, "f": 7.7, "c": 2.6, "kcal": 164, "area": "全国", "img": "lawson_grill_chicken.png",
     "desc": "シンプルなグリルチキン。\n安定のP21g超えでリピート確定。"},
    {"name": "てっげうめぇ！炭火焼き 塩", "cat": "チルド惣菜", "p": 20.2, "f": 9.2, "c": 0.4, "kcal": 165, "area": "全国", "img": "lawson_tegue_shio.png",
     "desc": "塩味でシンプルに楽しめる。\nP20.2gの安定した高たんぱく。"},
    {"name": "よだれ鶏", "cat": "チルド惣菜", "p": 17.9, "f": 4.6, "c": 17.3, "kcal": 182, "area": "全国", "img": "lawson_yodare_tori.png",
     "desc": "麻辣醤・豆板醤・花山椒の本格派。\n冷たいまま食べられて便利。"},
    {"name": "ざるそば", "cat": "麺類", "p": 18.9, "f": 3.0, "c": 63.4, "kcal": 356, "area": "全国", "img": "lawson_zarusoba.png",
     "desc": "F3.0gで脂質が極めて低い。\nたんぱく源と組み合わせれば完璧な一食。"},
    {"name": "ROLLサンド チキンとたまご", "cat": "サンドイッチ", "p": 17.6, "f": 9.7, "c": 29.8, "kcal": 277, "area": "沖縄除く", "img": "lawson_roll_sand.png",
     "desc": "ソフトフランスパン使用。\nチキンとたまごで栄養バランス◎"},
    {"name": "1食分の野菜ちゃんぽん", "cat": "麺類", "p": 16.4, "f": 8.2, "c": 42.9, "kcal": 311, "area": "地域差あり", "img": "lawson_chanpon.png",
     "desc": "8種の野菜で1食分の野菜が摂れる。\n温かい麺類でたんぱく質も確保。"},
]

FAMILY_ITEMS = [
    {"name": "たんぱく質が摂れるチキンロール", "cat": "サンドイッチ", "p": 22.9, "f": 9.8, "c": 25.3, "kcal": 281, "area": "全国", "img": "family_chicken_roll.jpg",
     "desc": "ファミマ最強クラスのP22.9g。\n手軽に食べられるロールタイプ。"},
    {"name": "鶏むね肉とたまごのサラダ", "cat": "サラダ", "p": 21.6, "f": 7.4, "c": 2.0, "kcal": 161, "area": "全国", "img": "family_tori_tamago_salad.jpg",
     "desc": "鶏むね肉＋ゆでたまごの黄金コンビ。\n161kcalで低カロリーも魅力。"},
    {"name": "棒棒鶏風サラダ", "cat": "サラダ", "p": 20.3, "f": 9.5, "c": 5.8, "kcal": 190, "area": "全国", "img": "family_banbang_salad.jpg",
     "desc": "棒棒鶏風のピリ辛ドレッシング。\nP20.3gで食べ応えのあるサラダ。"},
    {"name": "鶏そぼろあんかけ揚げ出し豆腐", "cat": "チルド惣菜", "p": 19.2, "f": 8.5, "c": 32.7, "kcal": 284, "area": "全国", "img": "family_tofu.jpg",
     "desc": "豆腐×鶏そぼろで高たんぱく。\nあんかけで満足感も十分。"},
    {"name": "ねぎたっぷり！豚肉そば", "cat": "麺類", "p": 18.3, "f": 9.2, "c": 52.5, "kcal": 366, "area": "全国", "img": "family_buta_soba.jpg",
     "desc": "だし豊かな温かいそば。\n豚肉とネギで栄養バランスが良い。"},
    {"name": "バジルチキン", "cat": "チルド惣菜", "p": 17.5, "f": 7.0, "c": 7.0, "kcal": 161, "area": "全国", "img": "family_basil_chicken.jpg",
     "desc": "バジルソースが香る一品。\nざるそばとの組み合わせが最強。"},
    {"name": "石臼挽きそば粉 ざるそば", "cat": "麺類", "p": 17.1, "f": 1.9, "c": 65.1, "kcal": 346, "area": "全国", "img": "family_zarusoba.jpg",
     "desc": "F1.9gは全商品中トップの低脂質。\n主食として最優秀の栄養バランス。"},
    {"name": "炙り焼鶏つくねごはん（軟骨入り）", "cat": "弁当", "p": 16.5, "f": 7.2, "c": 64.3, "kcal": 388, "area": "全国", "img": "family_tsukune_gohan.jpg",
     "desc": "軟骨の食感が楽しい弁当。\n脂質7.2gで弁当としては優秀。"},
    {"name": "冷しとろろそば", "cat": "麺類", "p": 15.1, "f": 2.2, "c": 57.7, "kcal": 311, "area": "全国", "img": "family_tororo_soba.jpg",
     "desc": "とろろ＋そばのヘルシーな組み合わせ。\nF2.2gの超低脂質メニュー。"},
    {"name": "ローストチキンのパスタサラダ", "cat": "サラダ", "p": 15.6, "f": 6.7, "c": 31.3, "kcal": 248, "area": "全国", "img": "family_pasta_salad.jpg",
     "desc": "パスタ入りで満足感のあるサラダ。\nローストチキンでたんぱく質を確保。"},
]


# ================================================================
# 番外編: 見た目に反して低脂質な商品
# ================================================================
BONUS_ITEMS = [
    {"name": "生チョコパンケーキ", "store": "セブン", "store_color": C_SEVEN,
     "cat": "スイーツ", "p": 3.9, "f": 5.1, "c": 35.7, "kcal": 203,
     "surprise": "チョコ×パンケーキなのに\n脂質たった5.1g！",
     "note": "※1個あたり（2個入り）", "img": "seven_choco_pancake.jpg"},
    {"name": "ショコラ蒸しパン", "store": "セブン", "store_color": C_SEVEN,
     "cat": "菓子パン", "p": "-", "f": 1.0, "c": "-", "kcal": "-",
     "surprise": "チョコレート菓子パンなのに\n脂質わずか1.0g！",
     "note": "※1個あたり（4個入り）", "img": "seven_chocola_mushpan.jpg"},
    {"name": "7プレミアム カステラ", "store": "セブン", "store_color": C_SEVEN,
     "cat": "焼菓子", "p": 2.6, "f": 1.8, "c": 25.2, "kcal": 127,
     "surprise": "リッチな見た目のカステラが\n1切れ脂質1.8g！",
     "note": "※1切あたり（3切入り）", "img": "seven_castella.jpg"},
    {"name": "黒蜜入りわらび餅", "store": "セブン", "store_color": C_SEVEN,
     "cat": "和菓子", "p": 2.7, "f": 2.0, "c": 50.2, "kcal": 227,
     "surprise": "きなこたっぷりスイーツが\n脂質2.0gの超低脂質！",
     "note": "", "img": "seven_warabi_mochi.jpg"},
    {"name": "とろけるクリームパン", "store": "ローソン", "store_color": C_LAWSON,
     "cat": "菓子パン", "p": "-", "f": 9.3, "c": "-", "kcal": 236,
     "surprise": "クリームたっぷりなのに\n脂質9.3gで10g以下！",
     "note": "", "img": "lawson_cream_pan.jpg"},
    {"name": "杵つき豆大福 つぶあん", "store": "ローソン", "store_color": C_LAWSON,
     "cat": "和菓子", "p": "-", "f": 0.3, "c": 44.8, "kcal": 192,
     "surprise": "ずっしり大福なのに\n脂質ほぼゼロの0.3g！",
     "note": "", "img": "lawson_daifuku.jpg"},
    {"name": "もちもち食感 生どら焼き", "store": "ファミマ", "store_color": C_FAMILY_G,
     "cat": "和菓子", "p": 5.0, "f": 6.8, "c": 50.7, "kcal": 279,
     "surprise": "「生」クリーム入りなのに\n脂質6.8gの驚き！",
     "note": "", "img": "family_nama_dorayaki.jpg"},
    {"name": "あんころ餅", "store": "ファミマ", "store_color": C_FAMILY_G,
     "cat": "和菓子", "p": 4.6, "f": 0.5, "c": 52.1, "kcal": 238,
     "surprise": "ボリューム満点の和菓子が\n脂質0.5gでほぼゼロ！",
     "note": "", "img": "family_ankoromochi.jpg"},
]


TOTAL_PAGES = (
    1  # 表紙
    + 2  # 選び方①②
    + 1  # セブン目次
    + len(SEVEN_ITEMS)  # セブン各商品
    + 1  # ローソン目次
    + len(LAWSON_ITEMS)  # ローソン各商品
    + 1  # ファミマ目次
    + len(FAMILY_ITEMS)  # ファミマ各商品
    + 1  # まとめ
    + 3  # 番外編（タイトル + リスト①② ）
    + 1  # 注意事項
)


# ================================================================
# 表紙
# ================================================================
def page_cover(c):
    cover_path = os.path.join(BASE, "assets", "表紙.png")
    if os.path.exists(cover_path):
        img = ImageReader(cover_path)
        c.drawImage(img, 0, 0, width=W, height=H, preserveAspectRatio=True, anchor='c')
    else:
        # フォールバック: 画像がない場合
        draw_bg(c)
        # グラデーション風の装飾
        c.setFillColor(colors.HexColor("#2A1F3D"))
        c.rect(0, 0, W, H / 2, fill=1, stroke=0)
        # アクセントライン
        c.setFillColor(C_ACCENT)
        c.rect(0, H / 2 - 2, W, 4, fill=1, stroke=0)
        c.setFillColor(C_ACCENT2)
        c.rect(0, H / 2 + 2, W, 2, fill=1, stroke=0)
        # タイトル
        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 28)
        c.drawCentredString(W / 2, H / 2 + 180, "楽しく踊って、賢く食べる")
        c.setFillColor(C_ACCENT)
        c.setFont(FONT_BOLD, 72)
        c.drawCentredString(W / 2, H / 2 + 60, "最強コンビニ飯")
        c.setFillColor(C_ACCENT2)
        c.setFont(FONT_BOLD, 48)
        c.drawCentredString(W / 2, H / 2 - 20, "ガイドブック")
        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 22)
        c.drawCentredString(W / 2, H / 2 - 100, "高たんぱく・低脂質  厳選28商品 + 番外編8商品")
        # ブランド名
        c.setFillColor(C_ACCENT2)
        c.setFont(FONT_BOLD, 20)
        c.drawCentredString(W / 2, 60, "STAY GOLD  |  pojipoji bodymake")


# ================================================================
# 選び方①
# ================================================================
def page_howto_1(c):
    draw_bg(c, colors.HexColor("#1E1430"))

    # ヘッダー
    c.setFillColor(C_BG_DARK)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    draw_accent_line(c, H - 93)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 40)
    c.drawString(60, H - 62, "コンビニ食の選び方")
    c.setFillColor(C_ACCENT)
    c.setFont(FONT_REG, 22)
    c.drawRightString(W - 60, H - 58, "HOW TO CHOOSE")

    # メッセージボックス
    draw_rounded_rect(c, 60, H - 200, W - 120, 80, 10, fill_color=C_CARD)
    c.setFillColor(C_ACCENT)
    c.setFont(FONT_BOLD, 28)
    c.drawCentredString(W / 2, H - 160, "コンビニでも、ダイエット・ボディメイクは十分に可能！")
    c.setFillColor(C_LIGHT)
    c.setFont(FONT_REG, 18)
    c.drawCentredString(W / 2, H - 188, "選ぶ基準を持てば、コンビニは最強の食事調達ツールになります。")

    # ポイント1〜3
    points = [
        ("01", C_ACCENT,  "たんぱく質 15g以上を目安に",
         "筋肉の維持・増量には1食あたりのたんぱく質量が重要。15g以上を目安に商品を選びましょう。"),
        ("02", C_ACCENT2, "脂質 10g以下に抑える",
         "揚げ物・マヨネーズ系は脂質が高くなりがち。焼き・蒸し・茹で系を優先することで脂質を抑えられます。"),
        ("03", C_ACCENT,  "焼き・蒸し系の調理法を選ぶ",
         "焼鳥・蒸し鶏・豚しゃぶなど、油を使わない調理法の商品はP↑F↓の条件を満たしやすい。"),
    ]

    card_w = (W - 120 - 40) / 3
    card_h = 300
    card_y = H - 550

    for i, (num, col, title, body) in enumerate(points):
        cx = 60 + i * (card_w + 20)
        draw_rounded_rect(c, cx, card_y, card_w, card_h, 10, fill_color=C_CARD)
        c.setFillColor(col)
        c.rect(cx, card_y + card_h - 6, card_w, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont(FONT_BOLD, 60)
        c.drawCentredString(cx + card_w / 2, card_y + card_h - 90, num)
        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 22)
        c.drawCentredString(cx + card_w / 2, card_y + card_h - 140, title)
        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 16)
        words = body
        max_chars = 20
        lines = []
        while words:
            lines.append(words[:max_chars])
            words = words[max_chars:]
        for j, line in enumerate(lines):
            c.drawCentredString(cx + card_w / 2, card_y + card_h - 175 - j * 25, line)


# ================================================================
# 選び方②
# ================================================================
def page_howto_2(c):
    draw_bg(c, colors.HexColor("#1E1430"))

    c.setFillColor(C_BG_DARK)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    draw_accent_line(c, H - 93)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 40)
    c.drawString(60, H - 62, "コンビニ食の選び方")
    c.setFillColor(C_ACCENT)
    c.setFont(FONT_REG, 22)
    c.drawRightString(W - 60, H - 58, "HOW TO CHOOSE")

    points = [
        ("04", C_ACCENT2, "麺類はそば・冷し中華が狙い目",
         "ラーメンより、そばや冷し中華は脂質が低め。たんぱく質豊富な具材も補給できます。"),
        ("05", C_ACCENT,  "必ず包装ラベルで最終確認",
         "Web情報と店頭表示が異なる場合があります。購入時は必ず包装裏面の栄養成分表示を確認。"),
    ]

    card_w = (W - 120 - 20) / 2
    card_h = 320
    card_y = H - 520

    for i, (num, col, title, body) in enumerate(points):
        cx = 60 + i * (card_w + 20)
        draw_rounded_rect(c, cx, card_y, card_w, card_h, 10, fill_color=C_CARD)
        c.setFillColor(col)
        c.rect(cx, card_y + card_h - 6, card_w, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont(FONT_BOLD, 72)
        c.drawCentredString(cx + card_w / 2, card_y + card_h - 110, num)
        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 26)
        c.drawCentredString(cx + card_w / 2, card_y + card_h - 160, title)
        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 18)
        max_chars = 26
        words = body
        lines = []
        while words:
            lines.append(words[:max_chars])
            words = words[max_chars:]
        for j, line in enumerate(lines):
            c.drawCentredString(cx + card_w / 2, card_y + card_h - 210 - j * 28, line)

    c.setFillColor(C_ACCENT)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(W / 2, 100, "この5つのポイントを押さえれば、コンビニで理想の食事が見つかります！")


# ================================================================
# 商品リスト（目次）ページ
# ================================================================
def page_store_index(c, store_name, items, brand_color, subtitle=""):
    draw_bg(c, colors.HexColor("#1E1430"))

    c.setFillColor(brand_color)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 40)
    c.drawString(60, H - 62, f"{store_name}  おすすめ商品一覧")
    c.setFillColor(colors.HexColor("#FFFFFFCC"))
    c.setFont(FONT_REG, 20)
    c.drawRightString(W - 60, H - 58, f"全{len(items)}商品  |  {subtitle}")

    draw_accent_line(c, H - 93, brand_color)

    th_y = H - 140
    c.setFillColor(C_BG_MID)
    c.rect(60, th_y - 5, W - 120, 40, fill=1, stroke=0)
    c.setFillColor(C_ACCENT)
    c.setFont(FONT_BOLD, 18)
    c.drawString(80, th_y + 8, "No.")
    c.drawString(140, th_y + 8, "商品名")
    c.drawString(700, th_y + 8, "カテゴリ")
    c.drawString(920, th_y + 8, "P（g）")
    c.drawString(1040, th_y + 8, "F（g）")
    c.drawString(1160, th_y + 8, "kcal")
    c.drawString(1280, th_y + 8, "販売地域")

    row_h = 50
    start_y = th_y - 45

    for i, item in enumerate(items):
        ry = start_y - i * row_h

        if i % 2 == 0:
            c.setFillColor(colors.HexColor("#1E1432"))
        else:
            c.setFillColor(colors.HexColor("#1A1028"))
        c.rect(60, ry - 5, W - 120, row_h, fill=1, stroke=0)

        c.setFillColor(brand_color)
        c.rect(60, ry - 5, 4, row_h, fill=1, stroke=0)

        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 20)
        c.drawString(82, ry + 12, f"{i + 1:02d}")

        c.setFont(FONT_BOLD, 18)
        name_display = item["name"].replace("\n", " ")
        if len(name_display) > 22:
            name_display = name_display[:21] + "…"
        c.drawString(140, ry + 12, name_display)

        c.setFillColor(C_GRAY)
        c.setFont(FONT_REG, 16)
        c.drawString(700, ry + 12, item["cat"])

        c.setFillColor(brand_color)
        c.setFont(FONT_BOLD, 20)
        c.drawString(920, ry + 12, f"{item['p']}")

        c.setFillColor(C_ACCENT2)
        c.setFont(FONT_BOLD, 18)
        c.drawString(1040, ry + 12, f"{item['f']}")

        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 16)
        c.drawString(1160, ry + 12, f"{item['kcal']}")

        area = item["area"]
        if len(area) > 8:
            area = area[:7] + "…"
        c.drawString(1280, ry + 12, area)


# ================================================================
# 個別商品ページ（1ページ1商品）
# ================================================================
def page_product(c, item, brand_color, store_name, idx, total_in_store):
    draw_bg(c, colors.HexColor("#1E1430"))

    c.setFillColor(brand_color)
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 28)
    c.drawString(60, H - 48, store_name)
    c.setFillColor(colors.HexColor("#FFFFFFCC"))
    c.setFont(FONT_REG, 18)
    c.drawRightString(W - 60, H - 45, f"{idx} / {total_in_store}")

    img_area_x = 60
    img_area_y = 80
    img_area_w = 560
    img_area_h = H - 170

    info_x = 660
    info_w = W - 660 - 60

    draw_rounded_rect(c, img_area_x, img_area_y, img_area_w, img_area_h, 12,
                      fill_color=colors.HexColor("#2A1F3D"))

    if item["img"]:
        ip = os.path.join(BASE, "product_images", item["img"])
        if os.path.exists(ip):
            pad = 30
            c.drawImage(ip,
                        img_area_x + pad, img_area_y + pad,
                        width=img_area_w - pad * 2,
                        height=img_area_h - pad * 2,
                        preserveAspectRatio=True, anchor='c')

    # カテゴリバッジ
    cat_y = H - 120
    draw_rounded_rect(c, info_x, cat_y - 5, len(item["cat"]) * 20 + 30, 38, 6, fill_color=brand_color)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 18)
    c.drawString(info_x + 15, cat_y + 5, item["cat"])

    area_badge_x = info_x + len(item["cat"]) * 20 + 50
    c.setFillColor(C_GRAY)
    c.setFont(FONT_REG, 16)
    c.drawString(area_badge_x, cat_y + 5, f"📍 {item['area']}")

    # 商品名
    name_y = cat_y - 55
    c.setFillColor(C_WHITE)
    name_parts = item["name"].split("\n")
    if len(name_parts) == 1:
        c.setFont(FONT_BOLD, 38)
        c.drawString(info_x, name_y, name_parts[0])
    else:
        c.setFont(FONT_BOLD, 34)
        c.drawString(info_x, name_y, name_parts[0])
        c.drawString(info_x, name_y - 45, name_parts[1])
        name_y -= 45

    # 説明文
    desc_y = name_y - 55
    c.setFillColor(C_LIGHT)
    c.setFont(FONT_REG, 20)
    desc_lines = item["desc"].split("\n")
    for j, line in enumerate(desc_lines):
        c.drawString(info_x, desc_y - j * 30, line)

    # 栄養情報カード
    nut_y = 200
    nut_h = 180
    draw_rounded_rect(c, info_x, nut_y - 20, info_w, nut_h, 10, fill_color=C_CARD)

    c.setFillColor(brand_color)
    c.setFont(FONT_BOLD, 18)
    c.drawString(info_x + 20, nut_y + nut_h - 50, "たんぱく質")
    c.setFont(FONT_BOLD, 56)
    c.drawString(info_x + 20, nut_y + nut_h - 115, f"P  {item['p']}g")

    c.setStrokeColor(colors.HexColor("#3A2F50"))
    c.setLineWidth(1)
    sep_x = info_x + 300
    c.line(sep_x, nut_y - 5, sep_x, nut_y + nut_h - 30)

    sub_x = sep_x + 30
    c.setFillColor(C_ACCENT2)
    c.setFont(FONT_BOLD, 16)
    c.drawString(sub_x, nut_y + nut_h - 50, "脂質")
    c.setFont(FONT_BOLD, 36)
    c.drawString(sub_x, nut_y + nut_h - 90, f"F  {item['f']}g")

    sub_x2 = sep_x + 230
    c.setFillColor(colors.HexColor("#B088D0"))
    c.setFont(FONT_BOLD, 16)
    c.drawString(sub_x2, nut_y + nut_h - 50, "炭水化物")
    c.setFont(FONT_BOLD, 36)
    c.drawString(sub_x2, nut_y + nut_h - 90, f"C  {item['c']}g")

    c.setFillColor(C_GRAY)
    c.setFont(FONT_REG, 18)
    c.drawString(sub_x, nut_y + 5, f"エネルギー")
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 28)
    c.drawString(sub_x + 150, nut_y, f"{item['kcal']} kcal")

    c.setFillColor(brand_color)
    c.rect(0, 45, W, 3, fill=1, stroke=0)


# ================================================================
# まとめページ
# ================================================================
def page_summary(c):
    draw_bg(c)

    c.setFillColor(C_ACCENT)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColor(C_BG_DARK)
    c.setFont(FONT_BOLD, 40)
    c.drawCentredString(W / 2, H - 62, "まとめ — 3つの戦略")

    strategies = [
        ("STEP 1", "主役は「焼き・蒸し系たんぱく源」",
         "焼鳥（塩/たれ）・蒸し鶏・豚しゃぶが最優秀候補。\n揚げ物・マヨネーズ系は脂質オーバーになりやすい。",
         C_ACCENT),
        ("STEP 2", "主食は「そば」か「冷し中華」",
         "ざるそばは脂質2〜3g台と優秀。冷し中華も脂質10g以内。\nこってりラーメン・チャーハンは避ける。",
         C_ACCENT2),
        ("STEP 3", "全国販売品を軸に、地域品でプラスα",
         "セブンプレミアム冷凍焼鳥3品は全国で購入可能。\n地域限定品は補助的に活用する。",
         C_ACCENT),
    ]

    card_w = (W - 120 - 40) / 3
    card_h = 340
    card_y = H - 480

    for i, (step, title, body, col) in enumerate(strategies):
        cx = 60 + i * (card_w + 20)
        draw_rounded_rect(c, cx, card_y, card_w, card_h, 10, fill_color=C_CARD)

        draw_rounded_rect(c, cx + 20, card_y + card_h - 60, 120, 36, 6, fill_color=col)
        c.setFillColor(C_BG_DARK)
        c.setFont(FONT_BOLD, 18)
        c.drawCentredString(cx + 80, card_y + card_h - 48, step)

        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 22)
        c.drawString(cx + 20, card_y + card_h - 100, title)

        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 16)
        for j, line in enumerate(body.split("\n")):
            c.drawString(cx + 20, card_y + card_h - 140 - j * 26, line)

    tips_y = 130
    store_tips = [
        (C_SEVEN,  "Seven-Eleven", "冷凍焼鳥シリーズが全国展開の最強定番。そば・冷し中華も脂質が低い。"),
        (C_LAWSON, "LAWSON",       "チルド惣菜に超高たんぱく商品が集中。てっげうめぇ！シリーズが狙い目。"),
        (C_FAMILY, "FamilyMart",   "チキンロールP22.9gが最強。ざるそばF1.9gとの組み合わせが最強コンビ。"),
    ]
    tip_w = (W - 120 - 40) / 3
    for i, (sc, sn, stip) in enumerate(store_tips):
        tx = 60 + i * (tip_w + 20)
        draw_rounded_rect(c, tx, tips_y, tip_w, 60, 6, fill_color=C_BG_MID)
        c.setFillColor(sc)
        c.rect(tx, tips_y, 5, 60, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 16)
        c.drawString(tx + 15, tips_y + 38, sn)
        c.setFillColor(C_LIGHT)
        c.setFont(FONT_REG, 13)
        max_c = 30
        lines = [stip[k:k+max_c] for k in range(0, len(stip), max_c)]
        for j, line in enumerate(lines):
            c.drawString(tx + 15, tips_y + 18 - j * 18, line)


# ================================================================
# 番外編タイトルページ
# ================================================================
def page_bonus_title(c):
    draw_bg(c)

    c.setFillColor(C_ACCENT2)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColor(C_BG_DARK)
    c.setFont(FONT_BOLD, 44)
    c.drawCentredString(W / 2, H - 62, "番外編")

    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 48)
    c.drawCentredString(W / 2, H - 220, "見た目に反して")
    c.setFillColor(C_ACCENT2)
    c.setFont(FONT_BOLD, 64)
    c.drawCentredString(W / 2, H - 300, "脂質 10g 以下！")

    c.setFillColor(C_LIGHT)
    c.setFont(FONT_REG, 24)
    c.drawCentredString(W / 2, H - 380, "「え、これで低脂質なの！？」という意外な商品を集めました")

    draw_rounded_rect(c, 200, 120, W - 400, 70, 10, fill_color=C_CARD)
    c.setFillColor(C_ACCENT2)
    c.setFont(FONT_BOLD, 20)
    c.drawCentredString(W / 2, 162, "※ たんぱく質の基準（15g以上）は満たしていません")
    c.setFillColor(C_LIGHT)
    c.setFont(FONT_REG, 16)
    c.drawCentredString(W / 2, 135, "ダイエット中の間食・デザート選びの参考にどうぞ")


# ================================================================
# 番外編リストページ
# ================================================================
def page_bonus_list(c):
    _draw_bonus_page(c, BONUS_ITEMS[:4], "番外編 — 見た目に反して低脂質な商品  ①")


def page_bonus_list_2(c):
    _draw_bonus_page(c, BONUS_ITEMS[4:], "番外編 — 見た目に反して低脂質な商品  ②")

    c.setFillColor(C_ACCENT2)
    c.setFont(FONT_BOLD, 16)
    c.drawString(40, 14, "和菓子は低脂質の宝庫！  大福・羊羹・わらび餅・あんころ餅はほぼ脂質ゼロ")


def _draw_bonus_page(c, items, title):
    draw_bg(c, colors.HexColor("#1E1430"))

    c.setFillColor(C_ACCENT2)
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColor(C_BG_DARK)
    c.setFont(FONT_BOLD, 32)
    c.drawString(60, H - 48, title)

    cols = 4
    margin = 40
    gap = 16
    card_w = (W - margin * 2 - gap * (cols - 1)) / cols
    card_h = 640

    for idx, item in enumerate(items):
        cx = margin + idx * (card_w + gap)
        card_top = H - 90
        card_bottom = card_top - card_h

        draw_rounded_rect(c, cx, card_bottom, card_w, card_h, 8, fill_color=C_CARD)

        c.setFillColor(item["store_color"])
        c.rect(cx, card_top - 5, card_w, 5, fill=1, stroke=0)

        c.setFillColor(item["store_color"])
        c.setFont(FONT_BOLD, 14)
        c.drawString(cx + 12, card_top - 28, item["store"])
        c.setFillColor(C_GRAY)
        c.setFont(FONT_REG, 13)
        c.drawRightString(cx + card_w - 12, card_top - 28, item["cat"])

        img_h = 220
        img_top = card_top - 40
        img_bottom = img_top - img_h

        c.setFillColor(colors.HexColor("#1E1432"))
        c.rect(cx + 8, img_bottom, card_w - 16, img_h, fill=1, stroke=0)

        if item.get("img"):
            ip = os.path.join(BASE, "product_images", item["img"])
            if os.path.exists(ip):
                try:
                    c.drawImage(ip, cx + 12, img_bottom + 4,
                                width=card_w - 24, height=img_h - 8,
                                preserveAspectRatio=True, anchor='c')
                except Exception:
                    pass

        name_y = img_bottom - 28
        c.setFillColor(C_WHITE)
        c.setFont(FONT_BOLD, 18)
        name = item["name"]
        if len(name) > 12:
            c.setFont(FONT_BOLD, 15)
        c.drawCentredString(cx + card_w / 2, name_y, name)

        c.setFillColor(C_ACCENT2)
        c.setFont(FONT_BOLD, 48)
        c.drawCentredString(cx + card_w / 2, name_y - 60, f"F {item['f']}g")

        c.setFillColor(C_WHITE)
        c.setFont(FONT_REG, 14)
        surprise_lines = item["surprise"].split("\n")
        for j, line in enumerate(surprise_lines):
            c.drawCentredString(cx + card_w / 2, name_y - 100 - j * 20, line)

        if item["kcal"] != "-":
            c.setFillColor(C_GRAY)
            c.setFont(FONT_REG, 12)
            kcal_text = f"{item['kcal']}kcal"
            if item.get("note"):
                kcal_text += f"  {item['note']}"
            c.drawCentredString(cx + card_w / 2, card_bottom + 16, kcal_text)


# ================================================================
# 注意事項ページ
# ================================================================
def page_notes(c):
    draw_bg(c)

    c.setFillColor(colors.HexColor("#E85D75"))
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont(FONT_BOLD, 40)
    c.drawCentredString(W / 2, H - 62, "購入時の重要注意事項")

    notes = [
        "栄養成分はメーカー・仕様変更により、Webと店頭ラベルが異なる場合があります。",
        "最終的な判断は必ず「包装裏面の栄養成分表示」で行ってください。",
        "販売地域は公式サイト掲載時点の情報です。店舗によって取り扱いが異なります。",
        "季節・地域限定商品は入荷状況によって購入できない場合があります。",
        "組み合わせ次第でさらに効果的に。1食だけでなくトータルの食事管理を意識しましょう。",
    ]

    card_y = H - 180
    for i, note in enumerate(notes):
        ny = card_y - i * 90
        draw_rounded_rect(c, 100, ny - 20, W - 200, 70, 8, fill_color=C_CARD)
        c.setFillColor(colors.HexColor("#E85D75"))
        c.setFont(FONT_BOLD, 28)
        c.drawString(130, ny + 8, f"0{i + 1}")
        c.setFillColor(C_WHITE)
        c.setFont(FONT_REG, 22)
        c.drawString(200, ny + 8, note)

    c.setFillColor(C_ACCENT)
    c.rect(0, 0, W, 50, fill=1, stroke=0)
    c.setFillColor(C_BG_DARK)
    c.setFont(FONT_BOLD, 20)
    c.drawString(60, 16, "STAY GOLD  |  高たんぱく・低脂質 おすすめコンビニ飯ガイド")


# ================================================================
# メイン
# ================================================================
def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("STAY GOLD 高たんぱく・低脂質 おすすめコンビニ飯ガイド（横スライド版）")
    c.setAuthor("STAY GOLD / pojipoji bodymake")

    page_num = 0

    # 表紙
    page_cover(c)
    c.showPage()
    page_num += 1

    # 選び方①
    page_howto_1(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # 選び方②
    page_howto_2(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # セブン-イレブン
    page_store_index(c, "セブン-イレブン", SEVEN_ITEMS, C_SEVEN, "P15g以上 / F10g以下 厳選")
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    for i, item in enumerate(SEVEN_ITEMS):
        page_product(c, item, C_SEVEN, "セブン-イレブン", i + 1, len(SEVEN_ITEMS))
        draw_page_num(c, page_num + 1, TOTAL_PAGES)
        c.showPage()
        page_num += 1

    # ローソン
    page_store_index(c, "ローソン", LAWSON_ITEMS, C_LAWSON, "P15g以上 / F10g以下 厳選")
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    for i, item in enumerate(LAWSON_ITEMS):
        page_product(c, item, C_LAWSON, "ローソン", i + 1, len(LAWSON_ITEMS))
        draw_page_num(c, page_num + 1, TOTAL_PAGES)
        c.showPage()
        page_num += 1

    # ファミリーマート
    page_store_index(c, "ファミリーマート", FAMILY_ITEMS, C_FAMILY_G, "P15g以上 / F10g以下 厳選")
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    for i, item in enumerate(FAMILY_ITEMS):
        page_product(c, item, C_FAMILY_G, "ファミリーマート", i + 1, len(FAMILY_ITEMS))
        draw_page_num(c, page_num + 1, TOTAL_PAGES)
        c.showPage()
        page_num += 1

    # まとめ
    page_summary(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # 番外編タイトル
    page_bonus_title(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # 番外編リスト①
    page_bonus_list(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # 番外編リスト②
    page_bonus_list_2(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()
    page_num += 1

    # 注意事項
    page_notes(c)
    draw_page_num(c, page_num + 1, TOTAL_PAGES)
    c.showPage()

    c.save()
    print(f"PDF saved: {OUT}")
    print(f"Total pages: {TOTAL_PAGES}")


if __name__ == "__main__":
    main()
