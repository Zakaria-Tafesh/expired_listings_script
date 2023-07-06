from utils.zak_csv_utils import *


Target_CSV = """Adam's_Custom_Spreadsheet.csv"""

if __name__ == '__main__':
    csv_obj = UpdateCSV(Target_CSV)
    objs = csv_obj.read_and_convert()

    # print(type(objs))
    # for i, obj in enumerate(objs):
    #     address = obj.get('Address')
    #     address += f', {City}, {Area}'
    #     estimate = GetEstimateAPI(address)
    #     resp = estimate.get_estimate()
    #     print(resp)
    #     if resp.get('offer_price'):
    #         obj['offer_price'] = UpdateCSV.format_as_dollar(resp.get('offer_price'))
    #         obj['offer_price_90'] = UpdateCSV.format_as_dollar(resp.get('offer_price_90'))
    #
    #     print(obj)

    print(objs[0])
