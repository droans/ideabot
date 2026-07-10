from src.util import filter_ideas, format_ideas
from interactions import Guild, Client, Listener
from interactions.api.events import Component



async def on_component(event: Component) -> None:
  """Respond to search request."""
  ctx = event.ctx
  component_id = ctx.custom_id
  kwargs = {}
  if component_id == "name_select":
    kwargs["name"] = ctx.values
  if component_id == "category_select":
    kwargs["category"] = event.ctx.values
  guild = ctx.guild
  server_name = guild.name if isinstance(guild, Guild) else ""
  channel = ctx.channel
  if channel and isinstance(channel.name, str):
    channel_name = channel.name
  else:
    channel_name = ""
  user = ctx.author
  user_name = user.global_name
  if not user_name:
    raise ValueError("Can't discern user name")
  ideas = filter_ideas(
    server=server_name,
    channel=channel_name,
    user=user_name,
    **kwargs,
  )
  await ctx.send(format_ideas(ideas))

def add_component_listener(bot: Client) -> Listener:
  """Subscribes the mention listener to the bot."""
  listen_func = Listener.create("Component")
  result = listen_func(on_component)
  bot.add_listener(result)
  return result
