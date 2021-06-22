
from bson.json_util  import ObjectId, dumps
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response 
import json
import uuid
import time
from array import *
import collections
from collections import defaultdict
# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSMarkets']

# Choose collections
products = db['Products']
users = db['Users']

#Encoder too export objectid for the elements inside mongodb
class MyEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)
        
# Initiate Flask App
app = Flask(__name__)
app.json_encoder = MyEncoder
app.config['JSON_SORT_KEYS'] =True

# Session for simple users
users_sessions = {}

# Create sessions for simple users
def create_session(user_name):
    user_uuid = str(uuid.uuid1()) #37 characters wide string 
    users_sessions[user_uuid] = (user_name, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

#Session for Administrators
admins_sessions = {}

# Create sessions for Admins
def create_admin_session(admin_name):
    admin_uuid = str(int(uuid.uuid1())) #39 digit number displayed as string
    admins_sessions[admin_uuid] = (admin_name, time.time())
    return admin_uuid
def admin_session_valid(admin_uuid):
    return admin_uuid in admins_sessions


# Δημιουργία Διαχειριστή 
@app.route('/createAdmin', methods=['POST'])
def create_admin():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data or not "name" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    if users.find({"email":data["email"]}).count() == 0 :# Έλεγχος αν  υπάρχει admin με το email το οποίο δόθηκε.
        admin = {"email": data['email'], "name": data['name'], "password":data['password'], "category":"Admin"}
        # Add Admin to the "Users" collection
        users.insert_one(admin)
        return Response(data['name']+" with the email address :"+data['email']+" has been added to the MongoDB", status=200,mimetype='application/json')
            # Διαφορετικά, αν υπάρχει ήδη κάποιος διαχειριστής  με αυτό το name.
    else:
        return Response("An Admin with the given credentials already exists", status=400 ,mimetype='application/json')

# Σύνδεση Ως Διαχειριστής 
@app.route('/AdminLogin', methods=['POST'])
def admin_login(): 
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data :
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    if users.find({'$and':[{"email":data["email"]},{"password":data["password"]},{"category": "Admin"} ]}).count() !=0  :
        admin_uuid = create_admin_session(data['email'])# Ο εκάστοτε χρήστης χρησιμοποιεί ένα μοναδικό uuid το οποίο παρέχει το σύστημα ώστε να παραμείνει σε σύνδεση ο χρήστης.
        res = {"uuid": admin_uuid, "email": data['email']}
        return Response(json.dumps(res),status=200,mimetype='application/json')
    else:
        return Response("Wrong email or password.",status=400,mimetype='application/json')

# Δημιουργία απλού χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data or not "name" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    if users.find({"email":data["email"]}).count() == 0 :# Έλεγχος αν  υπάρχει user με το email το οποίο δόθηκε.
        user = {"email": data['email'], "name": data['name'], "password":data['password'], "category":"Simple User"}
        # Add user to the "Users" collection
        users.insert_one(user)
        return Response(data['name']+" with the email address :"+data['email']+" has been added to the MongoDB", status=200,mimetype='application/json')
            # Διαφορετικά, αν υπάρχει ήδη κάποιος χρήστης με αυτό το username.
    else:
        return Response("A user with the given credentials already exists", status=400 ,mimetype='application/json')

# Σύνδεση ως απλός χρήστης
@app.route('/login', methods=['POST'])
def login(): 
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data :
        return Response("Information incomplete",status=500,mimetype="application/json")
    if users.find({'$and':[{"email":data["email"]},{"password":data["password"]}, {"category": "Simple User"} ]}).count() !=0  :
        user_uuid = create_session(data['email'])# Ο εκάστοτε χρήστης χρησιμοποιεί ένα μοναδικό uuid το οποίο παρέχει το σύστημα ώστε να παραμείνει σε σύνδεση ο χρήστης.
        res = {"uuid": user_uuid, "email": data['email']}
        global user_email
        user_email = data['email']
        return Response(json.dumps(res),status=200,mimetype='application/json')
    else:
        return Response("Wrong email or password.",status=400,mimetype='application/json')



# Εύρεση Προϊόντος
@app.route('/getProduct', methods=['GET'])
def get_product():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    uuid = request.headers.get('Authorization')
    if is_session_valid(uuid)    == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid)   == True:
        print("You can search a product with one the following three options: \n 1:Search via the name of the product \n 2:Search via the product's catergory \n 3:Search via the products ID")
        # User choice(user input)
	# Check if user applies more that one fields during search (only one available at a time!)
        if "name" in data and "_id" in data and "category" in data :
            return Response("Plase search with one of the three options every time at once: name or _id or category",status=400,mimetype="application/json")
        if "name" in data and "_id" in data :
            return Response("Plase search with one of the three options every time at once: name or _id or category",status=400,mimetype="application/json")
        if "_id" in data and "category" in data :
            return Response("Plase search with one of the three options every time at once: name or _id or category",status=400,mimetype="application/json")
        if "name" in data and "category" in data :
            return Response("Plase search with one of the three options every time at once: name or _id or category",status=400,mimetype="application/json")
	# Search by name
        if "name" in data:
            product = products.find({"name":data["name"]})
            if product != None :
                Products = []
                for i in product:
                    Products.append(i)
                return jsonify(Products)
            if product == None :
                return Response("No product found with that name",status=400,mimetype='application/json')
        #Search by category
        if "category" in data: 
            product = products.find({"category":data["category"]})
            if product != None :
                Products = []
                for i in product:
                    Products.append(i)
                return jsonify(Products)
            if product == None :
                return Response("No product found by this category",status=400,mimetype='application/json')
        # Search by ID
        if "_id" in data:
            product = products.find_one({"_id": ObjectId(data["_id"])})
            if product != None :
                product = {'name':product["name"], 'description':product["description"], 'price':product["price"], 'category':product["category"], '_id':str(product["_id"])}
                return Response(json.dumps(product), status=200, mimetype='application/json')
            if product == None : 
                return Response("No product found by that ID",status=400,mimetype="application/json")
        if "name" in data and "_id" in data and "category" in data :
            return Response(json.dumps("Plase search with one of the three options every time at once: name or _id or category"),status=400,mimetype="application/json")

global shopping_cart,price_list, new_total_cost, new_price_list, cost
new_price_list = []
new_total_cost = []
price_list = []
shopping_cart = []


# Προσθήκη Προϊόντος στο καλάθι :
@app.route('/addToCart/<int:requested_stock>', methods=['PUT'])
def add_Product(requested_stock) :
        def totalPrice():
            for k in shopping_cart:
                price_list.append(price)
                if len(price_list) > 1:
                    cost = sum(price_list)
                    return cost
                if len(price_list) == 1 :
                    cost =("The Hole price displayed above!")
                    return cost
        uuid = request.headers.get('Authorization')
        if is_session_valid(uuid)    == False :
            return Response("User was not authedicated ", status=401, mimetype='application/json')
        if is_session_valid(uuid)   == True:
            id = request.args.get('id')
            if id == None:
                return Response('Bad request',status=500,mimetype="application/json")
            product = products.find_one({"_id": ObjectId(id)})
            if requested_stock > product["stock"]:
                return Response('Out of stock , Please insert a valid number' ,status=500,mimetype='application/json')
            if product != None :
                price = product["price"]*requested_stock
                product = {"_id":product["_id"], "hole_price":price, "name": product["name"], "description":product["description"], "category":product["category"], "stock":int(requested_stock)}
                shopping_cart.append(product)
                if shopping_cart != None:
                    global total_cost,sum_cost
                    total_cost= totalPrice()
                    sum_cost = total_cost
                    Products = []
                    for i in shopping_cart:
                        Products.append(i)
                    return jsonify("Products Successfully added and info is displayed(total cost is also provided)",Products,"Final cost is:",total_cost)
                else:
                    return Response(json.dumps('Shopping cart is actually emptys!'),status=500,mimetype="application/json")
            else :
                return Response(json.dumps('No product was found by the given ID'),status=500,mimetype="application/json")

# Εμφάνιση Καλαθιού
@app.route('/viewCart', methods=['GET'])
def view_cart():
    uuid = request.headers.get('Authorization')
    if is_session_valid(uuid)  == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid)  == True:
        if shopping_cart != None:
            global sum_cost
            return jsonify('Products displayed',shopping_cart,'Your receipt:',sum_cost)     
        else:
            return Response(json.dumps('Shopping cart is actually empty!'),status=500,mimetype="application/json")

global final_summary
# Διαφραφή προϊόντος απο το καλάθι μέσω του μοναδικού κωδικού 
@app.route('/deleteFromCart', methods=['DELETE'])
def delete_from_cart():
    uuid = request.headers.get('Authorization')
    if is_session_valid(uuid) == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid) == True:
            data = None 
            try:
                data = json.loads(request.data)
            except Exception as e:
                return Response("bad json content",status=500,mimetype='application/json')
            if data == None:
                return Response("bad request",status=500,mimetype='application/json')
            if not "_id" in data :
                return Response("Information incomplete",status=500,mimetype="application/json")
            global total_cost
            global final_summary
            if len(shopping_cart) != 0 :
                for k in range(len(shopping_cart)) :
                    if str(shopping_cart[k]["_id"]) == str(data['_id']):
                        global new_total_cost
                        new_total_cost = total_cost - shopping_cart[k]["hole_price"]
                        total_cost -= shopping_cart[k]["hole_price"]
                        final_summary = [("Your price after successfuly removed item: ",total_cost)]
                        del shopping_cart[k]
                        break
                    else:
                        return Response(json.dumps("The following id: "+str(data['_id'])+" does not correspond with any item of your shopping_cart"+str(shopping_cart[0]["_id"])),status=404,mimetype="application/json")
            if len(shopping_cart) == 0 :
                return Response(json.dumps("Your shopping cart is actually empty!",status=500,mimetype="application/json"))
            global sum_cost
            sum_cost = new_total_cost
            new_final_summary = [("Your price after removal: ",new_total_cost)]
            return jsonify(shopping_cart+new_final_summary)
# Αγορά προϊόντων 
@app.route('/buyProducts', methods=['GET'])
def buyProducts():
    uuid = request.headers.get('Authorization')
    card = request.args.get('card')
    if is_session_valid(uuid)  == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid)  == True:
        if len(card) > 16:
            return Response('Error a 16 digit number is only allowed',status=500,mimetype='application/json')
        if len(card) < 16:
            return Response('Error a 16 digit number is required',status=500,mimetype='application/json')
        if len(card) == 16 :
            shopping_cart.clear()
            return jsonify('Card number entered succsefully and your receipt is displayed','Products',shopping_cart,'Total Cost',sum_cost)
           
        
# Εμφάνιση ιστορικού παραγγελιών του συγκεκριμένου χρήστη 
@app.route('/OrderHistory', methods=['PATCH'])
def order_History ():
    uuid = request.headers.get('Authorization')
    if is_session_valid(uuid)  == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid)  == True:
        user = users.find_one({"email":user_email})
        if user != 0:  
            history = str(shopping_cart)
            price_history = str(sum_cost)  
            user = users.update_one({"email":user_email},
            {"$set":
                {   
                    "orderHistory": (history,'Total Price:',price_history), 
                }
            })
            user = users.find_one({"email": user_email})
            return Response(json.dumps('Order History Upgraded successfuly: /n'+str(user["orderHistory"])),status=200,mimetype="application/json")
        else:
            return Response(json.dumps('Error 404 Not Found!!', status=404,mimtype='application/json'))
         

# Διαγραφή Απλού χρήστη απο το ΠΣ.
@app.route('/deleteUser', methods=['DELETE'])
def delete_user():
    uuid= request.headers.get('Authorization')
    if is_session_valid(uuid) == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if is_session_valid(uuid) == True:
        user = users.find_one({"email": user_email})
        msg = (user['name']+' was deleted.')
        users.delete_one({"email": user_email})
        return Response(msg, status=200, mimetype='application/json')



#=================================== ENDPOINTS τα οποία αφορούν μονο τους διαχειριστές =================
#=======================================================================================================
# Δημιουργία προϊόντος
@app.route('/createProduct', methods=['PUT'])
def create_product():
    uuid= request.headers.get('Authorization')
    if admin_session_valid(uuid) == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if admin_session_valid(uuid) == True:
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "name" in data or not "price" in data or not "description" in data or not "category" in data or not "stock" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")
        if products.find({'$and':[{"name":data["name"]}, {"price":data["price"]}, {"description":data["description"]}, {"stock":data["stock"]}] }) == 0 :
            product = {"name":data["name"], "price":data["price"], "description":data["description"], "category":data['category'], "stock":data['stock']}
            products.insert_one(product)
            return Response("Product was added successfuly added to the collection",status=200,mimetype="application/json")
        else :
            return Response("Could not add the given information",status=400,mimetype='application/json')


# Διαγραφή Προϊόντος απο το κατάστημα 
@app.route('/deleteProduct/<string:_id>', methods=['DELETE'])
def delete_product(_id):
    uuid= request.headers.get('Authorization')
    if admin_session_valid(uuid) == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if admin_session_valid(uuid) == True:
        product = products.find_one({"_id":ObjectId(_id)})
        if product != None:
            msg = (product['name']+' was deleted.')
            products.delete_one({"_id": ObjectId(_id)})
            return Response(msg, status=200, mimetype='application/json')
        else:
            msg = ('No product found by the corresponding _id : '+_id)
            return Response(msg,status=400,mimetype='application/json')


# Ενημέρωση κάποιου προϊόντος
@app.route ('/updateProduct/<string:_id>', methods=['POST', 'PUT'])
def update_product(_id):
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
       return Response("bad request",status=500,mimetype='application/json')

    uuid= request.headers.get('Authorization')
    if admin_session_valid(uuid) == False :
        return Response("User was not authedicated ", status=401, mimetype='application/json')
    if admin_session_valid(uuid) == True:
       # Name
        if data["_id"] in data: 
                try:
                    data = json.loads(request.data)
                except Exception as e:
                    return Response("bad json content",status=500,mimetype='application/json')
                if data == None:
                    return Response("bad request",status=500,mimetype='application/json')
                if not "name" :
                    return Response("Information incomplete",status=500,mimetype="application/json")
                try:
                    product = products.update_one({"_id":data["_id"]},
                    {"$set": 
                        {
                            "name": str(data["name"]),
                            "price": float(data["price"]),
                            "description": str(data["description"]),
                            "stock": int(data["stock"])                                                                                                                             
                        }
                    }) 
                    product = products.find_one({"_id":data["_id"]})
                    return jsonify("Product Updated :",product)
                except Exception as e:
                    return Response("Product could not be upgraded",status=500,mimetype="application/json")
                  

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)