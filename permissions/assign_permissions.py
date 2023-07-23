from guardian.shortcuts import assign_perm


def assign_permissions(user, obj, perms):
    if perms:
        for perm in perms:
            assign_perm(perm, user, obj)
