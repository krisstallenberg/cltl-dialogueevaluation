from cltl.dialogue_evaluation.likelihood_evaluation import LikelihoodEvaluator
from cltl.dialogue_evaluation.usr_dialogue_retrieval_evaluation import USR_DialogRetrieval_Evaluator
import os
from pathlib import Path

SCENARIOS_FOLDER = Path("/Users/piek/Desktop/t-MA-Combots-2022/assignments/interaction1")

# evaluator_ft = LikelihoodEvaluator(model_path_mlm='adamlin/usr-topicalchat-roberta_ft', max_context=300,
#                                 len_top_tokens=20)

# evaluator_ctx = USR_DialogRetrieval_Evaluator(model_path_ctx='adamlin/usr-topicalchat-ctx', context_type="ctx", max_context=300,
#                                 len_top_tokens=20)

evaluator_uk = USR_DialogRetrieval_Evaluator(model_path_ctx='adamlin/usr-topicalchat-uk',context_type="fct",  max_context=300,
                                 len_top_tokens=20)



for path in os.listdir(SCENARIOS_FOLDER):
    if os.path.isdir(os.path.join(SCENARIOS_FOLDER, path)):
        # evaluator_ft.evaluate_conversation(scenario_folder=SCENARIOS_FOLDER,
        #                                 scenario_id=path,
        #                                 metrics_to_plot=['MLM llh'])
        # evaluator_ctx.evaluate_conversation(scenario_folder=SCENARIOS_FOLDER,
        #                                 scenario_id=path,
        #                                 metrics_to_plot=['Ctx Score'])
        evaluator_uk.evaluate_conversation(scenario_folder=SCENARIOS_FOLDER,
                                        scenario_id=path,
                                        metrics_to_plot=['Ctx Score'])

