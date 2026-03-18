# Team.TomoRevo

ユウジさんの事業・人生を支えるAIエージェントチーム。

---

## エージェント一覧

| エージェント | 役割 | 設定ファイル |
|------------|------|-------------|
| 秘書 | タスク管理・ブリーフィング・議事録作成・ジャーナル連携 | `secretary/CLAUDE.md` |

## スラッシュコマンド一覧

| コマンド | 用途 | おすすめ頻度 |
|---------|------|-------------|
| `/sync-journal` | Notionジャーナルの最新エントリを取得し、CLAUDE.mdとメモリを自動更新 | ジャーナル記録後 |
| `/update-profile` | 対話で得た新情報をオーナープロファイルに反映 | 随時 |
| `/weekly-review` | 1週間分のジャーナル+タスクを総合レビュー（思考の癖トラッキング付き） | 週1回 |
| `/post-sns` | SNS投稿コンテンツの作成・スケジューリング支援 | 投稿時 |

## ファイル構成

```
team-TomoRevo/
├── CLAUDE.md                  # 全エージェント共通設定（オーナープロファイル・理念・価値観）
├── README.md                  # このファイル
├── .claude/
│   ├── commands/
│   │   ├── sync-journal.md    # /sync-journal コマンド定義
│   │   ├── update-profile.md  # /update-profile コマンド定義
│   │   ├── weekly-review.md   # /weekly-review コマンド定義
│   │   └── post-sns.md        # /post-sns コマンド定義
│   └── settings.local.json    # MCP権限設定（Notion・Google Sheets）
└── secretary/
    ├── CLAUDE.md              # 秘書エージェント設定
    └── briefings/             # ブリーフィング保存先
```

## データソース

| ソース | 種別 | ID |
|--------|------|----|
| ジャーナル | Notion DB | `collection://31f48561-540f-80db-ac7c-000bdfc3b66e` |
| 個人タスク | Notion DB | `3fb08cb1-64e8-42bc-96fe-1dacf983f399` |
| YouTube タスク | Google Sheets | `1faOIQzkisQzlgBl_VhxB5iO-kfkTb_Z9_x4G4n8VXS8` |

## 運用ルール

- エージェントやコマンドを追加したら、このREADMEの一覧も更新する
- `CLAUDE.md` の「現在のフォーカス」は `/sync-journal` で定期的に最新化する
- 各エージェントの `CLAUDE.md` 冒頭でルートの `CLAUDE.md` を参照する
