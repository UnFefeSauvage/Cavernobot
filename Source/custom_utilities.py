def has_role(member, roleid):
    for role in member.roles:
        if role.id == roleid:
            return True

    return False

async def toggle_role(member, roleid):
    role = discord.Object(roleid)
    if has_role(member, roleid):
        await member.remove_roles(role)
        print("%s had the role, I removed it." % (member.name))
    else:
        await member.add_roles(role)
        print("gave the frole to %s" % (member.name))