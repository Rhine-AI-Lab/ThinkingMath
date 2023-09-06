import random
from general_utils import *

eg = """
(((36+(8*(72-4)))/2)+7)
27*[8+(45-3)/6]+10
16*[32+45*(3+6)]/4+9
35+10*(15+32)/2-3
"""

ma_len = 8
operates = ['+', '-', '*', '/']

ras = []
fhs = []
kh = []

for i in range(ma_len):
    ras.append(0)
    if i != 0:
        fhs.append(random_str(operates))

for i in range(ma_len - 1):
    if i not in kh and i + 2 not in kh and i + 1 not in kh:
        if fhs[i] == '-' and len(fhs) > i + 1 and fhs[i + 1] not in ['*', '/']:
            kh.append(i + 1)
        if fhs[i] == '/' and len(fhs) > i + 1:
            kh.append(i + 1)
    if i - 1 not in kh and i + 1 not in kh and i not in kh:
        if fhs[i] in ['+', '-'] and len(fhs) > i + 1 and fhs[i + 1] in ['*', '/']:
            kh.append(i)
        if fhs[i] in ['+', '-'] and i > 0 and fhs[i - 1] in ['*', '/']:
            kh.append(i)

print(kh)


print('先计算括号内内容')
khr = {}
pm_ws = [1, 3]
td_ws = [1, 3]
for i in kh:
    print(fhs[i])
    if fhs[i] == '+':
        ras[i] = random_len_int(random.randint(pm_ws[0], pm_ws[1]))
        ras[i+1] = random_len_int(random.randint(pm_ws[0], pm_ws[1]))
    if fhs[i] == '-':
        ras[i] = random_len_int(random.randint(pm_ws[0], pm_ws[1]))
        ras[i+1] = random.randint(10 ** (pm_ws[0] - 1), ras[i])
    if fhs[i] == '*':
        ras[i] = random_len_int(random.randint(td_ws[0], td_ws[1]))
        ras[i+1] = random_len_int(random.randint(td_ws[0], td_ws[1]))
    if fhs[i] == '/':
        ras[i+1] = random_len_int(random.randint(td_ws[0], td_ws[1]))
        ras[i] = ras[i+1] * random_len_int(random.randint(td_ws[0], td_ws[1]))

expression = str(ras[0])
if 0 in kh:
    expression = '( ' + expression
for i in range(len(fhs)):
    if i - 1 in kh:
        expression += ' )'
    expression += f' {fhs[i]}'
    if i + 1 in kh:
        expression += ' ('
    expression += f' {ras[i + 1]}'
if len(fhs) - 1 in kh:
    expression += ' )'
print(expression)


try:
    print('=', eval(expression))
except:
    print('= NaN')
    pass




