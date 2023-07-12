from utils.zak_csv_utils import *


Target_CSV = """Adam's_Expired_Listing_Report (3).csv"""
ADD_TO_OUTPUT = """Complete"""
ADD_DATETIME_TO_OUTPUT = True

if __name__ == '__main__':
    csv_obj = UpdateCSV(Target_CSV, ADD_TO_OUTPUT, ADD_DATETIME_TO_OUTPUT)

    csv_obj.read_and_convert()
    csv_obj.update_objects()
    csv_obj.write_objects()

