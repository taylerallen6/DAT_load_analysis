import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from pprint import pprint
from datetime import datetime
import json
import parse_load_data2 as pld


def main():
  cred = credentials.Certificate("firebaseServiceAccountKey.json")
  firebase_admin.initialize_app(cred)

  db = firestore.client()

  start_date = datetime.strptime("2021-06-28 4", "%Y-%m-%d %H")
  end_date = datetime.strptime("2021-06-28 6", "%Y-%m-%d %H")

  docs = db.collection(u'loads')
  # docs = docs.where('timestamp', '>=', start_date).where('timestamp', '<', end_date)
  docs = docs.stream()

  loads = []
  df = pd.DataFrame()
  for i, doc in enumerate(docs):
    data = doc.to_dict()['load_data']
    format = "%Y-%m-%d %H:%M:%S"
    data['collected_timestamp'] = doc.to_dict()['timestamp'].strftime(format)
    loads.append(data)

    if i % 1000 == 1000-1:
      print('batch: ', i)
      
      temp_df = pld.get_loads_df(loads)
      # print(temp_df)
      
      if not temp_df.empty:
        df = df.append(temp_df, ignore_index=True, sort=False)
        print('number of loads: ', len(df))

      loads = []

    break_val = 61000
    if i % break_val == break_val-1:
      break

  filename = 'loads2.csv'
  df.to_csv(filename, index=False)


if __name__ == "__main__":
  main()