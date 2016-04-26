from plover.formatting import _LookAheadAction

def meta_if_next_matches(ctx, meta):
    pattern, result1, result2 = meta.split('/')
    action_list = []
    for alternative in result1, result2:
        action = ctx.new_action()
        action.text = alternative
        action_list.append(action)
    return _LookAheadAction(pattern, *action_list)
