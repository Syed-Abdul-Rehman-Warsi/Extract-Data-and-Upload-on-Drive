import pandas as pd
import csv
import datetime
from datetime import date as dt
import calendar

class record:

    def extract_record(self):
        url = 'https://www.saudiexchange.sa/Resources/Reports/DetailedDaily_en.html'
        dfs = pd.read_html(url, encoding="utf-8")
        self.df = dfs[-1]
        f = dfs[0]
        f = f.iloc[4]
        date = f[0]
        self.date  = date.replace("Market Date ", "")        
        return self.df, self.date

    def date_time(self):
        date = self.extract_record()
        today = self.date
        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        day = datetime.datetime.strptime(today, '%Y/%m/%d').weekday()
        self.day = day_name[day]
        today = today.replace('/', '_')
        self.name = 'Companies_List_' + today + '.csv'
        return self.name, self.day

    def html_to_csv(self):
        data_frame = self.extract_record()
        df = self.df
        path = 'D:\Mama Jani\Daily Report'
        n_name = self.date_time()
        name = self.name
        self.completeName = (path + '\\' + name)
        df.to_csv(self.completeName, index=None, header=False)


    def companies_list(self):
        data = self.html_to_csv()
        d = self.date_time()
        file = self.completeName
        df1 = pd.read_csv(file)
        col = list(df1.columns)
        today_date = self.date
        today_day = self.day
        col.pop(0)
        col.insert(0, "Date")
        col.insert(1, "Day")
        path = 'D:\Mama Jani\Companies List\\'

        for i in range(len(df1)):
            da = df1.iloc[i]
            da = list(da)
            name = da[0]
            new_string = ''.join(char for char in name if char.isalnum())
            name = new_string + '.csv'
            name = path + name
            da.pop(0)
            da.insert(0, today_date)
            da.insert(1, today_day)
            f = open(name, 'a', newline='')

            # create the csv writer
            writer = csv.writer(f)

            # write a row to the csv file
            writer.writerow(da)

            # close the file
            f.close()

        print(today_day)
        print(today_date)
        print("Files updated successfully ")

    def upload_drive(self):
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        file = self.html_to_csv()
        filename = self.completeName
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1PNWZv-ptY1_iFWC-vbLI-E83B2oUw7o5'}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload()  # Upload the file.
            print("files upload successfully on drive")

    def test(self):
        a = self.date_time()
        b = self.extract_record()
        print(self.df.head())
        print(self.name)


a = record()
a.html_to_csv()
a.companies_list()
a.upload_drive()



