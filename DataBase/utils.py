def get_most_eaten(records, dishes):
    cnt = dict()
    for dish in dishes:
        cnt[dish[0]] = 0
    for _, dish_id, _ in records:
        cnt[dish_id] += 1
    return cnt


def get_most_fav(records, dishes):
    cnt = dict()
    for dish in dishes:
        cnt[dish[0]] = 0
    for _, dish_id in records:
        cnt[dish_id] += 1
    return cnt


def get_recommandation(ate, fav, dishes):
    eaten_weight = get_most_eaten(ate, dishes)
    fav_weight = get_most_fav(fav, dishes)
    ew_sum = sum(eaten_weight.values())
    fw_sum = sum(fav_weight.values())
    cnt = dict()
    for dish_id, ew in eaten_weight.items():
        cnt[dish_id] = ew / (ew_sum + 0.00001) + fav_weight[dish_id] / (fw_sum + 0.00001)
    info = [(dish_id, times) for dish_id, times in cnt.items()]
    info.sort(key=lambda x: x[1], reverse=True)
    return info


def search_by_name(name, dishes):
    return [dish[0] for dish in dishes if name in dish[1]]


def search_by_adj(adj, dishes, mapping: dict):
    k = mapping[adj]
    fits = []
    for dish in dishes:
        fixed_attr = dish[4] | (dish[3] << 5) | (dish[2] << 6)
        if fixed_attr & k > 0:
            fits.append(dish[0])
    return fits
