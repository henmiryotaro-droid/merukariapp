# メルカリ自動100円値下げアプリ

メルカリで出品している商品を毎日自動的に100円値下げするアプリです。

## 機能

- 🤖 毎日21:00に自動で値下げを実行
- 📊 値下げ履歴をデータベースに記録
- ⏰ 24時間ごとに1回のみ値下げ（同じ日に複数回値下げしない）
- 💾 設定可能な値下げ額と最低価格
- 📝 詳細なログ記録

## 必要な環境

- Python 3.8以上
- Google Chrome（Seleniumで使用）
- Chromedriver（Seleniumで必要）

## インストール

### 1. リポジトリをクローン

```bash
cd ~/Desktop/メルカリ100円値下げ
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. Chromedriversをインストール

Macの場合:
```bash
brew install chromedriver
```

または、[ChromeDriver](https://chromedriver.chromium.org/)から手動でダウンロードします。

### 4. 環境変数を設定

`.env.example`をコピーして`.env`ファイルを作成します：

```bash
cp .env.example .env
```

`.env`ファイルに自分のメルカリの認証情報を記入:

```
MERCARI_EMAIL=your_email@example.com
MERCARI_PASSWORD=your_password
```

**セキュリティ警告**: パスワードを平文で保存しないでください。本番環境では認証トークンなどのより安全な方法を使用してください。

## 使用方法

### アプリの起動

```bash
python main.py
```

アプリが起動すると、毎日21:00に自動的に値下げが実行されます。

### Vercelへのデプロイ

このリポジトリは、Vercelにデプロイして静的ページとPython APIエンドポイントを公開できるように構成されています。

- ルートURL: `index.html` による簡易ドキュメントページ
- APIエンドポイント: `/api/status`, `/api/trigger`

> ただし、Mercariのブラウザ自動化（Selenium + Chrome）はVercelのサーバーレス環境では実行できません。
> 実際の値下げ処理はローカル実行や専用サーバーでの実行をおすすめします。

### 手動での値下げテスト

```python
from mercari import MercariBot
from config import PRICE_DOWN_AMOUNT

bot = MercariBot('your_email@example.com', 'your_password')
bot.login()
items = bot.get_selling_items()
for item in items:
    bot.reduce_price(item['id'], PRICE_DOWN_AMOUNT)
bot.close()
```

## ファイル構成

```
メルカリ100円値下げ/
├── main.py              # メインアプリケーション
├── config.py            # 設定ファイル
├── mercari.py           # メルカリ連携モジュール（Selenium使用）
├── scheduler.py         # スケジューリング機能
├── requirements.txt     # 依存パッケージ
├── .env.example         # 環境変数テンプレート
├── .env                 # 環境変数（.gitignoreに追加）
├── .gitignore           # Git無視設定
├── mercari_items.db     # アイテム情報データベース（自動生成）
├── scheduler.db         # スケジューラー状態（自動生成）
├── app.log              # アプリケーションログ（自動生成）
└── README.md            # このファイル
└── index.html          # Vercelで表示する静的ページ
└── api/                # Vercel Python APIエンドポイント
    ├── status.py
    └── trigger.py
```

## 設定のカスタマイズ

`config.py`で以下の設定を変更できます：

```python
# 値下げ額（デフォルト: 100円）
PRICE_DOWN_AMOUNT = 100

# 値下げ実行時刻（デフォルト: 9:00 AM）
# scheduler.pyのAPScheduler設定で変更

# 最小価格（この価格までは値下げしない）
# itemsテーブルのmin_priceで設定
```

## ログ

アプリのすべてのアクションは`app.log`に記録されます：

```bash
# ログを確認
tail -f app.log
```

## トラブルシューティング

### Seleniumのエラー
- Chromedriversがインストールされていることを確認
- Chrome/Chromiumブラウザがインストールされていることを確認

### ログインエラー
- メールアドレスとパスワードが正しいことを確認
- メルカリアカウントが有効であることを確認
- メルカリのWebサイトが正常に動作していることを確認

### 値下げが実行されない
- アプリが実行されていることを確認
- ログファイルでエラーを確認
- 商品が出品中であることを確認
- 24時間以内に既に値下げされていないことを確認

## セキュリティに関する注意

⚠️ **重要**: 本番環境では以下の対策を実装してください：

1. パスワードを平文で保存しない
2. APIキーなどのより安全な認証方法を使用
3. `.env`ファイルを`.gitignore`に追加
4. クレデンシャルを暗号化する
5. アクセスログを定期的に確認

## ライセンス

MIT License

## 注意事項

このアプリはメルカリの利用規約に従う必要があります。メルカリの規約で自動化が禁止されていないかを確認してください。

## サポート

問題が発生した場合は、`app.log`ファイルを確認してエラーメッセージを確認してください。

## 更新履歴

### v1.0.0
- 初版リリース
- 基本的な値下げ機能
- スケジューリング機能
