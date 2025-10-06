from core.prompting_techniques.workflow_factory import WorkflowFactory
from dotenv import load_dotenv
from core.prompting_techniques.utils import save_tree_thoughts_graph

load_dotenv()

# problem = """
# Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. 
# She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?
# """


# workflow = WorkflowFactory(model='gpt-4.1').create_workflow(workflow_type='tree_of_thoughts')

# res = workflow.run(prompt=problem)
# print('Final answer: ', res.get('candidates', [''])[0])
# G = res.get('G', {})
# save_tree_thoughts_graph(G, filename='test')

# problem = """
# SAF 'Floral' Framed Painting (Wood, 30 inch x 10 inch, Special Effect UV Print Textured, SAO297) 
# Painting made up in synthetic frame with UV textured print which gives multi effects and attracts towards it. 
# This is an special series of paintings which makes your wall very beautiful and gives a royal touch (A perfect gift for your special ones).
# """
problem = """
Desire, Discord and Death: Approaches to the Ancient near Eastern Myth (Asor Books) About the Author Neal Walls is Associate Professor of Old Testament Interpretation at Wake Forest University. A scholar of the Hebrew Bible/Old Testament and related ancient Near Eastern texts, Walls is fascinated by the breadth, depth, and complexity of Old Testament literature. He enjoys helping students to become skillful interpreters of scripture, to appreciate the diversity of theological perspectives within the canon, and to reclaim the Old Testament's abundant theological imagination for the church's ministries today. Walls also leads pilgrimages and travel programs to Africa and the Middle East.
"""

# problem = """
# Quadro Emoldurado 'Floral' da SAF (Madeira, 30 x 10 polegadas, Impressão UV Texturizada com Efeito Especial, SAO297)
# Pintura em moldura sintética com impressão UV texturizada, que proporciona múltiplos efeitos e atrai o olhar.
# Esta é uma série especial de quadros que deixa sua parede muito bonita e confere um toque de realeza (Um presente perfeito para seus entes queridos).
# """


workflow = WorkflowFactory(model='gpt-4.1', dataset_name='ecommerce_classification').create_workflow(workflow_type='tree_of_thoughts')

res = workflow.run(prompt=problem)
print('Final answer: ', res.get('answer', ''))
print('Steps: ', res.get('steps', []))
G = res.get('G', {})
print('graph G: ', G)
# G = {
#   "\nDesire, Discord and Death: Approaches to the Ancient near Eastern Myth (Asor Books) About the Author Neal Walls is Associate Professor of Old Testament Interpretation at Wake Forest University. A scholar of the Hebrew Bible/Old Testament and related ancient Near Eastern texts, Walls is fascinated by the breadth, depth, and complexity of Old Testament literature. He enjoys helping students to become skillful interpreters of scripture, to appreciate the diversity of theological perspectives within the canon, and to reclaim the Old Testament's abundant theological imagination for the church's ministries today. Walls also leads pilgrimages and travel programs to Africa and the Middle East.\n": [
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.',
#     '1. Identify the primary nature and purpose of the product described, focusing on whether it is a physical object for household use, a literary work, an item of apparel/accessory, or an electronic device. The answer is Books.',
#     '1. Identify the main type of product being described by looking for keywords such as "book," "author," "literature," or references to academic study, publishing, or related terminology. The answer is Books.',
#     '1. Identify the main subject of the product description to determine if it matches one of the provided categories. The answer is Books.',
#     '1. Identify the primary function and subject of the product described, focusing on whether it is an item to be read, worn, used in a household, or an electronic device. The answer is Books.'
#   ],
#   '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.': [
#     '2. Match the identified keywords to the most relevant category from the provided options to confirm classification. The answer is Books.',
#     '2. Determine if the product fits within the definition of any of the provided categories by analyzing the identified keywords and overall context. The answer is Books.',
#     '2. Match the identified keywords to the most relevant category from the provided options, confirming that terms like "Author," "Old Testament," and "ASOR Books" are most closely associated with Books. The answer is Books.',
#     '2. Match the identified keywords to the most relevant category from the provided list, confirming that terms such as "Author," "Old Testament," and "ASOR Books" clearly indicate that the product is a book. The answer is Books.',
#     '2. Match the identified keywords to the most relevant category among the provided options and confirm that the product fits best under "Books." The answer is Books.'
#   ],
#   '1. Identify the primary nature and purpose of the product described, focusing on whether it is a physical object for household use, a literary work, an item of apparel/accessory, or an electronic device. The answer is Books.': [
    
#   ],
#   '1. Identify the main type of product being described by looking for keywords such as "book," "author," "literature," or references to academic study, publishing, or related terminology. The answer is Books.': [
    
#   ],
#   '1. Identify the main subject of the product description to determine if it matches one of the provided categories. The answer is Books.': [
    
#   ],
#   '1. Identify the primary function and subject of the product described, focusing on whether it is an item to be read, worn, used in a household, or an electronic device. The answer is Books.': [
    
#   ],
#   '2. Match the identified keywords to the most relevant category from the provided options to confirm classification. The answer is Books.': [
    
#   ],
#   '2. Determine if the product fits within the definition of any of the provided categories by analyzing the identified keywords and overall context. The answer is Books.': [
    
#   ],
#   '2. Match the identified keywords to the most relevant category from the provided options, confirming that terms like "Author," "Old Testament," and "ASOR Books" are most closely associated with Books. The answer is Books.': [
    
#   ],
#   '2. Match the identified keywords to the most relevant category from the provided list, confirming that terms such as "Author," "Old Testament," and "ASOR Books" clearly indicate that the product is a book. The answer is Books.': [
#     '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.',
#     '2. Match the identified keywords to the most relevant category from the provided list, confirming that terms such as "Author," "Old Testament," and "ASOR Books" clearly indicate that the product is a book. The answer is Books.',
#     '3. Since the keywords match only the "Books" category and do not relate to Household, Clothing & Accessories, or Electronics, finalize the classification. The answer is Books.',
#     '3. Confirm that none of the keywords or context suggest categories such as Household, Clothing & Accessories, or Electronics, ensuring that "Books" is the most accurate classification. The answer is Books.',
#     '2. Match the identified keywords to the most relevant category from the provided list, confirming that terms such as "Author," "Old Testament," and "ASOR Books" clearly indicate that the product is a book. The answer is Books.'
#   ],
#   '2. Match the identified keywords to the most relevant category among the provided options and confirm that the product fits best under "Books." The answer is Books.': [
    
#   ],
#   '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.': [
#     '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.',
#     '4. Finalize the classification by assigning the product to the Books category based on all previous steps. The answer is Books.',
#     '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.',
#     '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.',
#     '3. Confirm that none of the keywords or context in the description relate to Household, Clothing & Accessories, or Electronics, ensuring Books is the most accurate classification. The answer is Books.'
#   ],
#   '3. Since the keywords match only the "Books" category and do not relate to Household, Clothing & Accessories, or Electronics, finalize the classification. The answer is Books.': [
    
#   ],
#   '3. Confirm that none of the keywords or context suggest categories such as Household, Clothing & Accessories, or Electronics, ensuring that "Books" is the most accurate classification. The answer is Books.': [
    
#   ],
#   '4. Finalize the classification by assigning the product to the Books category based on all previous steps. The answer is Books.': [
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.',
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.',
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.',
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.',
#     '1. Identify keywords in the product description that indicate the nature and purpose of the product (e.g., "Author," "Old Testament," "literature," "Interpretation," "scholar," "ASOR Books"). The answer is Books.'
#   ]
# }
save_tree_thoughts_graph(G, filename='test')