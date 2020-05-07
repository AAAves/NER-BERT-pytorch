# -*- coding:utf-8 -*-
"""
@author:Aves
@file:convert_data_to_msra.py
@time:2020/5/711:20
"""
import os
import csv

csv.field_size_limit(500 * 1024 * 1024)
def read_get_label_sentence(file_name_list):
    file_label = []
    temp_label = []
    sentences = []
    temp_sen = []
    label_set = {'O'}
    for file_name in file_name_list:
        file_reader = open(file_name, 'r',encoding='UTF-8')
        file_rows = []
        for line in file_reader.readlines():
            file_rows.append(line.rstrip().split("\t "))
        file_reader.close()
        for row in file_rows:
            if len(row) > 1:
                temp_sen.append(row[0].strip())
                temp_label.append(row[-4].strip())
                if row[-4].strip() not in label_set:
                    label_set.add(row[-4].strip())
            else:
                assert (len(temp_label) == len(temp_sen))
                if temp_sen:
                    sentences.append(temp_sen)
                    temp_sen = []
                if temp_label:
                    file_label.append(temp_label)
                    temp_label = []
        if sentences[-1] != temp_sen and len(temp_sen)>1:
            assert (len(temp_label) == len(temp_sen))
            sentences.append(temp_sen)
            file_label.append(temp_label)
        assert(len(file_label) == len(sentences))
    return file_label, sentences


def build_msra(sent_label, sentences, out_file):
    if os.path.isfile(out_file):
        os.remove(out_file)
    with open(out_file, 'w', encoding='utf-8') as f:
        for sentence, sent_label in zip(sentences, sent_label):
            for word, label in zip(sentence, sent_label):
                f.writelines(word + '\t' + label+ '\n')
            f.writelines('\n')


if __name__ == "__main__":
    train_path = "../Task_1/Data/train_and_dev/train"
    dev_path = "../Task_1/Data/train_and_dev/dev"
    test_path = "../Task_1/Data/test/subtask_2"

    # train_data
    files = os.listdir(train_path)
    file_name_list = [os.path.join(train_path, file) for file in files]
    sent_label, sentences = read_get_label_sentence(file_name_list)
    train_mrsa = os.path.join("./my_data", "train_mrsa_bio")
    build_msra(sent_label,sentences, train_mrsa)
    print("get mrsa in " + str(train_mrsa))

    # dev_data

    files = os.listdir(dev_path)
    file_name_list = [os.path.join(dev_path, file) for file in files]
    sent_label, sentences = read_get_label_sentence(file_name_list)
    dev_mrsa = os.path.join("./my_data", "dev_mrsa_bio")
    build_msra(sent_label,sentences, dev_mrsa)
    print("get mrsa in " + str(dev_mrsa))



