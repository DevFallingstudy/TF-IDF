import os
import errno
import codecs
import operator

# 일단 구조를 파악 -> labels
# 상수 등록
directory_labels = ['child/', 'culture/', 'economy/', 'education/',
                    'health/', 'life/', 'person/', 'policy/', 'society/']

INPUT_DATA_PATH = "Input_Data/"
TEST_DATA_PATH = "Test_Feature_Data/"
ORIGINAL_DATA_PATH = "Original_Data/"
ORIGINAL_INPUT_DATA_PATH = ORIGINAL_DATA_PATH+INPUT_DATA_PATH

word_rank = dict()
sorted_word_rank = list()


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
    for doc_name in directory_labels:
        childs = os.listdir(ORIGINAL_INPUT_DATA_PATH+doc_name)
        for file_name in childs:
            file_path = ORIGINAL_INPUT_DATA_PATH+doc_name+file_name
            if file_name.startswith('(POS)'):
                getWordRankFromDocument(file_path)

    sorted_word_rank = sorted(word_rank.items(), key=operator.itemgetter(1, 0))

    for item in sorted_word_rank:
        print(item)


def getWordRankFromDocument(file_name):
    f = codecs.open(file_name, 'r', 'utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        try:
            word = line.split(sep='\t')[1]
            word = word.replace('\n', '')
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
                        word_rank[each_word] += 1
                    except KeyError as e:
                        word_rank[each_word] = 1

        except IndexError as e:
            pass
    f.close()


# TF IDF 값을 구하는 함수
# 1. 각 단어의 빈도를 체크해서 랭킹을 세움
# 2. 현재 문서에서의 단어 출현율 계산(TF)
# 3. 해당
def calculateTFIDF():
    tf_val = getTF()
    normalizeTF(tf_val)
    idf_val = getIDF()


def getTF(doc_name):
    pass


def normalizeTF(tf_val):
    pass


def getIDF():
    return -1


if __name__ == '__main__':
    # initDataDirectories()
    # initDataFiles()

    getTotalWordRank()
    # getWordRankFromDocument(ORIGINAL_INPUT_DATA_PATH+"child/(POS)child_1.txt")
    # calculateTFIDF()
