"""
主視窗模組
包含 MainFrame 類別，負責主要的用戶界面和功能整合
"""

import csv
import wx
import wx.grid
from models import Book
from database import DatabaseManager
from dialogs import BookFormDialog


class MainFrame(wx.Frame):
    """主視窗類別"""
    
    def __init__(self):
        """初始化主視窗"""
        super().__init__(None, title="個人化書籍收藏管理系統", size=(1100, 700))
        
        # 初始化資料庫管理器
        self.db_manager = DatabaseManager()
        
        # 設置圖示和樣式
        self.SetMinSize((900, 600))
        
        # 創建狀態列
        self.CreateStatusBar()
        
        self.init_ui()
        self.setup_layout()
        self.load_books()
        
        # 置中顯示
        self.Center()
    
    def init_ui(self):
        """初始化UI元件"""
        # 創建主面板
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour(wx.Colour(248, 249, 250))
        
        # 創建標題區域
        title_panel = wx.Panel(main_panel)
        title_panel.SetBackgroundColour(wx.Colour(33, 37, 41))
        
        title_label = wx.StaticText(title_panel, label="個人化書籍收藏管理系統")
        title_font = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(wx.Colour(255, 255, 255))
        
        subtitle_label = wx.StaticText(title_panel, label="Book Collection Management System")
        subtitle_font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        subtitle_label.SetFont(subtitle_font)
        subtitle_label.SetForegroundColour(wx.Colour(180, 180, 180))
        
        # 統計資訊面板
        stats_panel = wx.Panel(main_panel)
        stats_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        # 統計標籤
        self.total_books_label = wx.StaticText(stats_panel, label="總書籍數: 0")
        self.read_books_label = wx.StaticText(stats_panel, label="已讀: 0")
        self.reading_books_label = wx.StaticText(stats_panel, label="閱讀中: 0")
        self.unread_books_label = wx.StaticText(stats_panel, label="未讀: 0")
        
        # 設置統計標籤樣式 - 統一字體確保大小一致
        stats_font = wx.Font(13, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        for label in [self.total_books_label, self.read_books_label, 
                     self.reading_books_label, self.unread_books_label]:
            label.SetFont(stats_font)
        
        self.total_books_label.SetForegroundColour(wx.Colour(33, 37, 41))
        self.read_books_label.SetForegroundColour(wx.Colour(40, 167, 69))
        self.reading_books_label.SetForegroundColour(wx.Colour(255, 165, 0))
        self.unread_books_label.SetForegroundColour(wx.Colour(220, 53, 69))
        
        # 工具面板
        tool_panel = wx.Panel(main_panel)
        tool_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        # 搜尋區域
        search_label = wx.StaticText(tool_panel, label="搜尋書籍:")
        search_font = wx.Font(11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        search_label.SetFont(search_font)
        
        self.search_text = wx.TextCtrl(tool_panel, style=wx.TE_PROCESS_ENTER, size=(300, 28))
        self.search_text.SetHint("輸入書名或作者...")
        
        self.search_btn = wx.Button(tool_panel, label="搜尋", size=(80, 28))
        self.refresh_btn = wx.Button(tool_panel, label="重新整理", size=(100, 28))
        
        # 設置按鈕顏色
        self.search_btn.SetBackgroundColour(wx.Colour(0, 123, 255))
        self.search_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.refresh_btn.SetBackgroundColour(wx.Colour(108, 117, 125))
        self.refresh_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        
        # 內容面板
        content_panel = wx.Panel(main_panel)
        content_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        # 書籍列表 (使用Grid)
        self.book_grid = wx.grid.Grid(content_panel)
        self.book_grid.CreateGrid(0, 6)
        
        # 設置Grid樣式
        self.book_grid.SetDefaultCellBackgroundColour(wx.Colour(255, 255, 255))
        self.book_grid.SetLabelBackgroundColour(wx.Colour(248, 249, 250))
        self.book_grid.SetLabelTextColour(wx.Colour(33, 37, 41))
        self.book_grid.SetGridLineColour(wx.Colour(222, 226, 230))
        
        # 設置列標題
        headers = ["ID", "書名", "作者", "年份", "狀態", "評分"]
        for i, header in enumerate(headers):
            self.book_grid.SetColLabelValue(i, header)
        
        # 設置列寬
        self.book_grid.SetColSize(0, 80)
        self.book_grid.SetColSize(1, 250)
        self.book_grid.SetColSize(2, 180)
        self.book_grid.SetColSize(3, 100)
        self.book_grid.SetColSize(4, 120)
        self.book_grid.SetColSize(5, 100)
        
        # 設置欄位標題對齊方式 (所有標題都置中)
        self.book_grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        # 操作按鈕面板
        button_panel = wx.Panel(main_panel)
        button_panel.SetBackgroundColour(wx.Colour(248, 249, 250))
        
        # 操作按鈕
        self.add_btn = wx.Button(button_panel, label="新增書籍", size=(120, 35))
        self.edit_btn = wx.Button(button_panel, label="編輯書籍", size=(120, 35))
        self.delete_btn = wx.Button(button_panel, label="刪除書籍", size=(120, 35))
        self.export_btn = wx.Button(button_panel, label="匯出清單", size=(120, 35))
        
        # 設置按鈕樣式
        self.add_btn.SetBackgroundColour(wx.Colour(40, 167, 69))
        self.add_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        
        self.edit_btn.SetBackgroundColour(wx.Colour(255, 193, 7))
        self.edit_btn.SetForegroundColour(wx.Colour(33, 37, 41))
        
        self.delete_btn.SetBackgroundColour(wx.Colour(220, 53, 69))
        self.delete_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        
        self.export_btn.SetBackgroundColour(wx.Colour(23, 162, 184))
        self.export_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        
        # 設置按鈕字體
        button_font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.export_btn]:
            btn.SetFont(button_font)
        
        # 儲存面板引用
        self.main_panel = main_panel
        self.title_panel = title_panel
        self.stats_panel = stats_panel
        self.tool_panel = tool_panel
        self.content_panel = content_panel
        self.button_panel = button_panel
        
        # 儲存標籤引用
        self.title_label = title_label
        self.subtitle_label = subtitle_label
        self.search_label = search_label
        
        # 綁定事件
        self.search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        self.refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_book)
        self.edit_btn.Bind(wx.EVT_BUTTON, self.on_edit_book)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete_book)
        self.export_btn.Bind(wx.EVT_BUTTON, self.on_export_books)
        self.search_text.Bind(wx.EVT_TEXT_ENTER, self.on_search)
    
    def setup_layout(self):
        """設置佈局"""
        # 主佈局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 標題區域佈局
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer.Add(self.title_label, 0, wx.ALL | wx.CENTER, 10)
        title_sizer.Add(self.subtitle_label, 0, wx.BOTTOM | wx.CENTER, 10)
        self.title_panel.SetSizer(title_sizer)
        
        # 統計區域佈局
        stats_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stats_sizer.Add(self.total_books_label, 1, wx.ALL | wx.CENTER, 10)
        stats_sizer.Add(wx.StaticLine(self.stats_panel, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        stats_sizer.Add(self.read_books_label, 1, wx.ALL | wx.CENTER, 10)
        stats_sizer.Add(wx.StaticLine(self.stats_panel, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        stats_sizer.Add(self.reading_books_label, 1, wx.ALL | wx.CENTER, 10)
        stats_sizer.Add(wx.StaticLine(self.stats_panel, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        stats_sizer.Add(self.unread_books_label, 1, wx.ALL | wx.CENTER, 10)
        self.stats_panel.SetSizer(stats_sizer)
        
        # 工具區域佈局
        tool_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tool_sizer.Add(self.search_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        tool_sizer.Add(self.search_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        tool_sizer.Add(self.search_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        tool_sizer.Add(self.refresh_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.tool_panel.SetSizer(tool_sizer)
        
        # 內容區域佈局
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        content_sizer.Add(self.book_grid, 1, wx.ALL | wx.EXPAND, 10)
        self.content_panel.SetSizer(content_sizer)
        
        # 按鈕區域佈局
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.add_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.edit_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.delete_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.export_btn, 0, wx.ALL, 5)
        button_sizer.AddStretchSpacer()
        self.button_panel.SetSizer(button_sizer)
        
        # 主面板佈局
        main_sizer.Add(self.title_panel, 0, wx.EXPAND)
        main_sizer.Add(self.stats_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        main_sizer.Add(self.tool_panel, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.content_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        main_sizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL, 5)
        
        self.main_panel.SetSizer(main_sizer)
    
    def load_books(self, books=None):
        """載入書籍到列表"""
        if books is None:
            books = self.db_manager.get_all_books()
        
        # 清空現有資料
        if self.book_grid.GetNumberRows() > 0:
            self.book_grid.DeleteRows(0, self.book_grid.GetNumberRows())
        
        # 添加新資料
        for i, book in enumerate(books):
            self.book_grid.AppendRows(1)
            row = self.book_grid.GetNumberRows() - 1
            
            self.book_grid.SetCellValue(row, 0, str(book.id))
            self.book_grid.SetCellValue(row, 1, book.title)
            self.book_grid.SetCellValue(row, 2, book.author)
            self.book_grid.SetCellValue(row, 3, str(book.year))
            self.book_grid.SetCellValue(row, 4, book.status)
            self.book_grid.SetCellValue(row, 5, f"{book.rating}★" if book.rating > 0 else "未評分")
            
            # 設置儲存格對齊方式
            for col in range(6):
                if col == 1 or col == 2:  # 書名和作者靠左對齊
                    self.book_grid.SetCellAlignment(row, col, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
                else:  # 其他欄位置中對齊
                    self.book_grid.SetCellAlignment(row, col, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            
            # 設置行顏色 (交替背景色)
            if i % 2 == 0:
                for col in range(6):
                    self.book_grid.SetCellBackgroundColour(row, col, wx.Colour(248, 249, 250))
            
            # 根據狀態設置特殊顏色
            status_colors = {
                "已讀": wx.Colour(212, 237, 218),
                "閱讀中": wx.Colour(255, 228, 181),
                "未讀": wx.Colour(248, 215, 218)
            }
            if book.status in status_colors:
                self.book_grid.SetCellBackgroundColour(row, 4, status_colors[book.status])
            
            # 設置為只讀
            for col in range(6):
                self.book_grid.SetReadOnly(row, col)
        
        self.book_grid.AutoSizeColumns()
        self.update_statistics()
    
    def update_statistics(self):
        """更新統計資訊"""
        books = self.db_manager.get_all_books()
        
        total_count = len(books)
        read_count = len([b for b in books if b.status == "已讀"])
        reading_count = len([b for b in books if b.status == "閱讀中"])
        unread_count = len([b for b in books if b.status == "未讀"])
        
        self.total_books_label.SetLabel(f"總書籍數: {total_count}")
        self.read_books_label.SetLabel(f"已讀: {read_count}")
        self.reading_books_label.SetLabel(f"閱讀中: {reading_count}")
        self.unread_books_label.SetLabel(f"未讀: {unread_count}")
        
        # 更新狀態列訊息 (如果狀態列存在)
        if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
            if total_count > 0:
                read_percentage = round((read_count / total_count) * 100, 1)
                self.SetStatusText(f"共 {total_count} 本書籍 | 已讀進度: {read_percentage}% | 最近更新: {wx.DateTime.Now().Format('%H:%M:%S')}")
            else:
                self.SetStatusText("歡迎使用個人化書籍收藏管理系統 | 點擊「新增書籍」開始建立您的收藏")
    
    def get_selected_book_id(self):
        """獲取選中的書籍ID"""
        selected_rows = self.book_grid.GetSelectedRows()
        if not selected_rows:
            # 檢查是否有選中的單元格
            if self.book_grid.GetGridCursorRow() >= 0:
                selected_rows = [self.book_grid.GetGridCursorRow()]
            else:
                return None
        
        if selected_rows:
            row = selected_rows[0]
            book_id_str = self.book_grid.GetCellValue(row, 0)
            try:
                return int(book_id_str)
            except ValueError:
                return None
        return None
    
    def on_search(self, event):
        """搜尋事件處理"""
        keyword = self.search_text.GetValue().strip()
        if keyword:
            books = self.db_manager.search_books(keyword)
            self.load_books(books)
            if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
                self.SetStatusText(f"搜尋結果: 找到 {len(books)} 本相關書籍")
        else:
            self.on_refresh(event)
    
    def on_refresh(self, event):
        """重新整理事件處理"""
        self.load_books()
        self.search_text.SetValue("")
        if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
            self.SetStatusText("已重新載入書籍列表")
    
    def on_add_book(self, event):
        """新增書籍事件處理"""
        dialog = BookFormDialog(self, "新增書籍")
        
        if dialog.ShowModal() == wx.ID_OK:
            book = dialog.get_book()
            if self.db_manager.add_book(book):
                wx.MessageBox("書籍新增成功!", "成功", wx.OK | wx.ICON_INFORMATION)
                self.load_books()
                if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
                    self.SetStatusText(f"成功新增書籍: {book.title}")
            else:
                wx.MessageBox("書籍新增失敗，請檢查輸入資料", "錯誤", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def on_edit_book(self, event):
        """編輯書籍事件處理"""
        book_id = self.get_selected_book_id()
        if book_id is None:
            wx.MessageBox("請先選擇要編輯的書籍", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        
        book = self.db_manager.get_book_by_id(book_id)
        if book is None:
            wx.MessageBox("找不到指定的書籍", "錯誤", wx.OK | wx.ICON_ERROR)
            return
        
        dialog = BookFormDialog(self, "編輯書籍", book)
        
        if dialog.ShowModal() == wx.ID_OK:
            updated_book = dialog.get_book()
            if self.db_manager.update_book(updated_book):
                wx.MessageBox("書籍更新成功!", "成功", wx.OK | wx.ICON_INFORMATION)
                self.load_books()
                if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
                    self.SetStatusText(f"成功更新書籍: {updated_book.title}")
            else:
                wx.MessageBox("書籍更新失敗，請檢查輸入資料", "錯誤", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def on_delete_book(self, event):
        """刪除書籍事件處理"""
        book_id = self.get_selected_book_id()
        if book_id is None:
            wx.MessageBox("請先選擇要刪除的書籍", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        
        # 確認對話框
        result = wx.MessageBox("確定要刪除選中的書籍嗎？", "確認刪除", wx.YES_NO | wx.ICON_QUESTION)
        
        if result == wx.YES:
            if self.db_manager.delete_book(book_id):
                wx.MessageBox("書籍刪除成功!", "成功", wx.OK | wx.ICON_INFORMATION)
                self.load_books()
                if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
                    self.SetStatusText(f"已刪除書籍 (ID: {book_id})")
            else:
                wx.MessageBox("書籍刪除失敗", "錯誤", wx.OK | wx.ICON_ERROR)
    
    def on_export_books(self, event):
        """匯出書籍清單事件處理"""
        # 選擇儲存位置
        wildcard = "CSV files (*.csv)|*.csv"
        dialog = wx.FileDialog(self, "儲存書籍清單", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            
            try:
                books = self.db_manager.get_all_books()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # 寫入標題行
                    writer.writerow(['ID', '書名', '作者', '出版年份', '閱讀狀態', '評分'])
                    
                    # 寫入書籍資料
                    for book in books:
                        writer.writerow([
                            book.id,
                            book.title,
                            book.author,
                            book.year,
                            book.status,
                            book.rating
                        ])
                
                wx.MessageBox(f"書籍清單已成功匯出到：\n{file_path}", "匯出成功", wx.OK | wx.ICON_INFORMATION)
                if hasattr(self, 'GetStatusBar') and self.GetStatusBar():
                    self.SetStatusText(f"已匯出 {len(books)} 本書籍到 CSV 檔案")
                
            except Exception as e:
                wx.MessageBox(f"匯出失敗：{str(e)}", "錯誤", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
