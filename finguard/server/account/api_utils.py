from drf_spectacular.utils import OpenApiExample

def custom_postprocessing_hook(result, generator, **kwargs):
    # This logic wraps your schemas in the "msg" dictionary globally for the docs
    for path in result['paths'].values():
        for method in path.values():
            if 'responses' in method:
                for status, response in method['responses'].items():
                    if 'content' in response:
                        schema = response['content']['application/json']['schema']
                        # Wrap the existing schema in a 'msg' object
                        response['content']['application/json']['schema'] = {
                            'type': 'object',
                            'properties': {
                                'msg': schema
                            }
                        }
    return result
