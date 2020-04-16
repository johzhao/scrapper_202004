import datetime
from urllib.parse import urlparse, unquote

import xlsxwriter
import xlsxwriter.worksheet

from model.sina_topic import SinaTopic
from model.sina_weibo import SinaWeibo


def export_task_1_and_2(filepath: str):
    with xlsxwriter.Workbook(filepath) as wbk:
        sheet = wbk.add_worksheet('task_1')
        _export_topic_title(sheet)

        topics = {}
        objects = SinaTopic.objects().all()
        # Remove duplicate
        index = 1
        for topic in objects:
            if topic.url not in topics:
                _export_topic(sheet, index, topic)
                topics[topic.url] = ''
                index += 1

        sheet = wbk.add_worksheet('task_2')
        _export_weibo_title(sheet)

        start_datetime = datetime.datetime(2020, 1, 10)
        end_datetime = datetime.datetime(2020, 4, 11)
        objects = SinaWeibo.objects().all()
        index = 1
        for weibo in objects:
            if start_datetime <= weibo.publish <= end_datetime:
                _export_weibo(sheet, index, weibo)
                index += 1


def _export_topic_title(sheet: xlsxwriter.worksheet.Worksheet):
    sheet.write(0, 0, '关键字')
    sheet.write(0, 1, '话题')
    sheet.write(0, 2, '爬取时间')
    sheet.write(0, 3, '阅读量')
    sheet.write(0, 4, '讨论量')


def _export_topic(sheet: xlsxwriter.worksheet.Worksheet, row: int, topic: SinaTopic):
    col = 0
    col = _write_data(sheet, row, col, topic.keyword)
    col = _write_data(sheet, row, col, topic.topic)
    col = _write_data(sheet, row, col, topic.created)
    col = _write_data(sheet, row, col, topic.read_count)
    _write_data(sheet, row, col, topic.comment_count)


def _export_weibo_title(sheet: xlsxwriter.worksheet.Worksheet):
    sheet.write(0, 0, '所属话题')
    sheet.write(0, 1, '爬取时间')
    sheet.write(0, 2, '用户名')
    sheet.write(0, 3, '内容')
    sheet.write(0, 4, '发表时间')
    sheet.write(0, 5, '转发数')
    sheet.write(0, 6, '评论数')
    sheet.write(0, 7, '点赞数')


def _export_weibo(sheet: xlsxwriter.worksheet.Worksheet, row: int, weibo: SinaWeibo):
    url_components = urlparse(weibo.url)
    queries = url_components.query.split('&')

    topic = ''
    for query in queries:
        if not query.startswith('q='):
            continue
        fields = query.split('=')
        if len(fields) != 2:
            raise Exception(f'Failed to parse topic from url {weibo.url}')
        topic = unquote(fields[1])
        break

    if not topic:
        fields = url_components.path.split('/')
        topic = unquote(fields[-1])

    if not topic:
        raise Exception(f'Failed to parse topic from url {weibo.url}')

    col = 0
    col = _write_data(sheet, row, col, topic)
    col = _write_data(sheet, row, col, weibo.created)
    col = _write_data(sheet, row, col, weibo.username)
    col = _write_data(sheet, row, col, weibo.content)
    col = _write_data(sheet, row, col, weibo.publish)
    col = _write_data(sheet, row, col, weibo.forward_count)
    col = _write_data(sheet, row, col, weibo.comment_count)
    _write_data(sheet, row, col, weibo.favor_count)


def _write_data(sheet: xlsxwriter.worksheet.Worksheet, row: int, col: int, data) -> int:
    if isinstance(data, datetime.datetime):
        data_str = data.strftime('%Y-%m-%d %H:%M:%S')
        sheet.write(row, col, data_str)
    elif data is not None:
        sheet.write(row, col, data)
    return col + 1
