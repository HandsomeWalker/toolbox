import base64
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

arr = []
copyIdx = 0

#设置文本只能输入数字
def is_number(content):
  # 如果不加上==""的话，就会发现删不完。总会剩下一个数字 isdigit函数：isdigit函数方法检测字符串是否只由数字组成。
  if content.isdigit():
    return True
  else:
    return False
def to_base64(file):
  with open(file, 'rb') as fileObj:
    image_data = fileObj.read()
    base64_data = base64.b64encode(image_data)
    return base64_data.decode()

def to_file(txt, file):
  base64_data = txt
  ori_image_data = base64.b64decode(base64_data)
  fout = open(file, 'wb')
  fout.write(ori_image_data)
  fout.close()
  lb1.config(text = '已保存')

def center_window(w, h):
  # 获取屏幕 宽、高
  ws = root.winfo_screenwidth()
  hs = root.winfo_screenheight()
  # 计算 x, y 位置
  x = (ws/2) - (w/2)
  y = (hs/2) - (h/2)
  root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def select():
  global copyIdx
  filename = filedialog.askopenfilename()
  if filename != '':
    arr.clear()
    copyIdx = 0
    curr_file.config(text = '当前文件：%s' % filename)
    b64 = to_base64(filename)
    lb64 = len(b64)
    i = 0
    real_name = filename.split('/')[-1]
    inputB64Len = input1.get()
    isNum = is_number(input1.get())
    if isNum:
      inputB64Len = int(inputB64Len)
    else:
      inputB64Len = 1000000

    if lb64 > inputB64Len:
      while i <= lb64:
        if i + inputB64Len > lb64:
          arr.append(b64[i:lb64] + '/' + real_name)
          break
        else:
          arr.append(b64[i:i + inputB64Len])
          i += inputB64Len
    else:
      arr.append(b64 + '/' + real_name)
    lb1.config(text = '已复制全部，总共%d段' % len(arr))
    root.clipboard_clear()
    root.clipboard_append(b64 + '/' + real_name)
    root.update()

def save():
  try:
    txt = root.clipboard_get()
    txt_arr = txt.split('/')
    real_name = txt_arr.pop()
    real_name_arr = real_name.split('.')
    filename = filedialog.asksaveasfilename(initialfile = real_name_arr[0], defaultextension = '.' + real_name_arr[1], filetypes = [(real_name_arr[1], '.' + real_name_arr[1])])
    if filename != '':
      to_file('/'.join(txt_arr), filename)
  except Exception:
    messagebox.showerror(title = 'error', message = '获取失败')

def disable(comp):
  comp['state'] = DISABLED

def mins():
  global copyIdx
  if copyIdx > 0:
    copyIdx -= 1
    lb2.config(text = copyIdx + 1)

def plus():
  global copyIdx
  if copyIdx < len(arr) - 1:
    copyIdx += 1
    lb2.config(text = copyIdx + 1)
def copy():
  if len(arr) == 0:
    return
  root.clipboard_clear()
  root.clipboard_append(arr[copyIdx])
  lb1.config(text = '已复制第%d段，总共%d段' % (copyIdx + 1, len(arr)))

def copy_all():
  if len(arr) == 0:
    return
  root.clipboard_clear()
  root.clipboard_append(''.join(arr))
  lb1.config(text = '已复制全部，总共%d段' % len(arr))

root = Tk()
root.title('b64tool')
center_window(500, 300)
btn1 = Button(root, text="选择文件", command = select)
btn1.grid(column = 0, row = 1)
btn2 = Button(root, text = '获取文件', command = save)
btn2.grid(column = 1, row = 1)
btn3 = Button(root, width = 2, text = '-', command = mins)
btn3.grid(column = 3, row = 1)
lb2 = Label(root, text = '1')
lb2.grid(column = 4, row = 1)
btn4 = Button(root, width = 2, text = '+', command = plus)
btn4.grid(column = 5, row = 1)
btn5 = Button(root, text = '复制', command = copy)
btn5.grid(column = 7, row = 1)
btn6 = Button(root, text = '复制全部', command = copy_all)
btn6.grid(column = 8, row = 1)
curr_file = Label(root, text = '')
curr_file.grid(columnspan = 100, row = 2)
lb1 = Label(root, text = '')
lb1.grid(row = 3)
inputLb = Label(root, text = '分段base64长度(默认100W):')
inputLb.grid(column = 0, row = 4)
input1 = Entry(root, bd = 2, exportselection = False)
input1.grid(column = 1, row = 4)
input1.insert(0, 1)
for i in range(1, 7):
    input1.insert(i, 0)
root.mainloop()
