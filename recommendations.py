import torch
import random
import warnings

import numpy as np
import pandas as pd
from recbole.quick_start.quick_start import load_data_and_model, run_recbole
from recbole.data.interaction import Interaction
warnings.filterwarnings("ignore")
@torch.no_grad()
def full_sort_scores(uid_series, model, test_data, device=None):
    """Calculate the scores of all items for each user in uid_series.

    Note:
        The score of [pad] and history items will be set into -inf.

    Args:
        uid_series (numpy.ndarray or list): User id series.
        model (AbstractRecommender): Model to predict.
        test_data (FullSortEvalDataLoader): The test_data of model.
        device (torch.device, optional): The device which model will run on. Defaults to ``None``.
            Note: ``device=None`` is equivalent to ``device=torch.device('cpu')``.

    Returns:
        torch.Tensor: the scores of all items for each user in uid_series.
    """
    device = device or torch.device("cpu")
    uid_series = torch.tensor(uid_series)
    uid_field = test_data.dataset.uid_field
    dataset = test_data.dataset
    model.eval()

    if not test_data.is_sequential:
        input_interaction = dataset.join(Interaction({uid_field: uid_series}))
        history_item = test_data.uid2history_item[list(uid_series)]
        
        history_row = torch.cat(
            [torch.full_like(hist_iid, i) for i, hist_iid in enumerate(history_item)]
        )
        history_col = torch.cat(list(history_item))
        history_index = history_row, history_col
    else:
        _, index = (dataset.inter_feat[uid_field] == uid_series[:, None]).nonzero(
            as_tuple=True
        )
        input_interaction = dataset[index]
        history_index = None

    # Get scores of all items
    input_interaction = input_interaction.to(device)
    try:
        scores = model.full_sort_predict(input_interaction)
    except NotImplementedError:
        input_interaction = input_interaction.repeat_interleave(dataset.item_num)
        input_interaction.update(
            test_data.dataset.get_item_feature().to(device).repeat(len(uid_series))
        )
        scores = model.predict(input_interaction)

    scores = scores.view(-1, dataset.item_num)
    scores[:, 0] = -np.inf  # set scores of [pad] to -inf
    if history_index is not None:
        scores[history_index] = -np.inf  # set scores of history items to -inf
    user_ids = test_data.dataset.field2token_id['user_id']
    
    user_ids = {value:key for key,value in user_ids.items()}
    user_ids.pop(0)
    item_ids = test_data.dataset.field2token_id['item_id']
    item_ids = {value:key for key,value in item_ids.items()}
    
    topk_values = torch.topk(scores,10)[1]
    top_k = pd.DataFrame(torch.topk(scores,10)[1].detach().cpu().numpy())
    
    for col in top_k.columns:
        top_k[col] = [item_ids[x] for x in top_k[col]]
    top_k['user_id'] = list(user_ids.values())
    top_k.columns = [str(x) for x in top_k.columns]
    new_cols = ['user_id','0','1','2','3','4','5','6','7','8','9']
    top_k = top_k[new_cols]
    return top_k
(
    config_1,
    model_1,
    dataset_1,
    train_data_1,
    valid_data_1,
    test_data_1,
) = load_data_and_model("saved/BPR-Apr-22-2023_19-30-38.pth")
total_users = list(test_data_1.dataset.field2token_id['user_id'].values())
total_users.remove(0)
df = full_sort_scores(total_users,model_1,test_data_1,config_1['device'])
df.to_csv('recommendations/recommendations.csv')