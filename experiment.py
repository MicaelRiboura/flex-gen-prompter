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

problem = """
SAF 'Floral' Framed Painting (Wood, 30 inch x 10 inch, Special Effect UV Print Textured, SAO297) 
Painting made up in synthetic frame with UV textured print which gives multi effects and attracts towards it. 
This is an special series of paintings which makes your wall very beautiful and gives a royal touch (A perfect gift for your special ones).
"""

# problem = """
# Quadro Emoldurado 'Floral' da SAF (Madeira, 30 x 10 polegadas, Impressão UV Texturizada com Efeito Especial, SAO297)
# Pintura em moldura sintética com impressão UV texturizada, que proporciona múltiplos efeitos e atrai o olhar.
# Esta é uma série especial de quadros que deixa sua parede muito bonita e confere um toque de realeza (Um presente perfeito para seus entes queridos).
# """


workflow = WorkflowFactory(model='gpt-4.1', dataset_name='ecommerce_classification').create_workflow(workflow_type='chain_of_thought')

res = workflow.run(prompt=problem)
print('Final answer: ', res.get('answer', ''))
