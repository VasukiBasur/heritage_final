import mysql.connector

def upgrade_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root@123',
            database='heritage_handloom'
        )
        cursor = conn.cursor()
        
        # Add village
        try:
            cursor.execute("ALTER TABLE artisans ADD COLUMN village VARCHAR(100) DEFAULT 'Harapanahalli'")
            print("Added column 'village'")
        except mysql.connector.Error as err:
            if err.errno == 1060: # Duplicate column name
                print("Column 'village' already exists")
            else:
                raise err
                
        # Add experience_years
        try:
            cursor.execute("ALTER TABLE artisans ADD COLUMN experience_years INT DEFAULT 10")
            print("Added column 'experience_years'")
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print("Column 'experience_years' already exists")
            else:
                raise err
                
        # Add wage_details
        try:
            cursor.execute("ALTER TABLE artisans ADD COLUMN wage_details VARCHAR(255) DEFAULT '₹800/day'")
            print("Added column 'wage_details'")
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print("Column 'wage_details' already exists")
            else:
                raise err
        
        # Update dummy data for existing rows
        cursor.execute("UPDATE artisans SET village='Ilkal', experience_years=15, wage_details='₹800/day' WHERE village IS NULL OR village = 'Harapanahalli'")
        conn.commit()
        print("Updated dummy data successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    upgrade_database()
