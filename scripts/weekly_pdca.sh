#!/bin/bash
# SNS週次PDCAレポート自動更新スクリプト
# 毎週木曜日の朝に実行（Week区切りが水曜日終わりのため）

export PATH="/Users/yujifujita/.local/node_modules/.bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/yujifujita"

WORKDIR="/Users/yujifujita/team_TomoRevo/team-TomoRevo"
LOGFILE="/Users/yujifujita/team_TomoRevo/team-TomoRevo/scripts/pdca_cron.log"
CLAUDE="/Users/yujifujita/.local/node_modules/.bin/claude"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 週次PDCAレポート更新を開始します" >> "$LOGFILE"

cd "$WORKDIR"

"$CLAUDE" --dangerously-skip-permissions --print \
"今日は週次PDCAレポートの更新日です。以下を実行してください：

1. Playwrightで https://x.com/STAYGOLDGY66061 にアクセスし、先週分（直近7投稿）のViews・いいね・RT・返信数を収集する
2. Playwrightで https://www.threads.com/@yuji_staygoldgym_tennoji にアクセスし、先週分のいいね・返信数を収集する
3. 今日の日付から今週のWeek番号を計算する（Day 1 = 3/13起算。週区切りは7日ごと）
4. NotionのSNS PDCAレポートページ（https://www.notion.so/32848561540f81809c40ccf5e63c21f4）を開き、該当WeekセクションにXとThreadsの数値データ・KPI達成状況・仮説・ネクストアクション・変更内容ログを記入する
5. 完了したらログに記録する

重要：投稿操作は行わないこと。データ収集とNotionの更新のみ実施する。" \
>> "$LOGFILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 週次PDCAレポート更新が完了しました" >> "$LOGFILE"
