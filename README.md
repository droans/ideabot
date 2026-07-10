# Ideabot

Discord bot for saving ideas

## Features
* Save and retrieve ideas via slash commands
* Or, save an idea by replying to a message and tagging the ideabot
* All ideas are saved with references to the user, server, and channel. They can only be retrieved by the same user on the same server and channel.

## Usage

### Slash Commands:

#### `/idea`

Store your idea. The user, channel, and server are automatically picked up from context. Replies with a thumbs-up emoji 

Replies with a Thumbs-up emoji if successful. If there's an error, it will reply with a thumbs-down emoji and a message.

**Arguments:**

| Argument | Type | Required | Description                                 |
|----------|------|----------|---------------------------------------------|
| idea     | str  | yes      | The description of your idea                |
| name     | str  | no       | An optional name to give to your idea       |
| category | str  | no       | An optional category to assign to your idea |

### `/remember`

Fetch your stored ideas. Will only return ideas stored by you in the same channel and server.

Replies with all filtered ideas.

**Arguments:**

| Argument | Type | Required | Description                                 |
|----------|------|----------|---------------------------------------------|
| idea     | str  | yes      | The description of your idea                |
| name     | str  | no       | An optional name to give to your idea       |
| category | str  | no       | An optional category to assign to your idea |

### Mentions

You won't always have the idea. Or you might but you don't want to (or forget) to use the slash command. Fortunately, there's another option.

Fortunately, you can still save that idea by tagging @ideabot in a reply to the message. You may optionally also add a category and name by separating them by commas.

Examples:

```
@anotheruser: Let's take over the world
↳ @you: @ideabot
```

Result: Ideabot remembers that you saved the idea "Let's take over the world".

```
@anotheruser: Let's take over the world
↳ @you: @ideabot domination
```

Result: Ideabot remembers that you saved the idea "Let's take over the world" with the category "domination".

```
@anotheruser: Let's take over the world
↳ @you: @ideabot domination, World Control
```

Result: Ideabot remembers that you saved the idea "Let's take over the world" with the category "domination" and name "World Control".