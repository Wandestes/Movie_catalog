from db.connection import get_connection

def test_connection():
    conn = get_connection()
    assert conn is not None
    assert conn.is_connected()
    conn.close()
