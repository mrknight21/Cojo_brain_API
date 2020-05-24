# Import the Firebase service
from firebase_admin import auth as frb_auth, firestore
import firebase_admin
from config import Config

def firebase_init():
    if (not len(firebase_admin._apps)):
        cred = firebase_admin.credentials.Certificate(Config.FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)


class Firestore_query(object):
    QUERY_OPERATORS = ['<', '<=', '==', '>', '>=', 'array-contains', 'in', 'array-contains-any']

    def __init__(self, field, operator, value):
        self.field = field
        if operator in self.QUERY_OPERATORS:
            self.operator = operator
        else:
            self.operator = None
            raise Exception("Operators is invalid")
        self.value = value

    def to_tuple(self):
        if self.field and self.operator and self.value:
            return (self.field, self.operator, self.value)

    def join_query(self, ref):
        q = self.to_tuple()
        if q:
            return ref.where(q[0], q[1], q[2])
        else:
            return ref

class Firestore_order(object):

    def __init__(self, field, desc = True):
        self.field = field
        self.desc =desc

    def join_query(self, ref):
        if self.field:
            if self.desc:
                return ref.order_by(self.field, direction=firestore.Query.DESCENDING)
            else:
                return ref.order_by(self.field, direction=firestore.Query.ASCENDING)


class Firebase_conn(object):

    MAX_BATCH_WRITE =450

    def __init__(self, base_collection = None):
        if (not len(firebase_admin._apps)):
            cred = firebase_admin.credentials.Certificate(Config.FIREBASE_CRED_PATH)
            firebase_admin.initialize_app(cred)
        self.cli = firestore.client()
        self.base_collection = base_collection

    # Add single doc into the collection with or without the custom key
    def insert(self, data, collection=None, doc_id = None, reference = None,  mode = 'set', merge = False):
        if not collection:
            collection = self.base_collection
        try:
            if doc_id:
                if reference:
                    ref = reference
                else:
                    ref = self.cli.collection(collection).document(doc_id)
                if mode == 'set':
                    ref.set(data, merge = merge)
                elif mode == 'update':
                    ref.update(data)
            else:
                if reference:
                    ref = reference
                else:
                    ref = self.cli.collection(collection)
                ref.add(data)
        except Exception as e:
            print(e)

    def nesting_insert(self, ref_path, data, collection= None, mode= 'set', merge = False):
        if not collection:
            collection = self.base_collection
        ref = self.cli.collection(collection)
        cur_type = 'collection'
        doc_id = None
        for fb_type, obj_id in ref_path:
            if cur_type == 'collection' and cur_type == fb_type: raise Exception('Nesting {} directly under {}'.format(cur_type, cur_type))
            if fb_type == 'collection':
                ref = ref.collection(obj_id)
                doc_id = None
            elif fb_type == 'document':
                ref = ref.document(obj_id)
                doc_id = obj_id
        self.insert(data, reference=ref, mode = mode, doc_id=doc_id, merge =  merge)



    def bulk_insert(self, data_list, collection =None, mode = 'set'):
        if not collection:
            collection = self.base_collection
        count = 0
        batch = self.cli.batch()
        try:
            for doc_id, data in data_list:
                if count >self.MAX_BATCH_WRITE:
                    batch.commit()
                    batch = self.cli.batch()
                    count = 0
                ref = self.cli.collection(collection).document(doc_id)
                if mode == 'set':
                    batch.set(ref, data)
                elif mode == 'update':
                    batch.update(ref, data)
                count += 1
            if count > 0:
                batch.commit()
        except Exception as e:
            print(e)

    def find_one(self, doc_id, collection=None):
        if not collection:
            collection = self.base_collection
        return self.cli.collection(collection).document(doc_id).get()

    def find_many(self, collection=None, query= None, order_by = None, limit = None):
        if not collection:
            collection = self.base_collection
        ref = self.cli.collection(collection)
        if query:
            for q in query:
                ref = q.join_query(ref)
        if order_by:
            ref = order_by.join_query(ref)
        if limit:
            ref = ref.limit(limit)
        results = ref.stream()
        return results
    #
    # def delete_one(self, collection, query):
    #     self.db_conn[collection].delete_one(query)

    # def update_one(self, collection, query, content, upsert = False):
    #     update_content = {'$set': content}
    #     self.db_conn[collection].update_one(query, update_content, upsert = upsert)
    #
    # def update_many(self, collection, query, content, upsert = False):
    #     update_content = {'$set': content}
    #     self.db_conn[collection].update_many(query, update_content, upsert=upsert)

def db_test():
    firebase_db = Firebase_conn(base_collection='test')
    data = [('monkey', {'weight':50, 'name': 'John'}), ('Cat', {'weight':10, 'name':'cathy'})]
    firebase_db.bulk_insert(data)



if __name__ == "__main__":
    db_test()