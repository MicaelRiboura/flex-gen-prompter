import json

class AccuracyMetric:
    def format_json_or_str(self, text):
        if '{' in text:
            try:
                if "'" in text: 
                    text = text.replace("'", '"')
                
                return json.loads(text)
            except Exception:
                return str(text).lower()
        else:
            return str(text).lower()
    
    def compute(self, predictions, ground_truths):
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
            predictions = [pred if type(pred) == dict else str(pred).lower() for pred in predictions]
            ground_truths = [self.format_json_or_str(ground_truth) for ground_truth in ground_truths]
            print('predictions: ', predictions)
            print('ground_truths: ', ground_truths)
        except AttributeError:
            print("Something in either preds or gts can not be convert to a string.")
            
        if not isinstance(predictions, list):
            predictions = [predictions]
            ground_truths = [ground_truths]

        return sum(a == b for a, b in zip(predictions, ground_truths)) / len(ground_truths)
