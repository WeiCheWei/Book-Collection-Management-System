"""
資料庫管理模組
包含 DatabaseManager 類別，負責所有 SQLite 資料庫操作
"""

import sqlite3
from typing import List, Optional
from models import Book


class DatabaseManager:
    """資料庫管理類別 - 負責 SQLite 資料庫的所有操作"""
    
    def __init__(self, db_path: str = "books.db"):
        """
        初始化資料庫管理器
        
        Args:
            db_path: 資料庫檔案路徑
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化資料庫，創建 books 表格"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        status TEXT DEFAULT '未讀',
                        rating INTEGER DEFAULT 0
                    )
                ''')
                conn.commit()
                print("資料庫初始化成功")
        except sqlite3.Error as e:
            print(f"資料庫初始化失敗: {e}")
            raise
    
    def get_next_id(self) -> int:
        """
        獲取下一個可用的ID (現有最大ID + 1)
        
        Returns:
            int: 下一個可用的ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT MAX(id) FROM books')
                result = cursor.fetchone()
                max_id = result[0] if result[0] is not None else 0
                return max_id + 1
        except sqlite3.Error as e:
            print(f"獲取最大ID失敗: {e}")
            return 1
    
    def add_book(self, book: Book) -> bool:
        """
        新增書籍到資料庫
        
        Args:
            book: 書籍物件
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 驗證書籍資料
            is_valid, error_msg = book.validate()
            if not is_valid:
                raise ValueError(error_msg)
            
            # 獲取下一個可用的ID
            next_id = self.get_next_id()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO books (id, title, author, year, status, rating)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (next_id, book.title, book.author, book.year, book.status, book.rating))
                
                book.id = next_id
                conn.commit()
                print(f"成功新增書籍: {book.title} (ID: {next_id})")
                return True
                
        except (sqlite3.Error, ValueError) as e:
            print(f"新增書籍失敗: {e}")
            return False
    
    def update_book(self, book: Book) -> bool:
        """
        更新書籍資訊
        
        Args:
            book: 書籍物件
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 驗證書籍資料
            is_valid, error_msg = book.validate()
            if not is_valid:
                raise ValueError(error_msg)
            
            if book.id is None:
                raise ValueError("書籍ID不能為空")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE books 
                    SET title=?, author=?, year=?, status=?, rating=?
                    WHERE id=?
                ''', (book.title, book.author, book.year, book.status, book.rating, book.id))
                
                if cursor.rowcount == 0:
                    raise ValueError("找不到指定的書籍")
                
                conn.commit()
                print(f"成功更新書籍: {book.title}")
                return True
                
        except (sqlite3.Error, ValueError) as e:
            print(f"更新書籍失敗: {e}")
            return False
    
    def delete_book(self, book_id: int) -> bool:
        """
        刪除書籍
        
        Args:
            book_id: 書籍ID
            
        Returns:
            bool: 操作是否成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
                
                if cursor.rowcount == 0:
                    raise ValueError("找不到指定的書籍")
                
                conn.commit()
                print(f"成功刪除書籍 ID: {book_id}")
                return True
                
        except (sqlite3.Error, ValueError) as e:
            print(f"刪除書籍失敗: {e}")
            return False
    
    def get_all_books(self) -> List[Book]:
        """
        獲取所有書籍
        
        Returns:
            List[Book]: 書籍列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, title, author, year, status, rating FROM books ORDER BY id')
                rows = cursor.fetchall()
                
                books = []
                for row in rows:
                    book = Book(
                        title=row[1],
                        author=row[2],
                        year=row[3],
                        status=row[4],
                        rating=row[5],
                        book_id=row[0]
                    )
                    books.append(book)
                
                return books
                
        except sqlite3.Error as e:
            print(f"獲取書籍列表失敗: {e}")
            return []
    
    def search_books(self, keyword: str) -> List[Book]:
        """
        搜尋書籍 (按書名或作者)
        
        Args:
            keyword: 搜尋關鍵字
            
        Returns:
            List[Book]: 符合條件的書籍列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_pattern = f"%{keyword}%"
                cursor.execute('''
                    SELECT id, title, author, year, status, rating 
                    FROM books 
                    WHERE title LIKE ? OR author LIKE ?
                    ORDER BY id
                ''', (search_pattern, search_pattern))
                rows = cursor.fetchall()
                
                books = []
                for row in rows:
                    book = Book(
                        title=row[1],
                        author=row[2],
                        year=row[3],
                        status=row[4],
                        rating=row[5],
                        book_id=row[0]
                    )
                    books.append(book)
                
                return books
                
        except sqlite3.Error as e:
            print(f"搜尋書籍失敗: {e}")
            return []
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        根據ID獲取書籍
        
        Args:
            book_id: 書籍ID
            
        Returns:
            Optional[Book]: 書籍物件或None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, title, author, year, status, rating FROM books WHERE id=?', (book_id,))
                row = cursor.fetchone()
                
                if row:
                    return Book(
                        title=row[1],
                        author=row[2],
                        year=row[3],
                        status=row[4],
                        rating=row[5],
                        book_id=row[0]
                    )
                return None
                
        except sqlite3.Error as e:
            print(f"獲取書籍失敗: {e}")
            return None
