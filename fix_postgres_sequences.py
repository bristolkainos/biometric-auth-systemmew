from sqlalchemy import text
from core.database import engine


def reset_sequence(table, sequence):
    sql = (
        f"SELECT setval('{sequence}', "
        f"(SELECT COALESCE(MAX(id), 1) FROM {table}));"
    )
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print(f"Reset sequence for {table}.")


def main():
    # Table name, sequence name pairs
    targets = [
        ("users", "users_id_seq"),
        ("admin_users", "admin_users_id_seq"),
        ("biometric_data", "biometric_data_id_seq"),
        ("login_attempts", "login_attempts_id_seq"),
    ]
    for table, seq in targets:
        reset_sequence(table, seq)
    print("All sequences reset.")


if __name__ == "__main__":
    main() 
