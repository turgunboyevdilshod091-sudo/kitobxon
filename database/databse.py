import asyncpg
from config import config
import os

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        dsn = os.getenv("DB_URL")
        
        if dsn:
            self.pool = await asyncpg.create_pool(dsn=dsn)
        else:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                host=config.DB_HOST,
                port=config.DB_PORT
            )

    async def add_user(self, telegram_id, username):
        query = """
        INSERT INTO users (username,telegram_id) 
        VALUES ($1, $2) 
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        await self.pool.execute(query,telegram_id,username)

    async def get_user_role(self, telegram_id):
        query = "SELECT role FROM users WHERE telegram_id = $1;"
        return await self.pool.fetchval(query, telegram_id)

    async def set_user_role(self, telegram_id, role):
        query = "UPDATE users SET role = $1 WHERE telegram_id = $2;"
        await self.pool.execute(query, role, telegram_id)

    async def get_users(self):
        query = "SELECT telegram_id, username, role FROM users ORDER BY id DESC;"
        return await self.pool.fetch(query)
    
    async def get_user(self,telegram_id):
        query = "SELECT telegram_id, username, role FROM users where telegram_id=$1"
        return await self.pool.fetchrow(query,telegram_id)

    # --- BOOK METODLARI ---

    async def add_books(self, title, author, description, category, sub_category, image_id, file_id):
        query = """
        INSERT INTO books (title, author, description, category, sub_category, image_id, file_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7);
        """
        await self.pool.execute(query, title, author, description, category, sub_category, image_id, file_id)

    async def get_book(self, sub_category):
        query = """
        SELECT id, title, author 
        FROM books 
        WHERE sub_category = $1 
        ORDER BY title ASC;
        """
        return await self.pool.fetch(query, sub_category)

    async def get_book_details(self, book_id):
        query = "SELECT * FROM books WHERE id = $1;"
        return await self.pool.fetchrow(query, int(book_id))

    # --- SAVED BOOKS METODLARI ---

    async def add_to_saved(self, user_id, book_id):
        query = "INSERT INTO saved_books (user_id, book_id) VALUES ($1, $2) ON CONFLICT DO NOTHING;"
        await self.pool.execute(query, user_id, int(book_id))

    async def remove_from_saved(self, user_id, book_id):
        query = "DELETE FROM saved_books WHERE user_id = $1 AND book_id = $2;"
        await self.pool.execute(query, user_id, int(book_id))

    async def get_saved_books(self, user_id):
        query = """
            SELECT b.id, b.title, b.author 
            FROM books b
            JOIN saved_books s ON b.id = s.book_id
            WHERE s.user_id = $1
            ORDER BY s.added_at DESC;
        """
        return await self.pool.fetch(query, user_id)
    
    async def search_books(self, query):
        sql = """
        SELECT id, title, author 
        FROM books 
        WHERE title ILIKE $1 OR author ILIKE $1
        LIMIT 10;
        """
        return await self.pool.fetch(sql, f'%{query}%')

    async def get_top_books(self):
        query = """
        SELECT id, title, author, views 
        FROM books 
        ORDER BY views DESC 
        LIMIT 10;
        """
        return await self.pool.fetch(query)

    async def increment_views(self, book_id):
        """Kitob ko'rilganda uning ko'rishlar sonini +1 qilish"""
        query = "UPDATE books SET views = views + 1 WHERE id = $1"
        await self.pool.execute(query, int(book_id))

#statistika

    async def get_bot_stats(self):
        users_count=await self.pool.fetchval("select count(*) from users")
        books_count=await self.pool.fetchval("select count(*) from books")
        total_views=await self.pool.fetchval("select sum(views) from books")
        top_book=await self.pool.fetch('select title,views from books order by views desc limit 3')
        return {
            "users": users_count,
            "books": books_count,
            "views": total_views,
            "top": top_book
        }