# FastAPI-Task-Tutorial-PJ

Zenn の本「FastAPI入門 - タスク管理APIを作ってみよう!」の答え合わせ用ソースコードです。

FastAPI でタスクの作成・取得・更新・削除ができる REST API を、4つのフェーズに分けて作ります。まず Python のリストにデータを置いて API の形を作り、最後に SQLAlchemy + SQLite へ差し替えます。

## ブランチ

| ブランチ | 内容 |
|---|---|
| `main` | 完成版 |
| `Chapter03/最小のFastAPIとSwaggerUI` | 入門03（Phase 1）を終えた時点のコード |
| `Chapter04/インメモリでCRUDを作る` | 入門04（Phase 2）を終えた時点のコード |
| `Chapter05/バリデーションと部分更新` | 入門05（Phase 3）を終えた時点のコード |
| `Chapter06/SQLiteとSQLAlchemyへ切り替える` | 入門06（Phase 4）を終えた時点のコード（完成版と同じ） |

## 動かし方

Python 3.10 以上が必要です。PowerShell の例です。

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

起動したら、ブラウザで `http://localhost:8000/docs` を開くと Swagger UI から API を試せます。停止は `Ctrl + C` です。

入門06以降は、初回起動時に SQLite のデータベースファイル `tasks.db` が作られます。データを初期状態に戻すときは、サーバーを止めて `tasks.db` を削除してください。

## 構成

```
main.py            # FastAPI アプリ（データベースの設定・モデル・エンドポイント）
requirements.txt   # 使うライブラリ
```

## 技術スタック

- Python 3.10+
- FastAPI / Uvicorn / Pydantic v2
- SQLAlchemy + SQLite
