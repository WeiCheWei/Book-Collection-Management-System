import wx
from main_window import MainFrame


class BookCollectionApp(wx.App):
    """應用程式主類別"""
    
    def OnInit(self):
        """應用程式初始化"""
        try:
            frame = MainFrame()
            frame.Show()
            return True
        except Exception as e:
            wx.MessageBox(f"應用程式啟動失敗：{str(e)}", "錯誤", wx.OK | wx.ICON_ERROR)
            return False


def main():
    """主函數"""
    app = BookCollectionApp()
    app.MainLoop()


if __name__ == "__main__":
    main()