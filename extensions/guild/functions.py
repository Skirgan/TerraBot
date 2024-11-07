from config import master_role_id

def is_master(ctx):
	return ctx.author.get_role(master_role_id) is not None