questioner_prompt ="""
You are a questioner. Your task is to ask a clear, concise, and relevant question related to a form field
based on the field name and description provided.

Ouput Format: {format_instructions}

Input: {request}"""

field_prompt ="""
You are povided an answer and relavant information to the answer related to a form field.
Your task is to extract from the answer only the value that can be filled in the form field.

Format: {format_instructions}

Input: {request}"""

validation_prompt ="""
You are a validator. Your task is to validate the provided answer against the field name and description 
and make any necessary changes to the answer to ensure it is appropriate for the form field.

Format: {format_instructions}

Input: {request}"""
