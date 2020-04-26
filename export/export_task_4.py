import datetime
from collections import defaultdict
from functools import partial

import xlsxwriter
import xlsxwriter.worksheet

from model import task_4_items


MODELS = {
    '央广网': task_4_items.CnrItem,
    '新华网': task_4_items.XinHuaNewsItem,
    # '人民网': task_4_items.PeopleItem,
    # '中国新闻网': task_4_items.ChinaNewsItem,
    '新浪新闻': task_4_items.SinaNewsItem,
    '中国政府网': task_4_items.GovItem,
    '中国疾病预防控制中心': task_4_items.ChinaCdcItem,
    # '中国网': task_4_items.ChinaItem,
    '央视网': task_4_items.CctvItem,
}

KEYWORDS = [
    '新冠',
    '肺炎',
    '武汉',
    'COVID-19',
    '冠状病毒',
    '疫情',
]


def export_task_4(filepath: str):
    with xlsxwriter.Workbook(filepath) as wbk:
        for key, value in MODELS.items():
            sheet = wbk.add_worksheet(key)
            _export_worksheet_items(value, sheet)


def _export_worksheet_items(item_class, sheet: xlsxwriter.worksheet.Worksheet):
    a = partial(defaultdict, int)
    data = defaultdict(a)

    begin = datetime.datetime(2020, 1, 10)
    for idx, keyword in enumerate(KEYWORDS, 1):
        items = item_class.objects(keyword=keyword).order_by('-date')
        for item in items:
            if item.publish < begin:
                continue

            public_str = _get_date_str(item.publish)
            data[public_str][keyword] += 1
        sheet.write(0, idx, keyword)

    order_keys = sorted(data.keys(), reverse=True)

    date_iterator = datetime.datetime.strptime(order_keys[0], '%Y-%m-%d')
    date_delta = datetime.timedelta(days=1)
    row = 1
    while date_iterator >= begin:
        date_str = _get_date_str(date_iterator)
        _write_row(sheet, row, date_str, data[date_str])
        row += 1
        date_iterator -= date_delta


def _write_row(sheet: xlsxwriter.worksheet.Worksheet, row: int, key: str, data: dict):
    sheet.write(row, 0, key)
    for idx, keyword in enumerate(KEYWORDS, 1):
        sheet.write(row, idx, data[keyword])


def _get_date_str(publish_datetime: datetime.datetime) -> str:
    return publish_datetime.strftime('%Y-%m-%d')
