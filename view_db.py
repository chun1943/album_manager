import sqlite3

conn = sqlite3.connect('albums.db')
cursor = conn.cursor()

print("=" * 60)
print("資料庫內容查看")
print("=" * 60)

# 查看 users 表
print("\n【USERS 表】")
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
if users:
    cursor.execute("PRAGMA table_info(users);")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"欄位: {', '.join(columns)}")
    print("-" * 60)
    for row in users:
        print(f"  ID: {row[0]}, Username: {row[1]}")
else:
    print("  (無資料)")

# 查看 albums 表
print("\n【ALBUMS 表】")
cursor.execute("SELECT * FROM albums;")
albums = cursor.fetchall()
if albums:
    cursor.execute("PRAGMA table_info(albums);")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"欄位: {', '.join(columns)}")
    print("-" * 60)
    for row in albums:
        print(f"  ID: {row[0]}")
        print(f"  Title: {row[1]}")
        print(f"  Normalized Title: {row[2]}")
        print(f"  Barcode: {row[3]}")
        print(f"  Artist: {row[4]}")
        print(f"  Owner ID: {row[5]}")
        print()
else:
    print("  (無資料)")

conn.close()
