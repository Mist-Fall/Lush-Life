# 高铁余票监控助手 - 课程实践版
import tkinter as tk
from tkinter import messagebox
import time
import random

# ========== 配置项 ==========
# 演示模式：True=模拟数据（脱机可运行，上课演示推荐）
DEMO_MODE = True
# 自动刷新间隔（毫秒）
REFRESH_INTERVAL = 5000


def get_mock_tickets():
    """生成模拟车次数据，用于课堂演示"""
    train_list = []
    for i in range(6):
        hour = random.randint(7, 18)
        minute = random.randint(0, 59)
        duration = random.randint(2, 5)
        seat_status = random.choice(["有", "无", "2张", "5张", "11张"])
        train_list.append({
            "train_no": f"G{random.randint(100, 399)}",
            "depart": f"{hour:02d}:{minute:02d}",
            "arrive": f"{hour + duration:02d}:{minute:02d}",
            "seat": seat_status
        })
    return sorted(train_list, key=lambda x: x["depart"])


class TicketMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高铁余票监控助手")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        self.is_monitoring = False

        # 行程输入区
        input_frame = tk.LabelFrame(root, text="行程信息", padx=10, pady=10)
        input_frame.pack(padx=15, pady=10, fill="x")

        tk.Label(input_frame, text="出发地：").grid(row=0, column=0)
        self.from_entry = tk.Entry(input_frame, width=12)
        self.from_entry.insert(0, "南京")
        self.from_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="目的地：").grid(row=0, column=2)
        self.to_entry = tk.Entry(input_frame, width=12)
        self.to_entry.insert(0, "上海")
        self.to_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="出行日期：").grid(row=1, column=0, pady=8)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.insert(0, "2026-10-30")
        self.date_entry.grid(row=1, column=1, padx=5)

        # 功能按钮区
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.query_btn = tk.Button(btn_frame, text="查询余票", width=12, command=self.query_tickets)
        self.query_btn.grid(row=0, column=0, padx=10)

        self.monitor_btn = tk.Button(btn_frame, text="开启监控", width=12, command=self.toggle_monitor)
        self.monitor_btn.grid(row=0, column=1, padx=10)

        # 结果显示区
        result_frame = tk.LabelFrame(root, text="查询结果", padx=5, pady=5)
        result_frame.pack(padx=15, pady=5, fill="both", expand=True)

        self.result_text = tk.Text(result_frame, font=("微软雅黑", 10))
        self.result_text.pack(fill="both", expand=True)

        # 状态栏
        self.status_bar = tk.Label(root, text="就绪", anchor="w", bd=1, relief="sunken")
        self.status_bar.pack(side="bottom", fill="x")

    def query_tickets(self):
        """执行余票查询"""
        from_city = self.from_entry.get().strip()
        to_city = self.to_entry.get().strip()
        date = self.date_entry.get().strip()

        if not all([from_city, to_city, date]):
            messagebox.showwarning("提示", "请填写完整的行程信息")
            return

        self.status_bar.config(text="正在查询中...")
        self.root.update()

        if DEMO_MODE:
            time.sleep(0.3)
            tickets = get_mock_tickets()
        else:
            tickets = []

        # 渲染结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"查询时间：{time.strftime('%H:%M:%S')}\n")
        self.result_text.insert(tk.END, "-" * 48 + "\n")
        self.result_text.insert(tk.END, f"{'车次':<6}{'出发':<6}{'到达':<6}{'二等座余票'}\n")
        self.result_text.insert(tk.END, "-" * 48 + "\n")

        has_ticket = False
        for t in tickets:
            line = f"{t['train_no']:<6}{t['depart']:<6}{t['arrive']:<6}{t['seat']}\n"
            self.result_text.insert(tk.END, line)
            if t["seat"] != "无":
                has_ticket = True

        self.status_bar.config(text=f"查询完成，共 {len(tickets)} 趟车次")

        if self.is_monitoring and has_ticket:
            messagebox.showinfo("有票提醒", "检测到可用余票！\n请尽快前往12306官方渠道购票")
            self.toggle_monitor()

    def toggle_monitor(self):
        """切换自动监控状态"""
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.monitor_btn.config(text="停止监控")
            self.status_bar.config(text=f"监控中，每{REFRESH_INTERVAL//1000}秒刷新一次")
            self.auto_refresh()
        else:
            self.monitor_btn.config(text="开启监控")
            self.status_bar.config(text="监控已停止")

    def auto_refresh(self):
        """自动刷新回调"""
        if self.is_monitoring:
            self.query_tickets()
            self.root.after(REFRESH_INTERVAL, self.auto_refresh)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketMonitorApp(root)
    root.mainloop()
