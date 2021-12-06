from collections import Counter

import numpy

import Viewer as v
import graphviz

#  Returns the a list of visitor ids for the users
#  that have visited the document
def findReaders(document):
    df = v.views(document)
    users = df['visitor_uuid']
    return users.values


#  Takes a visitorid and returns a list of documents
#  they have visited as a list of ids
def userHasRead(user):
    df = v.dataset.copy()
    df = df[df.visitor_uuid == user]
    df = df[df.event_type == 'read']
    documents = df['env_doc_id']
    return documents.values


#  Takes a list of document ids and sorts them
def sortDocuments(documents):
    documents.sort(key=Counter(documents).get, reverse=True)
    documents = list(dict.fromkeys(documents))
    return documents


#  Takes a document and optionally a user and a sorting function
#  and returns a list of the ten documents that have been
#  read by the most users, sorted with the inputted sorting algorithm
#  that have also read the input document
def alsoLikes(document,userIn=None,sortF=sortDocuments):
    users = findReaders(document)
    if(userIn!=None):
        numpy.append(users,userIn)
    documents = []
    for user in users:
        userDocs = userHasRead(user)
        documents.extend(userDocs)
    documents = sortF(documents)[:9]
    return documents
#
def buildGraph(documentIn,userIn=None,sortF=sortDocuments):
    documents = alsoLikes(documentIn,userIn,sortF)
    graph = graphviz.Digraph()

    graph.node('Documents', 'Documents', shape='plaintext', rank='Documents')
    graph.node('Readers', 'Readers', shape='plaintext', rank='Readers')
    graph.edge('Readers', 'Documents')
    addedUsers = findReaders(documentIn)
    for addedUser in addedUsers:
        userNodeLabel = addedUser[11:15]
        if (addedUser == userIn):
            graph.node(addedUser, userNodeLabel, style='filled', color='green', shape='box', rank='Readers')
        else:
            graph.node(addedUser, userNodeLabel, shape='box', rank='Readers')

    for document in documents:
        docNodeLabel = document[41:45]
        if(document==documentIn):
            graph.node(document, docNodeLabel, style='filled', color='green', shape='circle', rank='Readers')
        else:
            graph.node(document, docNodeLabel, shape='circle', rank='Readers')
        users=findReaders(document)
        for user in users:
            if addedUsers.__contains__(user):
                graph.edge(user, document)

    return graph
