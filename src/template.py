# 使用精确搜索方式
prompt_template_Document ='''"Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        the answer must be chinese.
        {context}

        Question: {question}
        Answer:"""
        '''
# 使用联想搜索方式
prompt_template_GPT ='''"ased on the provided context and question, 
        return a well-organized answer that does not exceed the scope of the context.
        {context}

        Question: {question}
        Answer:"""
        '''
