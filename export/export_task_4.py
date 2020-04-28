import datetime

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
        sheet = wbk.add_worksheet('task_4')
        row = 0
        _export_header(sheet, row)
        for key, value in MODELS.items():
            row = _export_worksheet_items(key, value, row, sheet)


def _export_worksheet_items(site_name: str, item_class, row: int, sheet: xlsxwriter.worksheet.Worksheet) -> int:
    begin = datetime.datetime(2020, 1, 10)
    for idx, keyword in enumerate(KEYWORDS, 1):
        items = item_class.objects(keyword=keyword).order_by('-date')
        for item in items:
            if item.publish < begin:
                continue
            row = _export_item(sheet, row, site_name, item)
    return row


def _export_header(sheet: xlsxwriter.worksheet.Worksheet, row: int):
    col = 0
    sheet.write(row, col, '关键词')
    col += 1
    sheet.write(row, col, '发表时间')
    col += 1
    sheet.write(row, col, '来源网站')
    col += 1
    sheet.write(row, col, '报道标题')


def _export_item(sheet: xlsxwriter.worksheet.Worksheet, row: int, site_name: str, item) -> int:
    col = 0
    sheet.write(row, col, item.keyword)
    col += 1
    public_str = _get_date_str(item.publish)
    sheet.write(row, col, public_str)
    col += 1
    sheet.write(row, col, site_name)
    col += 1
    sheet.write(row, col, item.title)
    return row + 1


def _write_row(sheet: xlsxwriter.worksheet.Worksheet, row: int, key: str, data: dict):
    sheet.write(row, 0, key)
    for idx, keyword in enumerate(KEYWORDS, 1):
        sheet.write(row, idx, data[keyword])


def _get_date_str(publish_datetime: datetime.datetime) -> str:
    return publish_datetime.strftime('%Y-%m-%d')
