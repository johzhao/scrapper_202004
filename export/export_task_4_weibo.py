import datetime

import xlsxwriter
import xlsxwriter.worksheet

from model.sina_topic_v2 import WeiboTopicDetailItem

KEYWORDS = [
    '新冠',
    '肺炎',
    '武汉',
    'COVID-19',
    '冠状病毒',
    '疫情',
]


def export_task_4_weibo(filepath: str):
    with xlsxwriter.Workbook(filepath) as wbk:
        sheet = wbk.add_worksheet('task_4_weibo')
        row = 0
        row = _export_header(sheet, row)
        items = WeiboTopicDetailItem.objects().order_by('title', 'keyword', '-date')
        for item in items:
            row = _export_item(sheet, row, item)


def _export_header(sheet: xlsxwriter.worksheet.Worksheet, row: int):
    col = 0
    sheet.write(row, col, '关键词')
    col += 1
    sheet.write(row, col, '话题')
    col += 1
    sheet.write(row, col, '时间')
    col += 1
    sheet.write(row, col, '阅读量')
    col += 1
    sheet.write(row, col, '讨论量')
    return row + 1


# noinspection DuplicatedCode
def _export_item(sheet: xlsxwriter.worksheet.Worksheet, row: int, item: WeiboTopicDetailItem) -> int:
    col = 0
    sheet.write(row, col, item.keyword)
    col += 1
    sheet.write(row, col, item.title)
    col += 1
    public_str = _get_date_str(item.date)
    sheet.write(row, col, public_str)
    col += 1
    sheet.write(row, col, item.read_count)
    col += 1
    sheet.write(row, col, item.discus_count)
    return row + 1


def _get_date_str(publish_datetime: datetime.datetime) -> str:
    return publish_datetime.strftime('%Y-%m-%d')
