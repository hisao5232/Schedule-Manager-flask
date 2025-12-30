# Schedule Manager (Flask + Docker + Traefik)

建設機械の修理エンジニアとしての現場経験を活かし、**「現場でも使いやすい、高速でレスポンシブなタスク管理システム」**をコンセプトに開発しました。
Ubuntu VPS上でDockerを用いて構築し、TraefikによるリバースプロキシとSSL自動更新（Let's Encrypt）を実装した実運用レベルのアプリケーションです。

## 🛠 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.12 / Flask / SQLAlchemy |
| **Database** | MySQL 8.0 |
| **Infrastructure** | Docker / Docker Compose |
| **Reverse Proxy** | Traefik (with Let's Encrypt SSL) |
| **Frontend** | HTML5 / CSS3 (Bootstrap 5) / JavaScript (ES6) |
| **Environment** | Ubuntu 24.04 (Xserver VPS) |

## 🚀 Key Features

- **レスポンシブ・ダークモード**: 現場の強い日差しの下や、夜間の作業報告でも見やすい高コントラストなダークモード設計。
- **直感的な操作感**: 
  - JavaScriptによる「物理ボタンのような押し感」のフィードバック。
  - タスク追加後の自動フォーカス機能による連続入力の最適化。
- **セキュアな設計**: 
  - 環境変数（`.env`）による機密情報の分離。
  - セッション管理（Flask-Login）とパスワード保護。
- **インフラの自動化**: Docker Composeにより、データベース、バックエンド、リバースプロキシをワンコマンドで展開可能。

## 📦 Architecture

Traefikが `todo-flask.go-pro-world.net` へのリクエストを検知し、SSL化された状態でFlaskコンテナへとルーティングします。DBコンテナは内部ネットワークに隔離されており、セキュリティを確保しています。

## 🔧 Getting Started

### Prerequisites
- Docker / Docker Compose
- Domain (Cloudflare DNS)

### Setup
1. リポジトリをクローン:
   ```bash
   git clone [https://github.com/hisao5232/Schedule-Manager-flask.git](https://github.com/hisao5232/Schedule-Manager-flask.git)
   cd Schedule-Manager-flask
   ```
環境変数の設定: .env ファイルを作成し、必要な情報を記入します。

2. コード スニペット

MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=todo_db
FLASK_SECRET_KEY=your_secret_key
DOMAIN=example.com

3. 起動:
Bash```
docker compose up -d --build
```

## 👨‍💻 Author
Hisao (Construction Machinery Repair Engineer)

Website: go-pro-world.net
