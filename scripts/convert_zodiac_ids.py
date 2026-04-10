#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换历史数据的生肖ID
从旧顺序转换到新顺序
"""

# 旧顺序: 鼠、牛、虎、兔、龙、蛇、马、羊、猴、鸡、狗、猪
OLD_ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
OLD_ID_TO_NAME = {i+1: name for i, name in enumerate(OLD_ZODIAC)}

# 新顺序: 马、蛇、龙、兔、虎、牛、鼠、猪、狗、鸡、猴、羊
NEW_ZODIAC = ["马", "蛇", "龙", "兔", "虎", "牛", "鼠", "猪", "狗", "鸡", "猴", "羊"]
NEW_NAME_TO_ID = {name: i+1 for i, name in enumerate(NEW_ZODIAC)}

def convert_id(old_id):
    """
    将旧ID转换为新ID
    """
    name = OLD_ID_TO_NAME[old_id]
    new_id = NEW_NAME_TO_ID[name]
    return new_id

def convert_csv(input_file, output_file):
    """
    转换CSV文件中的生肖ID
    """
    import csv
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        
        # 写标题
        header = next(reader)
        writer.writerow(header)
        
        # 转换数据
        for row in reader:
            period = row[0]
            old_zodiac = int(row[1])
            new_zodiac = convert_id(old_zodiac)
            writer.writerow([period, new_zodiac])
    
    print(f"转换完成: {input_file} -> {output_file}")
    print(f"旧ID -> 新ID映射:")
    for old_id in range(1, 13):
        name = OLD_ID_TO_NAME[old_id]
        new_id = NEW_NAME_TO_ID[name]
        print(f"  {old_id} ({name}) -> {new_id}")

if __name__ == '__main__':
    convert_csv('real_lottery_history.csv', 'real_lottery_history_converted.csv')
