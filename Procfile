web: gunicorn api_server:app --log-file -
release: python3 utils/init_db.py
worker: python3 start_scraper.py