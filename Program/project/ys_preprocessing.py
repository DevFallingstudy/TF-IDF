import os
import errno
import codecs
import operator
import math

# 일단 구조를 파악 -> labels
# 상수 등록
directory_labels = ['child/', 'culture/', 'economy/', 'education/',
                    'health/', 'life/', 'person/', 'policy/', 'society/']

INPUT_DATA_PATH = "Input_Data/"
TEST_DATA_PATH = "Test_Feature_Data/"
ORIGINAL_DATA_PATH = "Original_Data/"
ORIGINAL_INPUT_DATA_PATH = ORIGINAL_DATA_PATH+INPUT_DATA_PATH

word_rank = dict()

# 미리 Input_Data에 폴더를 만들어두고 시작
def initDataDirectories():
    try:
        for str_name in directory_labels:
            dir_path = INPUT_DATA_PATH+str_name
            if not(os.path.isdir(dir_path)):
                os.makedirs(os.path.join(dir_path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory")
            raise


# Input_Data안에 있는 폴더에 파일을 만들고 시작
def initDataFiles():
    for parent_path in directory_labels:
        for child_path in searchChilds(ORIGINAL_INPUT_DATA_PATH+parent_path):
            file_path = INPUT_DATA_PATH + parent_path + child_path
            if not(os.path.isfile(file_path)):
                f = open(file_path, 'w')
                f.close()


# root_path 아래의 차일드의 목록을 반환
def searchChilds(root_path):
    childs = os.listdir(root_path)
    return childs


def getTotalWordRank():
    total_words = dict()
    for doc_name in directory_labels:
        childs = os.listdir(ORIGINAL_INPUT_DATA_PATH+doc_name)
        for file_name in childs:
            file_path = ORIGINAL_INPUT_DATA_PATH+doc_name+file_name
            if file_name.startswith('(POS)'):
                words = getWordRankFromDocument(file_path)
                for key in words.keys():
                    try:
                        total_words[key] += words[key]
                    except KeyError as e:
                        total_words[key] = words[key]


    sorted_word_rank = sorted(total_words.items(), key=operator.itemgetter(1, 0), reverse=True)

    return sorted_word_rank


def getWordRankFromDocument(file_name):
    words = dict()
    f = codecs.open(file_name, 'r', 'utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        try:
            word = line.split(sep='\t')[1]
            word = word.replace('\n', '')
            word = word.replace('\r', '')
            word = word.replace('’', '')
            word = word.replace('‘', '')
            word = word.replace('“', '')
            word = word.replace('”', '')
            word = word.replace(',', '')
            word = word.replace('(', '')
            word = word.replace(')', '')

            for each_word in word.split('+'):
                if 'NNG' in each_word or 'NNP' in each_word:
                    try:
                        words[each_word] += 1
                    except KeyError as e:
                        words[each_word] = 1

        except IndexError as e:
            pass
    f.close()

    return words


# TF IDF 값을 구하는 함수
# 1. 각 단어의 빈도를 체크해서 랭킹을 세움
# 2. 현재 문서에서의 단어 출현율 계산(TF)
# 3. 해당
def calculateTFIDF(doc_name, top5000_keys):
    tf_table = getTF(doc_name, top5000_keys)
    norm_tf_table = normalizeTF(tf_table)
    # for key in norm_tf_table.keys():
    #     print('(' + key + ') :', norm_tf_table[key])
    idf_table = getIDF(doc_name, top5000_keys)

    return norm_tf_table


def getTF(doc_name, top5000_keys):
    tf_table = dict()
    child_name = doc_name[5:doc_name.index('_')]+"/"
    doc_path = ORIGINAL_INPUT_DATA_PATH + child_name + doc_name

    # print('TF for ' + doc_path)

    for key in top5000_keys:
        tf_table[key] = 1
    words = getWordRankFromDocument(doc_path)
    for key in top5000_keys:
        try:
            if 1 < words[key]:
                tf_table[key] = words[key]
        except KeyError as e:
            tf_table[key] = 0

    # for key in tf_table.keys():
    #     print('('+key+') :', tf_table[key])
    return tf_table


def normalizeTF(tf_table):
    for key in tf_table:
        val = float(tf_table[key]) + 1
        new_val = math.log10(val)
        tf_table[key] = new_val
    return tf_table


def getIDF(word_current):
    origin_file_paths = getOriginFilePath()

    doc_cnt = 0
    rank_val = 0

    for path_tmp in origin_file_paths:
        words_rank = getWordRankFromDocument(path_tmp)
        doc_cnt += 1
        try:
            if words_rank[word_current] > 0:
                rank_val += 1
        except KeyError as e:
            pass
    idf_val = math.log10(doc_cnt/rank_val)
    print('total doc :',doc_cnt, 'available doc :', rank_val)
    # print()
    return idf_val


def getOriginFilePath():
    path_list = list()
    for doc_name in directory_labels:
        childs = os.listdir(ORIGINAL_INPUT_DATA_PATH+doc_name)
        for file_name in childs:
            file_path = ORIGINAL_INPUT_DATA_PATH+doc_name+file_name
            if file_name.startswith('(POS)'):
                path_list.append(file_path)

    return path_list


def getFileNames():
    name_list = list()
    for doc_name in directory_labels:
        childs = os.listdir(ORIGINAL_INPUT_DATA_PATH+doc_name)
        for file_name in childs:
            file_path = ORIGINAL_INPUT_DATA_PATH+doc_name+file_name
            if file_name.startswith('(POS)'):
                name_list.append(file_path.split('/')[3])

    return name_list

if __name__ == '__main__':
    # initDataDirectories()
    # initDataFiles()

    file_paths = None
    doc_dict = dict()
    top5000_keys = list()

    # Get top 5000 word
    sorted_word_rank = getTotalWordRank()
    top5000_rank = sorted_word_rank[0:5]
    for item in top5000_rank:
        top5000_keys.append(item[0])

    file_paths = getFileNames()

    # Get TF
    print('Getting TF.')
    total_tf_table = dict()
    tf_table = dict()
    norm_tf_table = dict()
    for path in file_paths:
        tf_table = getTF(path, top5000_keys)
        norm_tf_table = normalizeTF(tf_table)

        total_tf_table[path] = norm_tf_table

    for key in total_tf_table.keys():
        print(key, total_tf_table[key])
    print('Got TF!')


    # Get IDF
    total_idf_table = dict()
    for word_current in top5000_keys:
        total_idf_table[word_current] = getIDF(word_current)
        print('('+word_current+') idf :', total_idf_table[word_current])


    for path in file_paths:
        tf_table = getTF(path, top5000_keys)
        norm_tf_table = normalizeTF(tf_table)

        total_tf_table[path] = norm_tf_table

    total_tfidf_table = dict()

    for doc_name in total_tf_table.keys():
        print(doc_name)
        total_tfidf_table[doc_name] = dict()
        for word in top5000_keys:
            doc_tf_table = total_tf_table[doc_name]
            tf_val = doc_tf_table[word]
            idf_val = total_idf_table[word]
            print(word)
            print('tf :', tf_val, 'idf :', idf_val)
            tfidf_val = tf_val * idf_val
            print('tf-idf :', tfidf_val)

            total_tfidf_table[doc_name][word] = tfidf_val
            print(total_tfidf_table[doc_name][word])
        print()

    for key1 in total_tfidf_table.keys():
        for key2 in total_tfidf_table[key1].keys():
            print(key1, key2, total_tfidf_table[key1][key2])

    # Write to files

    # for doc_name in total_tf_table.keys():
    #     print(doc_name)
    #     for word in top5000_keys:
    #         print(word)
    #         print(total_tfidf_table[doc_name][word])

    # getWordRankFromDocument(ORIGINAL_INPUT_DATA_PATH+"child/(POS)child_1.txt")
    # calculateTFIDF()
