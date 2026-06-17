import tkinter as tk
from tkinter import font

WORK = 25 * 60
BREAK = 5 * 60

remaining = WORK
is_work = True
running = False
count = 0
job = None


def fmt(s):
    return f"{s // 60:02d}:{s % 60:02d}"


def tick():
    global remaining, job
    remaining -= 1
    timer_label.config(text=fmt(remaining))
    root.title(f"{fmt(remaining)} — {'专注' if is_work else '休息'}")
    if remaining <= 0:
        switch_mode()
    else:
        job = root.after(1000, tick)


def switch_mode():
    global is_work, remaining, count, job
    if job:
        root.after_cancel(job)
        job = None
    if is_work:
        count += 1
        count_label.config(text=str(count))
    is_work = not is_work
    remaining = WORK if is_work else BREAK
    timer_label.config(text=fmt(remaining))
    label.config(text='专注' if is_work else '休息',
                 fg='#e94560' if is_work else '#0f3460')
    btn.config(text='开始')
    root.title('番茄钟')


def toggle():
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


root = tk.Tk()
root.title('番茄钟')
root.geometry('400x360')
root.configure(bg='#1a1a2e')
root.resizable(False, False)

label = tk.Label(root, text='专注', font=('', 16), bg='#1a1a2e', fg='#e94560')
label.pack(pady=(30, 0))

timer_font = font.Font(family='TkFixedFont', size=64, weight='normal')
timer_label = tk.Label(root, text=fmt(remaining), font=timer_font,
                       bg='#1a1a2e', fg='#eee')
timer_label.pack(pady=5)

btn = tk.Button(root, text='开始', font=('', 14), fg='#e94560', bg='#1a1a2e',
                activebackground='#e94560', activeforeground='#fff',
                borderwidth=2, relief='solid', padx=30, pady=6,
                cursor='hand2', command=toggle)
btn.pack(pady=10)

count_frame = tk.Frame(root, bg='#1a1a2e')
count_frame.pack(pady=(20, 0))
tk.Label(count_frame, text='已完成 ', font=('', 12), bg='#1a1a2e',
         fg='#555').pack(side='left')
count_label = tk.Label(count_frame, text='0', font=('', 12, 'bold'),
                       bg='#1a1a2e', fg='#e94560')
count_label.pack(side='left')
tk.Label(count_frame, text=' 个番茄', font=('', 12), bg='#1a1a2e',
         fg='#555').pack(side='left')

root.mainloop()
