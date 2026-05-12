import json
import unittest
import boto3
import app as app


class MyTestCase(unittest.TestCase):
    def test_something(self):
        client = boto3.client('cognito-idp')
        response = client.get_user(
            AccessToken='eyJraWQiOiJXWmZUWHJpNkxDTnEyT0ZnMkNNTUJSQ1BLSEJWK2tLaU1wUTcwSzRnNmkwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1YmU1Yjg5Yi1jMzJmLTQwMTktYjYyOC04OTBmOGZkZDM2MDIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9MemwxOFZWR0UiLCJjbGllbnRfaWQiOiI1bGVxbjd2bXZ0dWRxcXV2cWRsdmJlZnU5MSIsIm9yaWdpbl9qdGkiOiI0YjVlNjY3Zi0xMzk5LTQ4ZTgtODUzZC01ZDFiN2FjMjZkNTUiLCJldmVudF9pZCI6IjUxMWM5Y2Q3LTU0MzYtNDhkMi1iOGUyLWJjMDUyYjIyYjRlYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2OTIyOTEzNjIsImV4cCI6MTY5MjM3Nzc2MiwiaWF0IjoxNjkyMjkxMzYyLCJqdGkiOiJjODg1ZjdjNy1mZWQwLTRiNjEtYWQ3Ni0xMjY3NDE2MjgxOTQiLCJ1c2VybmFtZSI6IjViZTViODliLWMzMmYtNDAxOS1iNjI4LTg5MGY4ZmRkMzYwMiJ9.oknVFV87_PACBkAw2Fd-WzejnxOdmiMQoo7Rkh4m3FEoYJEU8gEwnHcuajGjVDhtxkftHXfGyROh5z549LSUkBFKKAAoTeY2FKUuzlEV68srCOzhWuvANqoTsZfvphTsDnFu1vwZzHsDkWomgYGXN-TewTRGAO2pTe7kfWjU-lYl-2EjQ4NyXrr8WMj4lyI_nmz_sFVH3DswAcLUCYMFIw-iR71L4-pdOwWVX05hKJb3Qjwe8BTYoC89DnwBANkamWWG5yAcNqn-kRQ1QMuGjt_dX2ctnddXQ1L2I-wyUt2MakQ-LCwg3vayFM717A1s_jeRzRA2C8ojuzlSPxqPSw'
        )
        print(response)
        # self.assertEqual(True, False)  # add assertion here

        EntityList = "beta_EntityList"
        UserRoleDetail = "beta_UserRoleDetail"
        role_id = 1
        query = f"""select {EntityList}.EntityName,{EntityList}.Path, {UserRoleDetail}.RoleId, {UserRoleDetail}.OrderNum from beta_EntityList, beta_UserRoleDetail
                    where {UserRoleDetail}.RoleId={role_id} and {UserRoleDetail}.EntityCode={EntityList}.EntityCode
                    order by OrderNum """
        print(query)

    def test_sign_in(self):
        body = {
            "username": "shahnawazbevanoor676@gmail.com",
            "password": "Shahanwaz@321"
        }
        pathParameters = {
            "action": "sign_in",
            "stage_name":"beta"
        }
        event = {
            'pathParameters':pathParameters,
            'body': json.dumps(body)
        }
        res = app.lambdaHandler(event,None)
        print(json.loads(res.get('body')))

if __name__ == '__main__':
    unittest.main()
