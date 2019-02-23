from lxml import etree
import os

def parse_job_xml(job_xml_filepath):
    """
    parse the job.xml file in res directory, and return job list
    :param job_xml_filepath:
    :return:
    """
    tree = etree.parse(job_xml_filepath)
    return tree.xpath('//job/text()')

# 判断是否存在文件夹
def mkdir(path):

    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")
