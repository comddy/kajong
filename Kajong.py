from collections import Counter
from itertools import product
import time, os

'''
answer:
1.AABBBCCCdd
2.AABBBCCCde
4.AXBBBCCCde

1.ADad
2.cf
4.ABCbcf
'''

def isValid(sequence):
    """
    :param sequence: 要判断的字符串
    :return bool
    判断字符串序列是否是Katte
	只判断不处理
    """

    n = len(sequence)
    small = [0] * n
    big = [0] * n
    for c in sequence:
        if c >= 'a':
            index = (ord(c) - 97) % n
            small[index] += 1
        else:
            index = (ord(c) - 65) % n
            big[index] += 1

    # print(small)
    # print(big)
    res = False

    def dfs(count, small, big, index, pair=False):
        nonlocal res
        if res: return
        if count == 0:
            res = True
            return
        elif index >= len(small):
            return

        # 四个直接返回
        s, b = small[index], big[index]
        if s > 3 or b > 3: return

        # nothing s 0 b 0
        if s == 0 and b == 0:
            dfs(count, small, big, index + 1, pair)

        # 不考虑Straight
        if s == 3 or b == 3:
            small[index] = 0 if s == 3 else s
            big[index] = 0 if b == 3 else b
            dfs(count - 1, small, big, index, pair)
            small[index] = s
            big[index] = b
        if (s == 1 and b == 2) or (s == 2 and b == 1):
            small[index] = 0
            big[index] = 0
            dfs(count - 1, small, big, index, pair)
            small[index] = s
            big[index] = b
        if (s == 2 and b == 0) or (s == 0 and b == 2):
            if pair:
                return
            else:
                small[index] = 0
                big[index] = 0
                dfs(count - 1, small, big, index, True)
                small[index] = s
                big[index] = b

        # 考虑Straight
        if index + 3 <= 11 and min(small[index], small[index + 1], small[index + 2]) > 0 and big[index] == 0:
            small[index] -= 1
            small[index + 1] -= 1
            small[index + 2] -= 1
            dfs(count - 1, small, big, index, pair)
            small[index] += 1
            small[index + 1] += 1
            small[index + 2] += 1
        if index + 3 <= 11 and min(big[index], big[index + 1], big[index + 2]) > 0 and small[index] == 0:
            big[index] -= 1
            big[index + 1] -= 1
            big[index + 2] -= 1
            dfs(count - 1, small, big, index, pair)
            big[index] += 1
            big[index + 1] += 1
            big[index + 2] += 1

    dfs(4, small, big, 0)
    return res


def reverseChar(c):
    return chr(ord(c) & ord('_')) if c >= 'a' else chr(ord(c) | ord(' '))


def biggerChar(c):
    return chr(ord(c) + 1)


def smallerChar(c):
    return chr(ord(c) - 1)


def extendChar(c) -> str:
    if c == 'a' or c == 'A':
        return c + biggerChar(c) + reverseChar(c)
    elif c == 'h' or c == 'H':
        return c + smallerChar(c) + reverseChar(c)
    else:
        return c + biggerChar(c) + smallerChar(c) + reverseChar(c)


# 不考虑X
def notX(line):
    result = set()
    mapping = dict(Counter(line))
    opt_keys = mapping.keys()
    for key in opt_keys:
        # 暴力搜索
        ext_key = extendChar(key)
        for ext in ext_key:
            new_line = line + ext
            if isValid(new_line): result.add(ext)
    return result


if __name__ == '__main__':
    if os.path.exists('结果.txt'):
        os.remove('结果.txt')
    result_file = open('结果.txt', 'a')
    with open('./data.txt', 'r') as fp:
        start_time = time.perf_counter()
        lines = fp.readlines()
        for line in lines:
            oringin_line = line.strip()
            id, line = oringin_line.split('.')
            # 不考虑X
            if 'X' not in line:
                res = notX(line)
            # 考虑X的情况比较复杂
            else:
                xNum = line.count('X')
                mapping = dict(Counter(line.replace('X', '')))
                for key, value in list(mapping.items()):
                    if value == 3:
                        del mapping[key]
                keys = list(mapping.keys())
                values = list(mapping.values())
                joker = []

                # dfs获取X可变字符
                def dfs(cur, x):
                    if sum(cur) == xNum:
                        joker.append(cur.copy())

                    for i in range(len(keys)):
                        if cur[i] == 3 - values[i]: continue
                        if x:
                            cur[i] += 1
                            dfs(cur, x - 1)
                            cur[i] -= 1


                dfs([0] * len(keys), xNum)
                result = set()
                for t in joker:
                    cur = ''
                    for i in range(len(t)):
                        cur += t[i] * keys[i]
                    result.add(cur)
                cur_line = line.replace('X', '')
                # print(result)
                # 扩展result结果
                t = set()
                for r in result:
                    size = len(r)
                    if size == 1:
                        t |= set(extendChar(r))
                    elif size == 2:
                        t |= set([''.join(_) for _ in product(extendChar(r[0]), extendChar(r[1]))])
                    elif size == 3:
                        t |= set([''.join(_) for _ in product(extendChar(r[0]), extendChar(r[1]), extendChar(r[2]))])
                # print(t)
                magic_joker = [cur_line + _ for _ in t]
                res = set()
                # print(magic_joker)
                for magic in magic_joker:
                    res |= notX(magic)

            if res:
                res = sorted(list(res))
                res = ''.join(res)
                result_file.write(f'{id}.{res}\n')
        result_file.close()
        end_time = time.perf_counter()
        print("用时：", end_time - start_time)
