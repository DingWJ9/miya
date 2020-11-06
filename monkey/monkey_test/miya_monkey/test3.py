#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
#汉诺塔
def move(index,start,mid,end):
    if index == 1:
        print("{}-->{}".format(start,end))
        return
    else:
        move(index-1,start,end,mid)
        print("{}-->{}".format(start, end))
        move(index-1,mid,start,end)
#找出任一重复
def checkone(num):
    sort_num = sorted(num)
    print(sort_num)
    num_len = len(sort_num)
    for i in range(1,num_len):
        if sort_num[i] == sort_num[i-1]:
            print("重复数为：{}".format(sort_num[i]))
            return True
#找出重复
def checkmore(nums):
    seen = []
    dup = []
    for i in nums:
        if i not in seen:
            seen.append(i)
        else:
            dup.append(i)

    print("重复的数字{}".format(dup))


if __name__ == '__main__':
    # move(3,"A","B","C")
    checkmore([66,88,99,88,66,77,7,7,2, 3, 1, 0, 2, 5, 3])