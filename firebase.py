import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


cred = credentials.Certificate('easy-go-mobile-firebase-adminsdk-ql8au-8bd00e2c82.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def make_transaction(userId, transaction_amount):

    collection_ref = db.collection('users')

    doc = get_doc(collection_ref, userId)

    if not doc:
        return "Error: User not registered"

    # Task 1: Update the field 'balance'
    current_balance = doc.get("balance")
    new_balance = current_balance - transaction_amount

    if new_balance < 0:
        return "Error: Insufficient Balance"

    # Update the document
    collection_ref.document(doc.id).update({"balance": new_balance})

    transaction_data = {
        "amount": transaction_amount,
        "time": datetime.now(),
        "provider": "Windsor Transit"
    }

    # Task 2: Add a new document to the 'transaction' subcollection
    transaction_subcollection_ref = collection_ref.document(doc.id).collection("transaction")
    transaction_subcollection_ref.add(transaction_data)

    # Task 3: Remove previous documents in 'recentPayment' subcollection
    recent_payment_subcollection_ref = collection_ref.document(doc.id).collection("recentPayment")
    old_payments = recent_payment_subcollection_ref.stream()
    
    # Delete old documents
    for old_payment in old_payments:
        recent_payment_subcollection_ref.document(old_payment.id).delete()

    # Add a new document to 'recentPayment'
    recent_payment_subcollection_ref.add(transaction_data)

    return "Done with boarding"


def get_doc(collection_ref, userId):

    document_ref = collection_ref.where("uid", "==", userId).limit(1).get()

    if not document_ref:
        print(f"No document found with userId {userId}")
        return False
    
    doc = document_ref[0]

    return doc

# make_transaction("01237")