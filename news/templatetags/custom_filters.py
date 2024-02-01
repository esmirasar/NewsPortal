from django import template

register = template.Library()

censorship_list = ['эпицентр', 'направление', 'количество']




@register.filter()
def censor(word):
    news = ''
    for i in word.split():
        if i in censorship_list:
            news += i[0] + '*' * (len(i) - 1) + ' '
        else:
            news += i + ' '
    return news

