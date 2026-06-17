"""番茄钟 — tkinter 实现的简易 Pomodoro 计时器。

- 25 分钟专注 / 5 分钟休息，交替循环
- 开始/暂停 按钮控制计时
- 底部计数完成的番茄数
"""
import tkinter as tk
from tkinter import font

# ── 常量 ────────────────────────────────────────────
WORK = 25 * 60    # 专注时长（秒）
BREAK = 5 * 60    # 休息时长（秒）

# ── 全局状态 ────────────────────────────────────────
remaining = WORK   # 当前阶段剩余秒数
is_work = True     # True=专注阶段, False=休息阶段
running = False    # 计时器是否在跑
count = 0          # 已完成番茄数
job = None         # tk after 的 job id，用于取消定时


def fmt(s):
    """秒数 → MM:SS 字符串"""
    return f"{s // 60:02d}:{s % 60:02d}"


def tick():
    """每秒回调：倒计时 -1，到 0 时自动切换模式"""
    global remaining, job
    remaining -= 1
    timer_label.config(text=fmt(remaining))
    root.title(f"{fmt(remaining)} — {'专注' if is_work else '休息'}")
    if remaining <= 0:
        switch_mode()
    else:
        job = root.after(1000, tick)  # 1 秒后再调一次


def switch_mode():
    """切换专注↔休息，重置计时，更新 UI"""
    global is_work, remaining, count, job
    if job:
        root.after_cancel(job)
        job = None
    if is_work:
        count += 1                      # 完成一个专注周期
        count_label.config(text=str(count))
    is_work = not is_work
    remaining = WORK if is_work else BREAK
    timer_label.config(text=fmt(remaining))
    label.config(text='专注' if is_work else '休息',
                 fg=RED if is_work else GREEN)
    btn.config(text='开始')
    root.title('番茄钟')


def toggle():
    """开始/暂停 按钮回调"""
    global running, job
    if running:
        root.after_cancel(job)
        job = None
        running = False
        btn.config(text='继续')
    else:
        job = root.after(1000, tick)
        running = True
        btn.config(text='暂停')


# ── 窗口 ────────────────────────────────────────────
root = tk.Tk()
root.title('番茄钟')
root.geometry('400x360')
root.configure(bg='#f5ecec')
root.resizable(False, False)

# ── 颜色 ────────────────────────────────────────────
BG = '#f5ecec'      # 暖白背景
FG = '#3d2d2d'      # 深棕文字
RED = '#c04040'      # 番茄红（专注）
GREEN = '#5a8a6a'    # 鼠尾草绿（休息）
MUTED = '#a09090'    # 辅助文字

# ── 模式标签（专注/休息） ──────────────────────────
label = tk.Label(root, text='专注', font=('', 16), bg=BG, fg=RED)
label.pack(pady=(30, 0))

# ── 计时器数字 ──────────────────────────────────────
timer_font = font.Font(family='TkFixedFont', size=64, weight='normal')
timer_label = tk.Label(root, text=fmt(remaining), font=timer_font,
                       bg=BG, fg=FG)
timer_label.pack(pady=5)

# ── 开始/暂停 按钮 ──────────────────────────────────
btn = tk.Button(root, text='开始', font=('', 14), fg=RED, bg=BG,
                activebackground=RED, activeforeground='#fff',
                borderwidth=2, relief='solid', padx=30, pady=6,
                cursor='hand2', command=toggle)
btn.pack(pady=10)

# ── 底部计数 ────────────────────────────────────────
count_frame = tk.Frame(root, bg=BG)
count_frame.pack(pady=(20, 0))
tk.Label(count_frame, text='已完成 ', font=('', 12), bg=BG,
         fg=MUTED).pack(side='left')
count_label = tk.Label(count_frame, text='0', font=('', 12, 'bold'),
                       bg=BG, fg=RED)
count_label.pack(side='left')
tk.Label(count_frame, text=' 个番茄', font=('', 12), bg=BG,
         fg=MUTED).pack(side='left')

root.mainloop()