# from flask import Flask, request, render_template, jsonify
# import json
# from datetime import datetime
# from flask_cors import CORS, cross_origin
# import mysql.connector
# import sys

# app = Flask(__name__)
# CORS(app, supports_credentials=True)


# @app.route('/query_result', methods=['POST'])
# def query_result():
#     # print("a")
#     post_data = request.get_json()
#     Reporter = post_data.get('Reporter')
#     Mail = post_data.get('Mail')
#     Person = post_data.get('Person')
#     Date = post_data.get('Date')
#     Type = post_data.get('Type')
#     Content = post_data.get('Content')
#     Evidence = post_data.get('Evidence')

#     # print(Date)

#     date_object = datetime.strptime(Date, '%b %d %Y %H:%M:%S')


#     cnx = mysql.connector.connect(user='root', password='123456', host='35.229.151.61', database='reports')
#     cursor = cnx.cursor()
#     sql = "INSERT INTO report (reporter, reporter_email, person, type, content, evidence, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#     val = (Reporter, Mail, Person, Type, Content, Evidence, date_object.strftime('%Y-%m-%d %H:%M:%S'))
#     try:
#         cursor.execute(sql, val)
#         cnx.commit()

#         message = {'status': 'Success'}
#         return jsonify(message)

#     except (mysql.connector.Error, mysql.connector.Warning) as e:
#         print(e)
#         return None


#     # message = {'status': 'Success'}
#     # print(Reporter, Mail, Person, Date, Type, Content)

    
# @app.route('/query_search', methods=['POST'])
# def query_search():
#     post_data = request.get_json()
#     Mail = post_data.get('Mail')
#     Person = post_data.get('Person')
#     StartDate = post_data.get('StartDate')
#     EndDate = post_data.get('EndDate')
#     Type = post_data.get('Type')
    
#     Type_Query = ""
#     Date_Query = ""
#     Person_Query = ""
#     Mail_Query = ""

#     # print("A" + Type + "A")

#     if Type == "none":
#         Type_Query = " type IS NOT NULL"
#     else:
#         Type_Query = " type = \'" + Type + "\'"

#     if StartDate != "":
#         StartDate = StartDate[:12] + "00:00:00"
#         EndDate = EndDate[:12] + "23:59:59"
#         START = datetime.strptime(StartDate, '%b %d %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
#         END = datetime.strptime(EndDate, '%b %d %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

#         Date_Query = " AND date BETWEEN \'" + START + "\' AND \'" + END + "\'" 

#     if Person != "":
#         Person_Query = " AND person = \'" + Person + "\'"

#     if Mail != "":
#         Mail_Query = " AND reporter_email = \'" + Mail + "\'" 


#     cnx = mysql.connector.connect(user='root', password='123456', host='35.229.151.61', database='reports')
#     cursor = cnx.cursor(buffered=True)
#     sql = "SELECT * FROM `report` WHERE" + Type_Query + Date_Query + Person_Query + Mail_Query

#     # print(sql)
#     try:
#         cursor.execute(sql)
#         cnx.commit()
#         result = cursor.fetchall()

#         row_list = []
#         for row in result:
#             ele_row = {
#                 "Reporter" : row[0],
#                 "Email" : row[1],
#                 "Person": row[2],
#                 "Type": row[3],
#                 "Content": row[4],
#                 "Evidence": row[5],
#                 "Date": row[6]
#             }
#             row_list.append(ele_row)



#         message = {'status': 'Success'}
#         return json.dumps(row_list, default= str)

#     except (mysql.connector.Error, mysql.connector.Warning) as e:
#         print(e)
#         return None


#     message = {'status': 'Success'}
#     return jsonify(message)



# # @app.route('/')
# # def hello_world():
# #     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)