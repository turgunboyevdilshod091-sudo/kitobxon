import asyncpg
from config import config

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        # Pool yaratilgach, jadvallarni tekshirib olamiz
        await self.create_tables()

    async def create_tables(self):
        # 1. Foydalanuvchilar jadvali (role qo'shildi)
        users_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            role TEXT DEFAULT 'user',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # 2. Kitoblar jadvali (sub_category va audio_id qo'shildi)
        books_query = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            description TEXT,
            category TEXT,
            sub_category TEXT,
            image_id TEXT,
            file_id TEXT,
            audio_id TEXT
        );
        """
        
        # 3. Saqlangan kitoblar jadvali
        saved_books_query = """
        CREATE TABLE IF NOT EXISTS saved_books (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
            book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, book_id)
        );
        """

        async with self.pool.acquire() as conn:
            await conn.execute(users_query)
            await conn.execute(books_query)
            await conn.execute(saved_books_query)
            print("✅ Barcha jadvallar (users, books, saved_books) yaratildi.")

    # --- USER METODLARI ---

    async def add_user(self, user_id, full_name, username):
        query = """
        INSERT INTO users (user_id, full_name, username) 
        VALUES ($1, $2, $3) 
        ON CONFLICT (user_id) DO NOTHING;
        """
        await self.pool.execute(query, user_id, full_name, username)

    async def get_user_role(self, user_id):
        query = "SELECT role FROM users WHERE user_id = $1;"
        return await self.pool.fetchval(query, user_id)

    async def set_user_role(self, user_id, role):
        query = "UPDATE users SET role = $1 WHERE user_id = $2;"
        await self.pool.execute(query, role, user_id)

    async def get_users(self):
        query = "SELECT user_id, username, full_name, role FROM users ORDER BY joined_at DESC;"
        return await self.pool.fetch(query)

    # --- BOOK METODLARI ---

    async def add_books(self, title, author, description, category, sub_category, image_id, file_id, audio_id):
        query = """
        INSERT INTO books (title, author, description, category, sub_category, image_id, file_id, audio_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
        """
        await self.pool.execute(query, title, author, description, category, sub_category, image_id, file_id, audio_id)

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