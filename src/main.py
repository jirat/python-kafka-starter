from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    app_name = os.getenv("APP_NAME", "python-starter")
    env = os.getenv("ENV", "dev")
    print(f"✅ {app_name} is running in {env} mode.")

if __name__ == "__main__":
    main()
