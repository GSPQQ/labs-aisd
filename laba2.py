import re
def num_to_words(digit):
    digit_words = {'0': 'ноль','1': 'один','2': 'два','3': 'три', '4': 'четыре','5': 'пять','6': 'шесть','7': 'семь'}
    return digit_words.get(digit, "неизвестно")
with open("vod.txt", 'r', encoding='utf-8') as f:
    stroki=f.readline()
numbers=stroki.split(',') 
flag = 0
for num in numbers:
    if re.match('333[0-7]+[0,2,4,6]', num) or re.match('3[0-7]+3[0,2,4,6]',num) :
        flag += 1
        output = " ".join(num_to_words(digit) for digit in num) if flag % 5 == 0 else num
        print(output)