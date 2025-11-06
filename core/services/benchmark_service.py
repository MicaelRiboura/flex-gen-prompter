from flexgenprompterlib import WorkflowFactory, AccuracyMetric
import tqdm
import re

class BenchmarkService:
    def evaluate(self, model, dataset_data, techniques, num_samples=None, update_state=lambda **kwargs: None):
        total = len(dataset_data)
        techniques_scores = {}
        total = total * len(techniques)
        steps = 0
        for technique in techniques:
            workflow = WorkflowFactory(model=model, dataset_name=self.dataset_name).create_workflow(technique)

            preds = []
            labels = []
            for i, data in enumerate(tqdm(dataset_data)):
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
            
            score = AccuracyMetric().compute(preds, labels)
            techniques_scores[technique] = score

        return techniques_scores