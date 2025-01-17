from config import firebaseKey,memberTable, companyId, role
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate(firebaseKey)
app=initialize_app(cred)
dbPath = firestore.client()

def postMember(memberName ,lineId):
    member = {
        "name" : memberName,
        "lineId" : lineId,
        "role" : role
    }
    memberCollection = dbPath.collection(memberTable)
    memberList = list(doc._data for doc in memberCollection.stream())
    for memberdata in memberList:
        print(memberdata)
        if memberdata["lineId"] == lineId:
            return memberdata
    # create memberdata in members
    memberId = memberCollection.add(member)[1].id
    memberCollection.document(memberId).update({'id' : memberId})

    # create memberid in company
    dbPath.document(f"companies/{companyId}/members/{memberId}").set(None)

    return {
        "name" : memberName,
        "lineId" : lineId,
        "id" : memberId
    }
