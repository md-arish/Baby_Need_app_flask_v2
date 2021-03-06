# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:36:45 2020

@author: mdari
"""


from flask import Flask,render_template,request
import sqlite3
import json

class item:
    def __init__(self):
        pass
    
    def __init__(self,name=None,qty=None,brand=None,colour=None,price=None):
        self.name=name
        self.qty=qty
        self.brand=brand
        self.colour=colour
        self.status="Not Bought"
        self.price=price
        
    
    def get_name(self):
        return self.name
    
    def set_name(self,name):
        self.name=name
        
    def get_qty(self):
        return self.qty
    
    def set_qty(self,qty):
        self.qty=qty
        
    def get_colour(self):
        return self.colour
    
    def set_colour(self,colour):
        self.colour=colour
        
    def get_brand(self):
        return self.brand
    
    def set_brand(self,brand):
        self.brand=brand
        
    def get_price(self):
        return self.price
    
    def set_price(self,price):
        self.price=price
        
    def get_status(self):
        return self.status
    
    def set_status(self,status):
        self.status=status
   


class database:
    def __init__(self):
        pass
    
    def get_item(self,item):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select * from items where Name=(:name)",{'name':item.get_name()})
        row=curs.fetchone()
        item.set_name(row[0])
        item.set_qty(row[1])
        item.set_brand(row[2])
        item.set_colour(row[3])
        item.set_price(row[4])
        item.set_status(row[5])
        connection.close()
        return item
    
    def get_name_all(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select name from items")
        names=curs.fetchall()
        return names
    
    def isempty(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select * from items")
        items=curs.fetchall()
        if len(items)==0:
            return True
        else:
            return False
        
    def create_table(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("CREATE TABLE items(name text,quantity integer,brand text,colour text,price integer,status text)")
        connection.commit()
        connection.close()
        
    def insert(self,item):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("INSERT INTO items values(:name, :quantity, :brand, :colour, :price, :status)",{'name':item.get_name(),'quantity':item.get_qty(),'brand':item.get_brand(),'colour':item.get_colour(),'price':item.get_price(),'status':item.get_status()})
        connection.commit()
        connection.close()

    def delete(self,item):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("DELETE FROM items where name=(:name)",{'name':item.get_name()})
        connection.commit()
        connection.close()
        
    def delete_all(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("drop table items")
        curs.execute("CREATE TABLE items(name text,quantity integer,brand text,colour text,price integer,status text)")
        connection.commit()
        connection.close()
        
    def update(self,item):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("update items set quantity=(:quantity),colour=(:colour),brand=(:brand),price=(:price),status=(:status) where name=(:name)",{'quantity':item.get_qty(),'colour':item.get_colour(),'brand':item.get_brand(),'price':item.get_price(),'status':item.get_status(),'name':item.get_name()})
        connection.commit()
        connection.close()
        
    def display_bought(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select * from items where status=(:sts)",{'sts':'Bought'})
        disp_list=curs.fetchall()
        connection.close() 
        return disp_list
            
    def display_unbought(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select * from items where status=(:sts)",{'sts':'Not Bought'})
        disp_list=curs.fetchall()
        connection.close()
        return disp_list
    
    def display_all(self):
        connection=sqlite3.connect('baby_needs.db')
        curs=connection.cursor()
        curs.execute("select * from items")
        disp_list=curs.fetchall()
        connection.close()
        return disp_list
    
    
app = Flask(__name__)
    
@app.route('/')
def index():
    d_database=database()
    d_database=database()
    names=d_database.get_name_all()
    formatted_names=[]
    for name in names:
        formatted_names.append(name[0])
    return render_template("test.html",names=formatted_names)
    

@app.route('/select_data', methods=['GET'])
def select_data():
    name=request.args.get('data')
    s_item=item()
    s_item.set_name(name)
    d_database=database()
    s_item=d_database.get_item(s_item)
    resp = {"name":s_item.get_name(),"colour":s_item.get_colour(),"quantity":s_item.get_qty(),"brand":s_item.get_brand(),"price":s_item.get_price(),"status":s_item.get_status()}
    return json.dumps(resp)
        

@app.route('/insert', methods=['POST'])
def insert():
     json_data=json.dumps(request.form)
     data=json.loads(json_data)
     i_item=item(data['name'],data['quantity'],data['brand'],data['colour'],data['price'])
     d_database=database()
     d_database.insert(i_item)
     resp={"status":"success"}
     return json.dumps(resp)
    

@app.route('/display_bought')
def disp_bought():
    d_database=database()
    item_list=d_database.display_bought()
    if not item_list:
        resp={"status":"failure"}
        return json.dumps(resp)
    else:
        items=[]
        resp={}
        for i in item_list:
            items.append(i[0])
        resp["names"]=items
        print(resp)
        return json.dumps(resp)

@app.route('/display_unbought')
def disp_unbought():
    d_database=database()
    item_list=d_database.display_unbought()
    if not item_list:
        resp={"status":"failure"}
        return json.dumps(resp)
    else:
        items=[]
        resp={}
        for i in item_list:
            items.append(i[0])
        resp["names"]=items
        return json.dumps(resp)
        
    
@app.route('/update', methods=['POST'])
def update():
    json_data=json.dumps(request.form)
    data=json.loads(json_data)
    up_item=item(data['name'],data['quantity'],data['brand'],data['colour'],data['price'])
    up_item.status=data['status']
    d_database=database()
    d_database.update(up_item)
    resp={"status":"success"}
    return json.dumps(resp)
    

@app.route('/delete',methods=['GET'])
def delete():
    name=request.args.get('data')
    d_item=item()
    d_item.set_name(name)
    d_database=database()
    d_database.delete(d_item)
    resp={"status":"success"}
    return json.dumps(resp)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
        