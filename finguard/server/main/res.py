def generate_res(data=None, err=None):
    return {
        "success": err == None,
        "data": data,
        "err":err
          }