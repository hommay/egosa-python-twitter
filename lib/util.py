from functools import reduce

# 文字列検索用
def search_or(search_words, target_string):
    result_list = [ 1 if i in target_string else 0 for i in search_words ]
    result = reduce(lambda x, y: x+y, result_list)
    return False if result == 0 else True
