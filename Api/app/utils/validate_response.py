from sanic import response

#status
#message
#status_code
#dict
async def response_json(payload):
  return response.json({
            "status" : payload["status"] , 
            "payload" :  payload["message"]  , 
            } , status =  payload["status_code"]
            )
            
async def check_content_type(req):
  if req.content_type != "application/json":
    payload = {
            "status" : False , 
            "message" : "Invalid content-type. Must be application/json." , 
            "status_code" : 400
            }
    return await response_json(payload)
  else :
    return None

#compare_key = ['a' , 'b']
#req = json
async def check_json_key(req , compare_key):
  if compare_key != None :
    arr_need =[]
    arr_over =[]
    rev_key = []
    for key in req.json :
      rev_key.append(key)
    arr_over = set(rev_key) - set(compare_key)
    arr_need = set(compare_key) - set(rev_key)
    array_payload =  (list(arr_need) , list(arr_over) )
    payload = {
            "status" : False , 
            "message" : {"params_key_need"  : array_payload[0] , "params_key_invalid" : array_payload[1]}, 
            "status_code" : 400
    }
    if len(arr_over) == 0 and len(arr_need) == 0:
      return None
    return await response_json(payload)
  else:
    return None

    