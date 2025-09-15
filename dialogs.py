"""
對話框模組
包含 BookFormDialog 類別，用於新增和編輯書籍的表單界面
"""

import wx
from models import Book


class BookFormDialog(wx.Dialog):
    """書籍表單對話框 - 用於新增和編輯書籍"""
    
    def __init__(self, parent, title="書籍資訊", book=None):
        """
        初始化書籍表單對話框
        
        Args:
            parent: 父視窗
            title: 對話框標題
            book: 書籍物件 (編輯模式時使用)
        """
        super().__init__(parent, title=title, size=(400, 300))
        
        self.book = book
        self.is_edit_mode = book is not None
        
        self.init_ui()
        self.setup_layout()
        
        if self.is_edit_mode:
            self.load_book_data()
    
    def init_ui(self):
        """初始化UI元件"""
        # 創建輸入欄位
        self.title_text = wx.TextCtrl(self)
        self.author_text = wx.TextCtrl(self)
        self.year_text = wx.TextCtrl(self)
        
        # 閱讀狀態選擇
        status_choices = ["未讀", "閱讀中", "已讀"]
        self.status_choice = wx.Choice(self, choices=status_choices)
        self.status_choice.SetSelection(0)
        
        # 評分選擇
        rating_choices = ["0 (未評分)", "1★", "2★", "3★", "4★", "5★"]
        self.rating_choice = wx.Choice(self, choices=rating_choices)
        self.rating_choice.SetSelection(0)
        
        # 按鈕
        self.ok_btn = wx.Button(self, wx.ID_OK, "確定")
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL, "取消")
        
        # 綁定事件
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
    
    def setup_layout(self):
        """設置佈局"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 表單區域
        form_sizer = wx.FlexGridSizer(5, 2, 10, 10)
        form_sizer.AddGrowableCol(1)
        
        form_sizer.Add(wx.StaticText(self, label="書名:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.title_text, 1, wx.EXPAND)
        
        form_sizer.Add(wx.StaticText(self, label="作者:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.author_text, 1, wx.EXPAND)
        
        form_sizer.Add(wx.StaticText(self, label="出版年份:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.year_text, 1, wx.EXPAND)
        
        form_sizer.Add(wx.StaticText(self, label="閱讀狀態:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.status_choice, 1, wx.EXPAND)
        
        form_sizer.Add(wx.StaticText(self, label="評分:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.rating_choice, 1, wx.EXPAND)
        
        # 按鈕區域
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.ok_btn, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.cancel_btn, 0)
        
        # 主佈局
        main_sizer.Add(form_sizer, 1, wx.ALL | wx.EXPAND, 20)
        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 20)
        
        self.SetSizer(main_sizer)
    
    def load_book_data(self):
        """載入書籍資料 (編輯模式)"""
        if self.book:
            self.title_text.SetValue(self.book.title)
            self.author_text.SetValue(self.book.author)
            self.year_text.SetValue(str(self.book.year))
            
            # 設置狀態選擇
            status_map = {"未讀": 0, "閱讀中": 1, "已讀": 2}
            self.status_choice.SetSelection(status_map.get(self.book.status, 0))
            
            # 設置評分選擇
            self.rating_choice.SetSelection(self.book.rating)
    
    def on_ok(self, event):
        """確定按鈕事件處理"""
        try:
            # 獲取輸入值
            title = self.title_text.GetValue().strip()
            author = self.author_text.GetValue().strip()
            year_str = self.year_text.GetValue().strip()
            
            # 驗證年份
            try:
                year = int(year_str)
            except ValueError:
                wx.MessageBox("出版年份必須是數字", "輸入錯誤", wx.OK | wx.ICON_ERROR)
                return
            
            # 獲取狀態和評分
            status_choices = ["未讀", "閱讀中", "已讀"]
            status = status_choices[self.status_choice.GetSelection()]
            rating = self.rating_choice.GetSelection()
            
            # 創建書籍物件
            if self.is_edit_mode:
                book = Book(title, author, year, status, rating, self.book.id)
            else:
                book = Book(title, author, year, status, rating)
            
            # 驗證書籍資料
            is_valid, error_msg = book.validate()
            if not is_valid:
                wx.MessageBox(error_msg, "輸入錯誤", wx.OK | wx.ICON_ERROR)
                return
            
            self.book = book
            self.EndModal(wx.ID_OK)
            
        except Exception as e:
            wx.MessageBox(f"處理資料時發生錯誤: {str(e)}", "錯誤", wx.OK | wx.ICON_ERROR)
    
    def get_book(self):
        """獲取書籍物件"""
        return self.book
