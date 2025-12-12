import csv
from django.shortcuts import render

def show(request):
    books = []
    with open('books_dummy.csv', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f) #辞書型にしている
        for row in reader:

            # 書籍名の「。」だけ空白に置換
            if '書籍名' in row:
                row['書籍名'] = row['書籍名'].replace('。', ' ')

            # ISBN が数字として読まれる問題への対応
            row['ISBN'] = str(row['ISBN'])

            books.append(row)
    
    return render(request, 'booklist/index.html', {'books': books})
