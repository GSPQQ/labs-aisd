with open("vod.txt",'r', encoding='utf-8') as f:
    stroki=f.readline()
numbers=stroki.split(',')  
flag=0
def num_to_words(digits):
    digit_words = {'0': 'ноль','1': 'один','2': 'два','3': 'три', '4': 'четыре','5': 'пять','6': 'шесть','7': 'семь',}
    return digit_words.get(digits, "неизвестно") 
for num in numbers:
    if  all('-1'< digit < '8' for digit in num) and int(num)%2==0: 
        if (num[0] == '3' and num[-2] == '3') or num.startswith('333'):
            flag+=1
            if flag%5==0:
                print(" ".join(num_to_words(digits) for digits in num))
            else: print(num)