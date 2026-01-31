import psycopg2
import os
from dotenv import load_dotenv
import time

load_dotenv()

def test_connection_variations():
    """Test different connection parameter combinations"""
    
    # Extract connection details from your .env
    base_params = {
        "host": "aws-1-ap-northeast-2.pooler.supabase.com",
        "port": 5432,
        "database": "postgres",
        "user": "postgres.sueldiagtqiwgyznppay",
        "password": "TYtVHR1a0QZUBPwA"
    }
    
    # Test different configurations
    test_configs = [
        {"sslmode": "require", "connect_timeout": 30},
        {"sslmode": "prefer", "connect_timeout": 30},
        {"sslmode": "require", "connect_timeout": 60, "application_name": "creator_ai_test"},
        {"sslmode": "disable", "connect_timeout": 30},  # Test without SSL
        {"sslmode": "require", "connect_timeout": 10, "keepalives_idle": 600, "keepalives_interval": 30}
    ]
    
    for i, ssl_config in enumerate(test_configs, 1):
        print(f"\n🔄 Test {i}: {ssl_config}")
        try:
            conn_params = {**base_params, **ssl_config}
            
            start_time = time.time()
            conn = psycopg2.connect(**conn_params)
            connect_time = time.time() - start_time
            
            # Test a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT version(), current_database(), current_user;")
            result = cursor.fetchone()
            
            print(f"✅ Success! Connected in {connect_time:.2f}s")
            print(f"📊 Database: {result[1]}, User: {result[2]}")
            print(f"🐘 PostgreSQL: {result[0][:50]}...")
            
            cursor.close()
            conn.close()
            return True
            
        except psycopg2.OperationalError as e:
            print(f"❌ Failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    return False

def test_url_format():
    """Test the exact URL format from .env"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print(f"🔄 Testing URL format: {database_url}")
    
    # Test with different timeout and SSL settings
    test_params = [
        {"connect_timeout": 30, "sslmode": "require"},
        {"connect_timeout": 60, "sslmode": "require", "application_name": "creator_ai"},
        {"connect_timeout": 30, "sslmode": "prefer"}
    ]
    
    for i, params in enumerate(test_params, 1):
        print(f"\n🔄 URL Test {i}: {params}")
        try:
            conn = psycopg2.connect(database_url, **params)
            
            cursor = conn.cursor()
            cursor.execute("SELECT current_database(), current_user, inet_server_addr();")
            result = cursor.fetchone()
            
            print(f"✅ Connected to database: {result[0]} as user: {result[1]}")
            print(f"🌐 Server IP: {result[2]}")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ URL test {i} failed: {e}")
    
    return False

if __name__ == "__main__":
    print("=== Supabase Connection Troubleshooting ===")
    
    # Test 1: Direct parameter connections
    print("\n1. Testing direct parameter connections...")
    success1 = test_connection_variations()
    
    # Test 2: URL format from .env
    print("\n2. Testing DATABASE_URL format...")
    success2 = test_url_format()
    
    if success1 or success2:
        print("\n🎉 At least one connection method worked!")
        print("💡 Use the successful configuration in your application")
    else:
        print("\n🚨 All connection attempts failed")
        print("💡 Consider using SQLite fallback for development:")
        print("   export DATABASE_URL='sqlite:///./creator_ai_local.db'")