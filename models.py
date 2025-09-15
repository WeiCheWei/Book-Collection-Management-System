"""
書籍模型模組
包含 Book 類別的定義和相關方法
"""

from typing import Tuple


class Book:
    """書籍類別 - 定義書籍物件的屬性和方法"""
    
    def __init__(self, title: str, author: str, year: int, status: str = "未讀", rating: int = 0, book_id: int = None):
        """
        初始化書籍物件
        
        Args:
            title: 書名
            author: 作者
            year: 出版年份
            status: 閱讀狀態 (未讀/閱讀中/已讀)
            rating: 評分 (1-5分，0表示未評分)
            book_id: 書籍ID (資料庫主鍵)
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.rating = rating
    
    def validate(self) -> Tuple[bool, str]:
        """
        驗證書籍資料的有效性
        
        Returns:
            Tuple[bool, str]: (是否有效, 錯誤訊息)
        """
        if not self.title.strip():
            return False, "書名不能為空"
        
        if not self.author.strip():
            return False, "作者不能為空"
        
        if not isinstance(self.year, int) or self.year < 0 or self.year > 2025:
            return False, "出版年份必須是有效的數字(0-2025)"
        
        if self.status not in ["未讀", "閱讀中", "已讀"]:
            return False, "閱讀狀態必須是：未讀、閱讀中、已讀 其中之一"
        
        if not isinstance(self.rating, int) or self.rating < 0 or self.rating > 5:
            return False, "評分必須是0-5之間的整數"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """將書籍物件轉換為字典"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
            'rating': self.rating
        }
    
    def __str__(self) -> str:
        """字串表示法"""
        return f"《{self.title}》- {self.author} ({self.year}) [{self.status}] {self.rating}★"
