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

    async def add_users(self,username,telegram_id):
        query="""
        INSERT INTO users (username,telegram_id) 
        VALUES ($1, $2) 
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        await self.pool.execute(query,username,telegram_id)

    async def get_user_role(self,telegram_id):
        query="""
        select role from users where telegram_id=$1;
        """
        return await self.pool.fetchval(query,telegram_id)
    
    async def get_users(self):
        query="""
        select username,role,telegram_id from users order by id;
        """
        return await self.pool.fetch(query)

    async def set_user_role(self,telegram_id,role):
        query="""
        update users set role=$1 where telegram_id=$2;
        """
        await self.pool.execute(query,role,telegram_id)

    async def add_books(self,title,author,description,category,sub_category,image_id,file_id,audio_id):
        query="""
        insert into books (title,author,description,category,sub_category,image_id,file_id,audio_id)
        values($1,$2,$3,$4,$5,$6,$7,$8);
        """
        await self.pool.execute(query,title,author,description,category,sub_category,image_id,file_id,audio_id)

    async def get_book_details(self,book_id):
        query="""
        select * from books where id=$1;
        """
        return await self.pool.fetchrow(query,int(book_id))
    
    async def get_book(self,sub_category):
        query="""
        SELECT id, title, author 
        FROM books 
        WHERE sub_category = $1 
        ORDER BY title ASC;
        """
        return await self.pool.fetch(query,sub_category)
    
    async def add_to_saved(self, user_id, book_id):
        query = "INSERT INTO saved_books (user_id, book_id) VALUES ($1, $2) ON CONFLICT DO NOTHING"
        await self.pool.execute(query, user_id, int(book_id))

    async def remove_from_saved(self, user_id, book_id):
        query = "DELETE FROM saved_books WHERE user_id = $1 AND book_id = $2"
        await self.pool.execute(query, user_id, int(book_id))

    async def get_saved_books(self, user_id):
        query = """
            SELECT b.id, b.title, b.author 
            FROM books b
            JOIN saved_books s ON b.id = s.book_id
            WHERE s.user_id = $1
            ORDER BY s.added_at DESC
        """
        return await self.pool.fetch(query, user_id)