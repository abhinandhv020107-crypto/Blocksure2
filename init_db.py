from database.database import Database

if __name__ == "__main__":
    with Database() as db:
        db.create_tables()
    print("BlockSure database created successfully: blocksure.db")
