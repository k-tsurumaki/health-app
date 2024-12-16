from typing import Generator

from health_app.backend.session import SessionLocal

def get_db() -> Generator:
    """DB接続を行うジェネレータ関数
        ・一度にすべての結果を返すのではなく、値を1つずつ生成し、その都度処理を停止・再開する
        ・pythonではyieldキーワードを使用して値を返す

    Yields:
        Generator: DBセッション

    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()