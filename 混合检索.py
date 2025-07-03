#coding:utf-8

import dashscope
from http import HTTPStatus
import numpy as np
import jieba
from jieba.analyse import extract_tags
import math

# 初始化dashscope，替换qwen的api key
dashscope.api_key = 'sk-xxxx'

def embed_text(text):
    """
    使用dashscope API获取文本的嵌入向量
    :param text: 输入的文本
    :return: 文本的嵌入向量，如果失败则返回None
    """
    resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v2,
        input=text)
    if resp.status_code == HTTPStatus.OK:
        return resp.output['embeddings'][0]['embedding']
    else:
        print(f"Failed to get embedding: {resp.status_code}")
        return None

def cosine_similarity(vec1, vec2):
    """
    计算两个向量之间的余弦相似度
    :param vec1: 第一个向量
    :param vec2: 第二个向量
    :return: 余弦相似度
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def calculate_similarity(text1, text2):
    """
    计算两个文本之间的相似度
    :param text1: 第一个文本
    :param text2: 第二个文本，可以包含多个句子，用逗号分隔
    :return: 每个句子的相似度列表，格式为 (句子, 相似度)
    """
    embedding1 = embed_text(text1)
    if embedding1 is None:
        return []

    similarities = []
    sentences = [sentence.strip() for sentence in text2.split(',') if sentence.strip()]

    for sentence in sentences:
        embedding2 = embed_text(sentence)
        if embedding2 is None:
            continue
        similarity = cosine_similarity(embedding1, embedding2)
        similarities.append((sentence, similarity))

    return similarities

def extract_keywords(text):
    """
    提取文本中的关键词
    :param text: 输入的文本
    :return: 关键词列表
    """
    return extract_tags(text)

def cosine_similarity_tfidf(vec1, vec2):
    """
    计算两个TF-IDF向量之间的余弦相似度
    :param vec1: 第一个TF-IDF向量
    :param vec2: 第二个TF-IDF向量
    :return: 余弦相似度
    """
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)
    sum1 = sum(vec1[x] ** 2 for x in vec1)
    sum2 = sum(vec2[x] ** 2 for x in vec2)
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return numerator / denominator if denominator else 0.0

def calculate_tfidf_similarity(text, text2):
    """
    计算两个文本之间的TF-IDF相似度
    :param text: 第一个文本
    :param text2: 第二个文本，可以包含多个文档，用竖线分隔
    :return: 每个文档的TF-IDF相似度列表
    """
    documents = [doc for doc in text2.split('|') if doc.strip()]
    query_keywords = extract_keywords(text)
    documents_keywords = [extract_keywords(doc) for doc in documents]

    query_keyword_counts = {kw: query_keywords.count(kw) for kw in set(query_keywords)}
    total_documents = len(documents)
    all_keywords = set(kw for doc in documents_keywords for kw in doc)
    keyword_idf = {kw: math.log((1 + total_documents) / (1 + sum(1 for doc in documents_keywords if kw in doc))) + 1 for kw in all_keywords}

    query_tfidf = {kw: count * keyword_idf.get(kw, 0) for kw, count in query_keyword_counts.items()}
    documents_tfidf = [{kw: doc.count(kw) * keyword_idf.get(kw, 0) for kw in set(doc)} for doc in documents_keywords]

    return [cosine_similarity_tfidf(query_tfidf, doc_tfidf) for doc_tfidf in documents_tfidf]

def calculate_final_score(embedding_similarity, tfidf_similarity, w1=0.5, w2=0.5):
    """
    计算最终得分，结合语义相似度和TF-IDF相似度
    :param embedding_similarity: 语义相似度
    :param tfidf_similarity: TF-IDF相似度
    :param w1: 语义相似度的权重
    :param w2: TF-IDF相似度的权重
    :return: 最终得分
    """
    return w1 * embedding_similarity + w2 * tfidf_similarity

def main():
    """
    主函数，用于测试和演示
    """
    text1 = '把商品发到闲鱼'
    text2 = '我想将商品挂到闲鱼'
    text3 = '我想找闲鱼问下商品'

    tfidf_similarities2 = calculate_tfidf_similarity(text1, text2)
    tfidf_similarities3 = calculate_tfidf_similarity(text1, text3)

    embedding_similarities2 = calculate_similarity(text1, text2)
    embedding_similarities3 = calculate_similarity(text1, text3)

    Semantic_Proportio = 0.8
    Word_Proportion = 0.2

    final_score2 = calculate_final_score(embedding_similarities2[0][1], tfidf_similarities2[0], Semantic_Proportio, Word_Proportion)
    final_score3 = calculate_final_score(embedding_similarities3[0][1], tfidf_similarities3[0], Semantic_Proportio, Word_Proportion)

    print(f"最终语句1得分: {final_score2} \n\n最终语句2得分: {final_score3}")

if __name__ == '__main__':
    main()

