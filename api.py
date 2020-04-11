from flask import Flask 
from flask_restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

CONTACTS = {
    'contact1':{'first':'eric','last':'hadley','email':'eric@domain.com','phone':'7038751234'},
    'contact2':{'first':'zach','last':'bower','email':'zach@domain.com','phone':'5715674567'},
    'contact3':{'first':'kelly','last':'johnson','email':'kelly@domain.com','phone':'9873643456'}
}

def abort_if_contact_doesnt_exist(contact_id):
    if contact_id not in CONTACTS:
        abort(404, message="Contact {} doesn't exist".format(contact_id))

parser = reqparse.RequestParser()

# declare parsers keys from payload
parser.add_argument('first')
parser.add_argument('last')
parser.add_argument('phone')
parser.add_argument('email')


# Contact
# shows a single contact item and lets you delete a contact item
class Contact(Resource):
    def get(self, contact_id):
        abort_if_contact_doesnt_exist(contact_id)
        return CONTACTS[contact_id]
    
    def delete(self, contact_id):
        abort_if_contact_doesnt_exist(contact_id)
        del CONTACTS[contact_id]
        return '', 204
    
    def put(self, contact_id):
        args = parser.parse_args()
        contact = {
            'first': args['first'],
            'last':args['last'],
            'email':args['email'],
            'phone':args['phone']
            }
        CONTACTS[contact_id]= contact
        return contact, 201

# ContactList
# shows a list of all contact, and lets you POST to new contacts
class ContactList(Resource):
    def get(self):
        return CONTACTS

    def post(self):
        args = parser.parse_args()
        contact_id = int(max(CONTACTS.keys()).lstrip('contact')) + 1
        contact_id = 'contact%i' % contact_id
        contact = {
            'first': args['first'],
            'last': args['last'],
            'email': args['email'],
            'phone': args['phone'],
            }
        CONTACTS[contact_id] = contact
        return CONTACTS[contact_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contact/<contact_id>')

if __name__ == '__main__':
    app.run(debug=True)