# 世界とお金のコンパス

毎朝8時（JST）に自動更新される、日英2言語のニュース＆経済ブリーフィングブログ。

- 日本語版: https://achu-news.github.io/news-blog/
- 英語版（US中心）: https://achu-news.github.io/news-blog/en/

## アーキテクチャ

```
毎朝8時: Claude定期タスク（このMac上）
  → WebSearch/APIでニュース・市場データ収集（数値は必ず裏取り）
  → _posts/YYYY-MM-DD-daily-briefing.md    （日本語, lang: ja）
  → _posts/YYYY-MM-DD-daily-briefing-en.md （英語・US中心, lang: en）
  → git push → GitHub Actions（.github/workflows/jekyll.yml）
  → jekyll-polyglot でJA/ENをビルド → GitHub Pages公開
```

- **多言語**: jekyll-polyglot。日英の記事ペアは同じ `permalink`（`/YYYY/MM/DD/daily-briefing/`）を持ち、`lang:` で区別。言語切り替えはヘッダーのJS製ボタン（polyglotのURL書き換えを回避するためJS実装）
- **ビルド**: GitHub Actions（`build_type=workflow`）。標準Pagesビルドは不使用
- **解析**: Google Analytics 4（G-L00D4424B6）＋ Search Console（sitemap送信済み）
- **収益化準備**: プライバシーポリシー・広告表記（`_layouts/post.html`）・バナー枠（`_includes/ad-banner.html`）

## 自動化タスクの定義

正本: このMacの `~/.claude/scheduled-tasks/daily-news-econ-blog/SKILL.md`
ミラー: [`automation/SKILL.md`](automation/SKILL.md)（毎朝のタスク実行時に自動コピーで同期）

## 注意

- ビルドが失敗するとその朝は更新されない（前日版が残る）。タスクはpush後にビルド結果を検証し、失敗時は修正を試みる設計
- 記事の数値・事実は裏取りしたもののみ記載し、一次ソースへリンクする方針
