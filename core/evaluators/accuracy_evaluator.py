from tqdm import tqdm
import re
from core.prompting_techniques.workflow_factory import WorkflowFactory
from core.services.datasets_service import DatasetsService

class AccuracyEvaluator:
    def __init__(self, dataset_name, model, techniques):
        service = DatasetsService()
        self.dataset_name = dataset_name
        self.dataset = service.get_dataset(dataset_name)
        self.model = model
        self.total = len(self.dataset)
        self.techniques = techniques

    def extract_answer(self, output):
        print(f'output: {output}')
        answer = output.replace('.', '')
        # answer = [s for s in re.findall(r'-?\d+\.?\d*', answer)]
        # answer = answer[0] if len(answer) > 0 else ""
        return answer

    def compute_accuracy(self, preds, gts):
        """
        Computes classification accuracy based on predictions and ground truths.

        Parameters:
        -----------
        preds : list
            A list of predictions.
        gts : list
            A list of ground truths.

        Returns:
        --------
        float
            The classification accuracy.
        """
        try:
            preds = [str(pred).lower() for pred in preds]
            gts = [str(gt).lower() for gt in gts]
        except AttributeError:
            print("Something in either preds or gts can not be convert to a string.")
            
        if not isinstance(preds, list):
            preds = [preds]
            gts = [gts]

        return sum(a == b for a, b in zip(preds, gts)) / len(preds)

    def evaluate(self, examples=[], num_samples=None, update_state=lambda **kwargs: None):
        techniques_scores = {}
        self.total = self.total * len(self.techniques)
        steps = 0
        for technique in self.techniques:
            workflow = WorkflowFactory(model=self.model, dataset_name=self.dataset_name).create_workflow(technique)

            preds = []
            labels = []
            for i, data in enumerate(tqdm(self.dataset)):
                if num_samples and i >= num_samples:
                    break
                
                label = data['label']
                labels.append(label.lower())
                
                input_text = data['content']

                update_state(
                    state='PROGRESS', 
                    meta={
                        'current': steps + 1, 
                        'total': num_samples * len(self.techniques) if num_samples and num_samples <= self.total else self.total
                    }
                )
                # try:
                if len(examples) > 0:
                    output = workflow.run(prompt=f'{input_text}', examples=examples)
                else:
                    output = workflow.run(prompt=f'{input_text}')
                    # save_tree_thoughts_graph(output.get("G", {}), filename=f"thoughts_graph/tree_of_thoughts_graph{i}.png")
                # except Exception as e:
                #     print(f"Error processing data index {i}: {e}")
                #     print(e)
                #     preds.append("Error")
                #     continue

                res = re.findall(r'##(.*)', output['answer'])
                pred = res[0] if res else output['answer']
                pred = self.extract_answer(pred)

                preds.append(pred)
                steps += 1
            
            score = self.compute_accuracy(preds, labels)
            techniques_scores[technique] = score

        return techniques_scores