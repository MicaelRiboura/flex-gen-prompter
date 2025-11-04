prompts = {
    'expand_node': {
        'gsm8k': """
            Answer the following question: 
            {problem}
            Make a strategy then write. Your output should be of the following format:
            Strategy:
            {strategy}
            Your strategy about how to answer the question.
            Complete with only the next strategic and concise step to solve this problem.
            Your output should be of the following format:
            i (where i is a number). Description of step.
            If you think that the last step of strategy is the final to classify, add to this sentence the answer.
            Your answer to the question. It should end in this format: "the answer is ##n" where n is a number. Please, keep '##' symbol.
        """,
        'ecommerce_classification': """
            You are an AI assistant and you are very good at doing ecommerce products classification.
            You are going to help a customer to classify the products in the ecommerce website.
            Based on the context bellow:
            Product Description:
            {problem}
            Strategy:
            Your strategy about how to classify the product based on product description enumerated step-by-step.
            {strategy}
            
            Complete with only the next strategic and concise step to classify this product description. 
            Your output should be of the following format:
            i (where i is a number). Description of step.
            If you think that the last step of strategy is the final to classify, add to this sentence the answer.
            You are only allowed to choose one of the following 4 categories:
            - Household
            - Books
            - Clothing & Accessories 
            - Electronics
            It should end with "The answer is ##c", where c is the name of one of the 4 categories above. Please, keep '##' symbol.
        """,
  },
    'evaluate_node': {
        'gsm8k': """
            Problem:
            {problem}
            Strategy:
            Your strategy about how to solve this problem enumerated step-by-step.
            {strategy}
            Given an instruction and several choices,
            decide which choice is most promising.
            Analyze each choice in detail, then conclude in the last line
            "The best choice is s", where s the integer id of the choice.
            {choices}
        """,
        'ecommerce_classification': """
            Product Description:
            {problem}
            Strategy:
            Your strategy about how to classify the product based on product description enumerated step-by-step.
            {strategy}
            Based on the product description, current strategic steps above and the several choices bellow,
            decide which choice is most promising to complete this strategy.
            Analyze each choice in detail, then conclude in the last line
            "The best choice is s", where s the integer id of the choice.
            {choices}
        """,
    }
}