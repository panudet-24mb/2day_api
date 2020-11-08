
async def sql_update_builder(req):
  sql_builder = ""
  for key in req.json :
      sql_builder = str(sql_builder)+(str(' ') + str(key)+ str(" = " ) +str("'")+ str(req.json[key]) +str("'")+ " ,")
  sql_builder= (sql_builder[0:(len(sql_builder)) - 1])
  return sql_builder

