
import requests
import random
import string

class Galigali:
    def __init__(self, username, password, prodId, accountNumber):
        self.username = username
        self.password = password
        self.prodId = prodId
        self.accountNumber = accountNumber
    
    
    access_token = ""
    transactionId = ""
    spending_account = ""




    def randomString(self, stringLength):
        # Generate a random string of fixed length
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))


    # Authentication

    def Authentication(self, uname,passw):
        url = "https://sandbox.galileo-ft.com/intserv/4.0/login"

        payload = {"username":uname, "password":passw}    
        request = requests.post(url, json=payload, headers={})
        response = request.json()
        # print(response)
        return [request.json(),response["access_token"]]
        # print(access_token)



    # access_token = Authentication(username,password)[1]
    def setAccessToken(self):
        self.access_token = self.Authentication(self.username,self.password)[1]



    # print(setAccessToken())

    # create account




    def createAccount(self, transactionId, access_token):
        # print(transactionId,access_token)
        url = "https://sandbox.galileo-ft.com/intserv/4.0/createAccount"
        payload = {"transactionId": transactionId,
            "prodId":self.prodId,
            "firstName": "robert",
            "lastName": "wilson"}
        headers = {
            'Authorization': "Bearer " + access_token,
            'Content-Type': "application/json",
            'response-content-type': "json"}
        # # print(headers['Authorization'])
        request = requests.request("POST",url, json=payload, headers=headers)

        # print(request.json())
        
        spending_account = request.json()["response_data"][0]["pmt_ref_no"]
        # print(spending_account)
        return [request.json(),spending_account]



    def setSpendingAccount(self):
        self.spending_account = self.createAccount(self.transactionId,self.access_token)[1]
        # print(spending_account)



    # transfer

    def transfer(self,transactionId):
        url = "https://sandbox.galileo-ft.com/intserv/4.0/createAccountTransfer"

        payload = "{\n\t\"transactionId\": \"ac983703-b964-4460-a90d-0c3750719662\",\n\t\"accountNo\": \"283101000570\",\n\t\"amount\": 100.0,\n\t\"transferToAccountNo\": \"276101001895\"\n}"
        payload = {"transactionId": transactionId,
            "accountNo" : self.accountNumber,
            "amount" : "15.00",
            "transferToAccountNo" : self.spending_account
            }
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'Content-Type': "application/json",
            'response-content-type': "json",
            }

        request = requests.post(url, json=payload, headers=headers)

        return request.json()

    # transfer()


    # getBalance
    def getBalance(self,transactionId):
        url = "https://sandbox.galileo-ft.com/intserv/4.0/getBalance"

        payload = {
            "transactionId" : transactionId,
            "accountNo" : self.spending_account
        }
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'Content-Type': "application/json",
            'response-content-type': "json"
            }

        request = requests.post(url, json=payload, headers=headers)

        return request.json()


    # getBalance()


    # simCardAuth
    def simCardAuth(self, transactionId):
        url = "https://sandbox.galileo-ft.com/intserv/4.0/createSimulatedCardAuth"

        payload = {
            "transactionId" : transactionId,
            "accountNo" : self.spending_account,
            "amount" : 4.0,
            "merchantName" : "Scuffed_Pizza",
            "association" : "mc_auth"
        }
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'Content-Type': "application/json",
            'response-content-type': "json"
            }

        request = requests.post(url, json=payload, headers=headers)

        return request.json()

    # simCardAuth()


    # getAuthHist
    def getAuthHist(self,transactionId):
        url = "https://sandbox.galileo-ft.com/intserv/4.0/getAuthHistory"

        payload = {
            "transactionId" : transactionId,
            "accountNo" : self.spending_account
        }
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'Content-Type': "application/json",
            'response-content-type': "json",
            }

        request = requests.post(url, json=payload, headers=headers)

        return request.json()


    def createAccountTransfer(self,transactionId, amount, transferToAccountNo):
        url='https://sandbox.galileo-ft.com/intserv/4.0/createAccountTransfer'
        payload = {
            'transactionId': transactionId,
            'accountNo': self.accountNumber,  
            'amount': amount, 
            'transferToAccountNo': transferToAccountNo}
        header = {
            'Authorization': "Bearer " + self.access_token,
            'Content-Type': "application/json",
            'response-content-type': "json",
        }
        request = requests.post(url, json=payload, headers=header)
        # print('createAccountTransfer response code: ' + r.json()['status_code'])
        print(request.text)
        print(request.json())



    # getAuthHist()
    # print("good")


# if __name__== "__main__" :
#     g = Galigali("T2_alU-0139","bWtGTLuQ33Q8YHx1","9614","283101000570")
#     g.setAccessToken()
#     # g.Authentication(g.username,g.password)
#     g.transactionId = g.randomString(30)
#     # g.createAccount(g.transactionId,g.access_token)
#     g.setSpendingAccount()
#     g.transfer(g.transactionId)
#     g.getBalance(g.transactionId)
#     g.simCardAuth(g.transactionId)
#     g.getAuthHist(g.transactionId)
#     g.createAccountTransfer(g.transactionId,15.0,"283101000539")