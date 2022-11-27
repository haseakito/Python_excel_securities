import requests
from datetime import date, timedelta

DATABASE = "database.db"

def main():
    # Get financial documents for the last year
    start_date = date(date.today().year - 1, 1, 1)
    end_date = date.today()

    day_list = get_day_list(start_date, end_date)

    docId_list = get_docId_list(day_list)

    for docId in docId_list:
        #　書類取得API
        edinet_url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/" + docId

        # pdf出力
        param = {type : 2}
        filename = "C://Users/81804/Documents/sample_financial_reports/" + docId + ".pdf"
        res = requests.get(edinet_url, param)

        if res.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)

def get_day_list(start_date, end_date):
    print("Start date: ", start_date)
    print("End date: ", end_date)

    # Get the period between the start date and end date
    period = end_date - start_date
    # Convert the period to int to get each day
    period = int(period.days)

    day_list = []
    for day in range(period + 1):
        day = start_date + timedelta(day)
        day_list.append(day)

    return day_list

def get_docId_list(day_list):
    docId_list = []

    # 　書類一覧API
    edinet_url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"

    for day in day_list:
        params = {"date" : day, "type" : 2}

        res = requests.get(edinet_url, params)
        res = res.json()

        for index in range(len(res["results"])):
            ordinance_code = res["results"][index]["ordinanceCode"]
            form_code = res["results"][index]["formCode"]

            print("ordinance code: ", ordinance_code, " form code: ", form_code)

            if ordinance_code == "010" and form_code == "030000":
                docId_list.append(res["results"][index]["docID"])

    return docId_list

if __name__ == "__main__":
    main()