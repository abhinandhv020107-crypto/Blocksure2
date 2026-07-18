from database.database import Database
from database.queries import GET_USER_BY_EMAIL, INSERT_CUSTOMER, INSERT_MANUFACTURER, INSERT_SELLER, INSERT_USER

USERS = [
("BlockSure Admin","admin@blocksure.local","admin123","admin","Active"),
("Demo Manufacturer","manufacturer@blocksure.local","manufacturer123","manufacturer","Active"),
("Demo Seller","seller@blocksure.local","seller123","seller","Active"),
("Demo Customer","customer@blocksure.local","customer123","customer","Active"),
]

def add_user(db,user):
    row=db.fetchone(GET_USER_BY_EMAIL,(user[1],))
    if row: return int(row["user_id"])
    return int(db.execute(INSERT_USER,user).lastrowid)

if __name__ == "__main__":
    with Database() as db:
        db.create_tables()
        _,m,s,c=[add_user(db,u) for u in USERS]
        if not db.fetchone("SELECT 1 FROM manufacturers WHERE user_id=?",(m,)):
            db.execute(INSERT_MANUFACTURER,(m,"Demo Manufacturing Company","Kochi, Kerala","9000000001"))
        if not db.fetchone("SELECT 1 FROM sellers WHERE user_id=?",(s,)):
            db.execute(INSERT_SELLER,(s,"Demo Seller Store","Kollam, Kerala","9000000002"))
        if not db.fetchone("SELECT 1 FROM customers WHERE user_id=?",(c,)):
            db.execute(INSERT_CUSTOMER,(c,"Demo Customer","Punalur, Kerala","9000000003"))
    print("Demo data inserted successfully.")
